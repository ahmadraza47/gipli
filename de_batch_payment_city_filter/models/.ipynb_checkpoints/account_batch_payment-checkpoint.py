# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountBatchPayment(models.Model):
    _inherit = 'account.batch.payment'
    
    city_id = fields.Many2one('res.city',string='City')

class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    city_id = fields.Many2one('res.city',string='City')
    