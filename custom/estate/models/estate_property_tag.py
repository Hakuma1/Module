# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate property tag'
    _order = "name"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name must be unique!!')]
