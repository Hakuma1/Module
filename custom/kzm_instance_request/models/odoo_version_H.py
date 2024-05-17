# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class OdooVersion(models.Model):
    _inherit = 'odoo.version'

    instance_ids = fields.One2many('kzm.instance.request', 'odoo_id', string="Instance")
    instance_count = fields.Integer(string='Instance count', compute='_compute_instance_count')

    @api.depends('instance_ids')
    def _compute_instance_count(self):
        for rec in self:
            rec.instance_count = len(rec.instance_ids)
