# -*- coding: utf-8 -*-
""" Import """
from odoo import models, fields


class AddInvoicesWizard(models.TransientModel):
    """ Add Invoices Wizard """
    _name = 'add.invoices.wizard'
    _description = "Add Invoices Wizard"

    invoice_ids = fields.Many2many('account.move')
    name = fields.Char(default='Factures')

    def create_declaration_lines(self):
        declaration = self.env.context.get('declaration', True)
        declaration = self.env['deadline.declaration'].browse(declaration)
        declaration.declaration_line_ids.unlink()
        for record in self.invoice_ids:
            declaration.declaration_line_ids = [(0, 0, {'invoice_id': record.id})]
