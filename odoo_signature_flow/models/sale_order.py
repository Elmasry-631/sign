from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrderSignature(models.Model):
    _name = "sale.order.signature"
    _description = "Sale Order Signature Slot"
    _order = "slot asc, id asc"

    order_id = fields.Many2one("sale.order", required=True, ondelete="cascade")
    slot = fields.Integer(required=True)
    role = fields.Selection(
        selection=[
            ("sales_person", "Sales Person"),
            ("approver_a", "Approver 1"),
            ("approver_b", "Approver 2"),
            ("company", "Company"),
            ("customer", "Customer"),
        ],
        required=True,
    )
    role_label = fields.Char(required=True)
    required = fields.Boolean(default=True)

    signer_user_id = fields.Many2one("res.users", string="Signer User")
    signer_partner_id = fields.Many2one("res.partner", string="Signer Partner")

    signed = fields.Boolean(default=False)
    signed_by_user_id = fields.Many2one("res.users", string="Signed By")
    signed_on = fields.Datetime()

    _sql_constraints = [
        (
            "sale_order_signature_unique_slot",
            "unique(order_id, slot)",
            "Each signature slot must be unique per order.",
        )
    ]

    def action_mark_signed(self):
        for rec in self:
            rec.write(
                {
                    "signed": True,
                    "signed_by_user_id": self.env.user.id,
                    "signed_on": fields.Datetime.now(),
                }
            )


class SaleOrder(models.Model):
    _inherit = "sale.order"

    signature_line_ids = fields.One2many(
        "sale.order.signature", "order_id", string="Signatures", copy=False
    )
    signature_document_type = fields.Selection(
        [("quotation", "Quotation"), ("sales_order", "Sales Order")],
        compute="_compute_signature_document_type",
        store=False,
    )
    signature_fully_signed = fields.Boolean(compute="_compute_signature_fully_signed")

    @api.depends("state")
    def _compute_signature_document_type(self):
        for order in self:
            order.signature_document_type = (
                "sales_order" if order.state in ("sale", "done") else "quotation"
            )

    @api.depends("signature_line_ids.signed", "signature_line_ids.required")
    def _compute_signature_fully_signed(self):
        for order in self:
            required_lines = order.signature_line_ids.filtered(lambda l: l.required)
            order.signature_fully_signed = bool(required_lines) and all(
                required_lines.mapped("signed")
            )

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        orders._sync_signature_slots()
        return orders

    def write(self, vals):
        result = super().write(vals)
        tracked_fields = {"state", "user_id", "partner_id", "company_id"}
        if tracked_fields.intersection(vals.keys()):
            self._sync_signature_slots()
        return result

    def _build_signature_templates(self):
        self.ensure_one()
        if self.state in ("sale", "done"):
            return [
                {
                    "slot": 1,
                    "role": "company",
                    "role_label": _("توقيع الشركة"),
                    "required": True,
                    "signer_user_id": self.company_id.sales_order_company_signer_id.id,
                    "signer_partner_id": False,
                },
                {
                    "slot": 2,
                    "role": "customer",
                    "role_label": _("توقيع العميل"),
                    "required": True,
                    "signer_user_id": False,
                    "signer_partner_id": self.partner_id.id,
                },
            ]

        return [
            {
                "slot": 1,
                "role": "sales_person",
                "role_label": _("توقيع مسؤول المبيعات"),
                "required": True,
                "signer_user_id": self.user_id.id,
                "signer_partner_id": False,
            },
            {
                "slot": 2,
                "role": "approver_a",
                "role_label": _("توقيع المعتمد الأول"),
                "required": True,
                "signer_user_id": self.company_id.quotation_approver_a_id.id,
                "signer_partner_id": False,
            },
            {
                "slot": 3,
                "role": "approver_b",
                "role_label": _("توقيع المعتمد الثاني"),
                "required": True,
                "signer_user_id": self.company_id.quotation_approver_b_id.id,
                "signer_partner_id": False,
            },
        ]

    def _sync_signature_slots(self):
        for order in self:
            templates = order._build_signature_templates()
            existing_by_slot = {line.slot: line for line in order.signature_line_ids}
            active_slots = []
            for template in templates:
                active_slots.append(template["slot"])
                existing_line = existing_by_slot.get(template["slot"])
                vals = {
                    "role": template["role"],
                    "role_label": template["role_label"],
                    "required": template["required"],
                    "signer_user_id": template["signer_user_id"],
                    "signer_partner_id": template["signer_partner_id"],
                }
                if existing_line:
                    existing_line.write(vals)
                else:
                    order.write(
                        {
                            "signature_line_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "slot": template["slot"],
                                        **vals,
                                    },
                                )
                            ]
                        }
                    )

            order.signature_line_ids.filtered(
                lambda l: l.slot not in active_slots
            ).unlink()

    @api.constrains(
        "state",
        "user_id",
        "partner_id",
        "company_id",
        "signature_line_ids",
        "signature_line_ids.signer_user_id",
        "signature_line_ids.signer_partner_id",
    )
    def _check_signature_assignments(self):
        for order in self:
            if order.state in ("sale", "done"):
                if len(order.signature_line_ids) != 2:
                    raise ValidationError(_("Sales order must contain exactly 2 signatures."))
                company = order.signature_line_ids.filtered(lambda l: l.slot == 1)
                customer = order.signature_line_ids.filtered(lambda l: l.slot == 2)
                if not company or company.role != "company":
                    raise ValidationError(_("Slot #1 must be company signature."))
                if not customer or customer.role != "customer":
                    raise ValidationError(_("Slot #2 must be customer signature."))
                if not company.signer_user_id:
                    raise ValidationError(_("Company signer must be assigned."))
                if not customer.signer_partner_id:
                    raise ValidationError(_("Customer signer must be assigned."))
            else:
                if len(order.signature_line_ids) != 3:
                    raise ValidationError(_("Quotation must contain exactly 3 signatures."))
                line1 = order.signature_line_ids.filtered(lambda l: l.slot == 1)
                line2 = order.signature_line_ids.filtered(lambda l: l.slot == 2)
                line3 = order.signature_line_ids.filtered(lambda l: l.slot == 3)
                if not line1 or line1.role != "sales_person":
                    raise ValidationError(_("Quotation slot #1 must be sales person."))
                if not line2 or line2.role != "approver_a":
                    raise ValidationError(_("Quotation slot #2 must be approver 1."))
                if not line3 or line3.role != "approver_b":
                    raise ValidationError(_("Quotation slot #3 must be approver 2."))
                if not line1.signer_user_id:
                    raise ValidationError(_("Sales person signer must be assigned."))
                if not line2.signer_user_id or not line3.signer_user_id:
                    raise ValidationError(
                        _("Quotation approver 1 and approver 2 must be assigned.")
                    )
