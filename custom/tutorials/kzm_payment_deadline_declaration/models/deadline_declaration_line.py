# -*- coding: utf-8 -*-
""" Import """
from odoo import models, fields, api


class DeadlineDeclarationLine(models.Model):
    """ deadline.declaration.line """
    _name = 'deadline.declaration.line'
    _description = "Declaration lines"

    invoice_id = fields.Many2one('account.move', domain=[('move_type', '=', 'in_invoice')])
    partner_id = fields.Many2one('res.partner', related='invoice_id.partner_id', required=True, string="Supplier")
    IF = fields.Char(string="Supplier IF", related="partner_id.vat")
    rc = fields.Char(string="Supplier RC", related="partner_id.commercial_register")
    contact_address = fields.Char(related='partner_id.contact_address', string="Supplier address")
    invoice_number = fields.Char(related='invoice_id.ref')
    release_date = fields.Date()
    merchandise_type_id = fields.Many2one('merchandise.type', string="Merchandise nature",
                                          related="partner_id.merchandise_type_id", readonly=False)
    delivery_date = fields.Date()
    transaction_month = fields.Integer(compute="_compute_transaction_month", inverse="_inverse_transaction_month")
    transaction_year = fields.Integer(compute="_compute_transaction_year", inverse="_inverse_transaction_year")
    ascertainment_date = fields.Date()
    expected_payment_date = fields.Date(compute="_compute_expected_payment_date",
                                        inverse="_inverse_expected_payment_date")
    agreed_payment_date = fields.Date(compute="_compute_agreed_payment_date", inverse="_inverse_agreed_payment_date")
    expected_invoice_payment_deadline = fields.Integer()
    expected_invoice_payment_date = fields.Date()
    invoice_amount = fields.Float(compute="_compute_invoice_amount", inverse="_inverse_invoice_amount")
    amount_residual = fields.Float(compute="_compute_amount_residual", inverse="_inverse_amount_residual")
    payed_amount_out_deadline = fields.Float()
    payment_date_out_deadline = fields.Date()
    amount_justice = fields.Float(string="Amount subject to litigation")
    legal_appeal_date = fields.Date()
    amount_residual_after_jugdment = fields.Float()
    final_judgment_date = fields.Date()
    payment_mode = fields.Selection(
        [('1', 'Cash'), ('2', 'Check'), ('3', 'Withdrawal'), ('4', 'Transfer'),
         ('5', 'Bill of exchange')])
    payment_ref = fields.Char()
    declaration_id = fields.Many2one('deadline.declaration', ondelete="cascade")

    def _inverse_agreed_payment_date(self):
        pass

    def _compute_agreed_payment_date(self):
        for record in self:
            record.agreed_payment_date = record.invoice_id.agreed_payment_date

    def _inverse_transaction_month(self):
        pass

    def _inverse_transaction_year(self):
        pass

    def _inverse_amount_residual(self):
        pass

    @api.depends('invoice_id', 'invoice_id.amount_residual')
    def _compute_amount_residual(self):
        for record in self:
            record.amount_residual = record.invoice_id.amount_residual

    def _inverse_invoice_amount(self):
        pass

    @api.depends('invoice_id', 'invoice_id.amount_total')
    def _compute_invoice_amount(self):
        for record in self:
            record.invoice_amount = record.invoice_id.amount_total

    def _inverse_expected_payment_date(self):
        pass

    @api.depends('invoice_id', 'invoice_id.invoice_date_due')
    def _compute_expected_payment_date(self):
        for record in self:
            record.expected_payment_date = record.invoice_id.agreed_payment_date

    @api.depends('invoice_id', 'invoice_id.invoice_date')
    def _compute_transaction_year(self):
        for record in self:
            record.transaction_year = record.invoice_id.invoice_date.year if record.invoice_id.invoice_date else 0

    @api.depends('invoice_id', 'invoice_id.invoice_date')
    def _compute_transaction_month(self):
        for record in self:
            record.transaction_month = record.invoice_id.invoice_date.month if record.invoice_id.invoice_date else 0
