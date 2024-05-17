# -*- coding: utf-8 -*-
""" Import """
from odoo import models, fields


class MerchandiseType(models.Model):
    """ Merchandise Type """
    _name = 'merchandise.type'

    name = fields.Char(required=True)
