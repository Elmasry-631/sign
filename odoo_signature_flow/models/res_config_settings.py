from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    quotation_approver_a_id = fields.Many2one(
        related="company_id.quotation_approver_a_id",
        readonly=False,
    )
    quotation_approver_b_id = fields.Many2one(
        related="company_id.quotation_approver_b_id",
        readonly=False,
    )
    sales_order_company_signer_id = fields.Many2one(
        related="company_id.sales_order_company_signer_id",
        readonly=False,
    )
