# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta


class EstatePropertyType(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'user_id', string="Property",
                                   domain="['|', ('state', '=', 'new'), ('state', '=', 'offer_received')]")
