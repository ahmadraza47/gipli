# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from dateutil.relativedelta import relativedelta
from odoo.addons import decimal_precision as dp

class AccountMoveInvoiceCheck(models.Model):
    _inherit = 'account.move'
    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        invoice_date = self.invoice_date
        warning = {}
        partner_invoices = self.env['account.move'].search([('partner_id', '=', self.partner_id.id), ('state', 'not in', ['cancel']), ('invoice_date', '>=', invoice_date), ('invoice_date', '<=', invoice_date), ],limit=1)
        if len(partner_invoices):
            warning = {
                'title': _("Warning for %s") % self.partner_id.name,
                'message': 'Invoice already created in this month'
            }
            return {'warning': warning}
                
        res = super(AccountMoveInvoiceCheck,self)._onchange_partner_id()
        return res
    
    @api.onchange('invoice_date')
    def _onchange_invoice_date(self):
        from_invoice_date = fields.Datetime.from_string(self.invoice_date) - relativedelta(days=10),
        to_invoice_date = fields.Datetime.from_string(self.invoice_date) + relativedelta(days=10),
        
        warning = {}
        partner_invoices = self.env['account.move'].search([('partner_id', '=', self.partner_id.id), ('state', 'not in', ['cancel']), ('invoice_date', '>=', from_invoice_date), ('invoice_date', '<=', to_invoice_date), ],limit=1)
        if len(partner_invoices):
            warning = {
                'title': _("Warning for %s") % self.partner_id.name,
                'message': 'Invoice already created in this month'
            }
            return {'warning': warning}