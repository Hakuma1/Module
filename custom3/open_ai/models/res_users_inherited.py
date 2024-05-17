# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsersInherited(models.Model):
    _inherit = "res.users"

    tokengpt = fields.Text(string="TokenGPT")
