from odoo import models, fields, api, _


class TokenInfor(models.Model):
    _name = "token.info"
    _rec_name = 'token'

    total_token = fields.Integer(string="Total Token")
    user_id = fields.Many2one('res.users', string="User")
    token = fields.Text(string="Token")
    prix_total = fields.Float(string="Montant total", digits=[16, 6])
    historique_ids = fields.One2many("chatbot.historique", 'token_info_id')