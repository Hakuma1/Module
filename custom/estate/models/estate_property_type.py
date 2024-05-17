# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type'
    _order = "sequence, name"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Property")
    sequence = fields.Integer(string="Sequence")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offer")
    offers_count = fields.Integer(string="Number", compute="_compute_offer_count")

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name must be unique!!')]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offers_count = len(record.offer_ids)

    def action_my_offers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Offers',
            'res_model': 'estate.property.offer',
            'domain': [('property_type_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }
