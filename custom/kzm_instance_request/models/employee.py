# -*- coding: utf-8 -*-
"""Employee inheritance"""

from odoo import models, fields, api


class Employee(models.Model):
    """Class representing employee"""
    _inherit = 'hr.employee'

    instance_ids = fields.One2many(comodel_name='kzm.instance.request', inverse_name='tl_id', string="Instance",
                                   tracking=True)
    instance_count = fields.Integer(string='Instance count', compute='_compute_instance_count')

    @api.depends('instance_ids')
    def _compute_instance_count(self):
        for rec in self:
            rec.instance_count = len(rec.instance_ids)

    def action_my_instances(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Instances',
            'res_model': 'kzm.instance.request',
            'domain': [('tl_id', '=', self.name)],
            'view_mode': 'tree,form',
            'target': 'current',
        }
