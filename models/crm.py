from odoo import fields, models, api


class CRM_ServiceType(models.Model):
    _name='crmextend.service.type'

    name = fields.Char(
        string='Name', 
        required=False)


class CRM(models.Model):
    _inherit = 'crm.lead'

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

    shipement_ids = fields.One2many(
        comodel_name='crmextend.shipment.details',
        inverse_name='crm_lead_id',
        string='Shipement_ids',
        required=False)


    def order_lines(self):
        for rec in self.shipement_ids:
            val={
                'product_id':rec.product_id.id,
                'product_uom_qty':rec.qty,
                'weight':rec.weight,
                'height':rec.height,
                'lengt':rec.lengt,
                'total_weight':rec.totam_weight,
            }

    @api.multi
    def _prepare_quotation(self):
        self.ensure_one()
        company_id = self.company_id.id
        print('ok')
        print(self.origin_src)
        quot = self.env['sale.order'].new({'partner_id': self.partner_id})
        # Get partner extra fields
        quot._onchange_partner_id()
        quot_vals = quot._convert_to_write(quot._cache)
        quot_vals.update({
            'partner_id': self.partner_id,
            'team_id': self.team_id,
            'campaign_id': self.campaign_id,
            'medium_id': self.medium_id,
            'origin': self.name,
            'source_id': self.source_id,
            'supplier_id': self.supplier_id,
            'consignee': self.consignee,
            'destination': self.destination,
            'origin_src': self.origin_src,
            'service_type': self.service_type,
            'weight': self.weight,
            'handling_instruction': self.handling_instruction,
            'shipement_ids': self.shipement_ids,
        })
        return quot_vals





class CRMShipment(models.Model):

    _name='crmextend.shipment.details'

    order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Order_id',
        required=False)

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=False)

    product_uom_qty = fields.Float(
        string='Qty', 
        required=False)
    
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

