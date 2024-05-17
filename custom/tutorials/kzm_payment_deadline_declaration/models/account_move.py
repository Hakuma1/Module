# -*- coding: utf-8 -*-
""" Import """
from datetime import timedelta
from odoo import models, fields, api


class AccountMove(models.Model):
    """ Account Move """
    _inherit = 'account.move'

    merchandise_type_id = fields.Many2one('merchandise.type', related='partner_id.merchandise_type_id', readonly=False,
                                          store=True)
    agreed_payment_delay = fields.Integer(related="partner_id.agreed_payment_delay", readonly=False)
    agreed_payment_date = fields.Date(compute="_compute_agreed_payment_date", store=True)

    @api.depends('invoice_date', 'agreed_payment_delay')
    def _compute_agreed_payment_date(self):
        for record in self:
            record.agreed_payment_date = record.invoice_date + timedelta(
                days=record.agreed_payment_delay) if record.invoice_date else False
