# -*- coding: utf-8 -*-
""" Import """
from odoo import models, fields


class ResPartner(models.Model):
    """ Res Partner """
    _inherit = 'res.partner'

    commercial_register = fields.Char()
    merchandise_type_id = fields.Many2one('merchandise.type')
    agreed_payment_delay = fields.Integer()
