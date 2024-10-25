# -*- coding: utf-8 -*-
"""Import"""
from odoo import models, fields


class PosPaymentMethod(models.Model):
    """pos.payment.method"""
    _inherit = "pos.payment.method"

    tax_id = fields.Many2one('account.tax')
    tax_amount = fields.Float(related="tax_id.amount", store=True)
