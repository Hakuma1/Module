# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OdooVersion(models.Model):
    """Odoo version"""
    _inherit = 'odoo.version'

    instance_ids = fields.One2many('kzm.instance.request', 'odoo_id', string="Instance")
    instance_count = fields.Integer(string='Instance count', compute='_compute_instance_count')

    @api.depends('instance_ids')
    def _compute_instance_count(self):
        for rec in self:
            rec.instance_count = len(rec.instance_ids)

    def test_ajout(self):
        for record in self:
            record.instance_ids = [(5, 0, 0)]
