from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    supplier_id = fields.Many2one(
        comodel_name='res.partner',
        string='Supplier',
        required=False, domain=([('supplier', '=', '1')]))

    consignee = fields.Many2one(
        comodel_name='res.partner',
        string='Consignee',
        required=False, domain=([('customer', '=', '1')]))

    origin_src = fields.Char(
        string='origin',
        required=False)


    destination = fields.Char(
        string='Destination',
        required=False)

    service_type = fields.Many2one(
        comodel_name='crmextend.service.type',
        string='Service type',
        required=False)

    weight = fields.Float(
        string='Weight',
        required=False)

    handling_instruction = fields.Char(
        string='Handling instruction',
        required=False)

class AccountInvoiceLine(models.Model):
    _inherit='account.invoice.line'

    weight = fields.Float(
        string='Weight',
        required=False,)

    height = fields.Float(
        string='Height',
        required=False)

    lengt = fields.Float(
        string='Length',
        required=False)

    total_weight = fields.Float(
        string='Total weight',
        required=False)

    crm_lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Leads',
        required=False)