# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TokenHistorique(models.Model):
    _name = 'token.historique'

    prompt_tokens = fields.Integer(string="Prompt tokens")
    total_tokens = fields.Integer(string="Total tokens")
    montant_total = fields.Float(string="Total amount", digits=[16, 6])
    answer = fields.Text(string="Answer")
    question = fields.Text(string="Question")
    token_info_id = fields.Many2one('token.info', string="Info")
