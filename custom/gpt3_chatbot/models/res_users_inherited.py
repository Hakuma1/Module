from odoo import models, fields, api, _


class ResUsersInherited(models.Model):
    _inherit = "res.users"

    chatgpt_token = fields.Text(string="ChatGPT Token")
