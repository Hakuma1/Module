# -*- coding: utf-8 -*-
"""Perimeter"""
from odoo import models, fields


class Perimeter(models.Model):
    """Perimeter"""
    _name = 'perimeter'
    _description = 'Perimeter'

    name = fields.Char(string="Name")
    color = fields.Integer('Color Index')
