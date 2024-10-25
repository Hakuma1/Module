# -*- coding: utf-8 -*-
""" Import """
from odoo import models, fields


class ResCompany(models.Model):
    """ Res Company """
    _inherit = 'res.company'

    activity_type = fields.Selection(
        [('1', 'Normal Activity'), ('2', 'During safeguard, recovery or liquidation proceedings')], default='1')
    declaration_payment_deadline = fields.Selection([('1', 'Annual'), ('2', 'Quarterly')], default='2')
    start_declaration_payment_deadline = fields.Date()
