import openai
from odoo import models, fields, api, _


class Chatbothistorique(models.Model):
    _name = "chatbot.historique"

    question = fields.Char('Question', required=True)
    answer = fields.Char('Answer', required=True)
    total_token = fields.Integer(string="Total Token")
    prompt_tokens = fields.Integer(string='Prompt tokens')
    prix_total = fields.Float(string="Montant total", digits=[16, 6])
    token_info_id = fields.Many2one('token.info', string="Token info")
