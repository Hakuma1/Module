# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TokenInfo(models.Model):
    _name = 'token.info'

    user_id = fields.Many2one("res.users", string="User")
    total_tokens = fields.Integer(string="Total tokens")
    montant_total = fields.Float(string="Total amount", digits=[16, 6])
    token = fields.Text(related='user_id.tokengpt', string="Token")
    historique_ids = fields.One2many('token.historique', 'token_info_id', string="Historique")
