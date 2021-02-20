from odoo import fields, models, api
from collections import defaultdict
class SaleOrder(models.Model):
    _inherit = "sale.order"


    supplier_id=fields.Many2one(
        comodel_name='res.partner',
        string='Supplier',
        required=False,domain=([('supplier','=','1')]))

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

    @api.model
    def default_get(self, fields):
        vals = super(SaleOrder, self).default_get(fields)
        ord = [(5, 0, 0)]
        if 'name' in vals:
            if vals['name']=='New' and 'opportunity_id' in vals:
                crm_lead = self.env['crm.lead'].search([('id','=',vals['opportunity_id'])])
                for rec in crm_lead.shipement_ids:
                    line = (0, 0, {
                        'product_id': rec.product_id.id,
                        'product_uom_qty': rec.product_uom_qty,
                        'weight': rec.weight,
                        'height': rec.height,
                        'lengt': rec.lengt,
                        'total_weight': rec.total_weight,
                        'price_unit': rec.product_id.lst_price,
                        'name': rec.product_id.name,
                        'customer_lead': crm_lead.partner_id.id,
                        'invoice_status':'to invoice',
                        'product_uom':1,
                        'qty_delivered':0,
                        'qty_to_invoice':rec.product_uom_qty,
                        'qty_invoiced':0,
                        'state':'sale',
                    })
                    ord.append(line)
                vals['order_line'] = ord
                vals['supplier_id'] =crm_lead.supplier_id.id
                vals['consignee'] = crm_lead.consignee.id
                vals['destination'] = crm_lead.destination
                vals['origin_src'] = crm_lead.origin_src
                vals['service_type'] = crm_lead.service_type.id
                vals['weight'] = crm_lead.weight
                vals['handling_instruction'] = crm_lead.handling_instruction
        return vals


    @api.multi
    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        company_id = self.company_id.id
        journal_id = (self.env['account.invoice'].with_context(company_id=company_id or self.env.user.company_id.id)
            .default_get(['journal_id'])['journal_id'])
        if not journal_id:
            raise UserError(_('Please define an accounting sales journal for this company.'))
        vinvoice = self.env['account.invoice'].new({'partner_id': self.partner_invoice_id.id, 'type': 'out_invoice'})
        # Get partner extra fields
        vinvoice._onchange_partner_id()
        invoice_vals = vinvoice._convert_to_write(vinvoice._cache)
        invoice_vals.update({
            'name': (self.client_order_ref or '')[:2000],
            'origin': self.name,
            'type': 'out_invoice',
            'account_id': self.partner_invoice_id.property_account_receivable_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'journal_id': journal_id,
            'currency_id': self.pricelist_id.currency_id.id,
            'comment': self.note,
            'payment_term_id': self.payment_term_id.id,
            'fiscal_position_id': self.fiscal_position_id.id or self.partner_invoice_id.property_account_position_id.id,
            'company_id': company_id,
            'user_id': self.user_id and self.user_id.id,
            'team_id': self.team_id.id,
            'transaction_ids': [(6, 0, self.transaction_ids.ids)],
            'supplier_id': self.supplier_id.id,
            'consignee': self.consignee.id,
            'destination': self.destination,
            'origin_src': self.origin_src,
            'service_type': self.service_type.id,
            'weight': self.weight,
            'handling_instruction': self.handling_instruction,
        })
        return invoice_vals





class SaleOrderLine(models.Model):
    _inherit='sale.order.line'

    weight = fields.Float(
        string='Weight',
        required=False)

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

    @api.multi
    def _prepare_invoice_line(self, qty):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        res = {}
        product = self.product_id.with_context(force_company=self.company_id.id)
        account = product.property_account_income_id or product.categ_id.property_account_income_categ_id

        if not account and self.product_id:
            raise UserError(
                _('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                (self.product_id.name, self.product_id.id, self.product_id.categ_id.name))

        fpos = self.order_id.fiscal_position_id or self.order_id.partner_id.property_account_position_id
        if fpos and account:
            account = fpos.map_account(account)

        res = {
            'name': self.name,
            'sequence': self.sequence,
            'origin': self.order_id.name,
            'account_id': account.id,
            'price_unit': self.price_unit,
            'quantity': qty,
            'discount': self.discount,
            'uom_id': self.product_uom.id,
            'product_id': self.product_id.id or False,
            'invoice_line_tax_ids': [(6, 0, self.tax_id.ids)],
            'account_analytic_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'display_type': self.display_type,
            'weight': self.weight,
            'height': self.height,
            'lengt': self.lengt,
            'total_weight': self.total_weight,
        }
        return res

