# -*- coding: utf - 8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
from odoo.fields import Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_do_sold(self):
        res = super().action_do_sold()
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        invoice_lines_1 = {
            "name": self.name,
            "quantity": 1,
            "price_unit": self.selling_price * 0.6 / 100
        }
        invoice_lines_2 = {
            "name": "Administrative fees",
            "quantity": 1,
            "price_unit": 100
        }
        for record in self:
            move_vals = {
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                'partner_id': record.buyer_id.id,
                'currency_id': 2,
                'invoice_date': date.today(),
                'invoice_line_ids': [Command.create(invoice_lines_1), Command.create(invoice_lines_2)]
            }
            move = record.env['account.move'].create(move_vals)
        return res, move
