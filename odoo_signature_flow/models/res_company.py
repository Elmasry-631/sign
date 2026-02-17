from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    quotation_approver_a_id = fields.Many2one(
        "res.users",
        string="Quotation Approver 1",
    )
    quotation_approver_b_id = fields.Many2one(
        "res.users",
        string="Quotation Approver 2",
    )
    sales_order_company_signer_id = fields.Many2one(
        "res.users",
        string="Sales Order Company Signer",
    )
