import time
import re
from openerp import models, fields, api, tools, _
class sale_order(models.Model):
    _inherit = 'sale.order'
    version = fields.Integer(string=None,default=1,copy=True)
    crm_lead_id = fields.Many2one('crm.lead', string='Leads', index=True)
    is_copied = fields.Boolean(string='Is Copied?',default=False,copy=False)
    is_templete = fields.Boolean('Is Templete')
    total_confirm_sale = fields.Float(string='Total Sale Value')
    order_details = fields.Html('Quotation Details')
    templete_id = fields.Many2one('sale.order', 'Chose Templete', domain="[('is_templete', '=', True)]")    
    payment_company_id = fields.Char(string='Mother Company', related='partner_id.x_mother_company_id.name')
    @api.onchange('templete_id')
    def _onchange_is_templete(self):
        if self.templete_id:
            templete = self.env['sale.order'].browse(self.templete_id.id)
            self.order_details = templete.order_details
    @api.multi
    def copy_button(self, default=None):
        default = dict(default or {})
        default.update({
            'name': self.name.split('_')[0] + "_" + str(self.version),
            'version': self.version + 1
        })
        ret = super(sale_order, self).copy(default)
        self.write({'is_copied': True})
        return {
            'name': _("Products to Process"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'sale.order',
            'res_id': ret.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': '[]',
            'flags' : {'initial_mode': 'edit'}
        }


class crm_lead(models.Model):
    _inherit = 'crm.lead'
    sale_revenue = fields.Float('Revenue')
    reason_to_fail = fields.Text('Reason to fail')
    co_users_ids = fields.One2many('res.users', 'crm_lead_id')
    co_partner_ids = fields.One2many('res.partner', 'crm_lead_id')
class res_users(models.Model):
    _inherit = 'res.users'
    crm_lead_id = fields.Integer('CRM Lead')

class res_partner(models.Model):
    _inherit = 'res.partner'
    crm_lead_id = fields.Integer('CRM Lead')