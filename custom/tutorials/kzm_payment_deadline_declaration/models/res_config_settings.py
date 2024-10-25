# -*- coding: utf-8 -*-
""" Import """
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """res.config.settings"""
    _inherit = 'res.config.settings'

    start_declaration_payment_deadline = fields.Date(related='company_id.start_declaration_payment_deadline',
                                                     readonly=False)

