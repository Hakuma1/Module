# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import ValidationError


class CreateInstance(models.TransientModel):
    """Wizard"""
    _name = "create.instance.wizard"
    _description = 'Request instance wizard'

    cpu = fields.Char(string="CPU")
    ram = fields.Char(string="RAM")
    disk = fields.Char(string="DISK")
    tl_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    limit_date = fields.Date(string="Limit date")
    url = fields.Char(string="URL")
    tl_id = fields.Many2one(comodel_name='hr.employee', string="Employee")

    def _default_sale_order(self):
        return self.env['sale.order'].browse(self._context.get('active_ids'))

    sale_ids = fields.Many2many(comodel_name="sale.order", string="Sale order", required=True,
                                default=_default_sale_order)

    def action_save(self):
        ids = []

        if int(self.cpu) <= 0 or int(self.ram) <= 0 or int(self.disk) <= 0:
            raise ValidationError(_("You can't request instances with zero performance!"))
        for record in self.sale_ids:
            val = self.env['kzm.instance.request'].create({'cpu': self.cpu, 'ram': self.ram, 'disk': self.disk,
                                                           'tl_id': self.tl_id,
                                                           'limit_date': self.limit_date,
                                                           'url': self.url, 'partner_id': record.partner_id.id,
                                                           'sale_id': record.id})
            ids.append(val.id)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Instances',
            'res_model': 'kzm.instance.request',
            'domain': [('id', '=', ids)],
            'view_mode': 'tree,form',
            'target': 'current',
        }
