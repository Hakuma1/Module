# -*- coding: utf-8 -*-

from odoo import models, fields


class Order(models.Model):
    """ Order """
    _inherit = 'sale.order'

    version_odoo_id = fields.Many2one(comodel_name="odoo.version", string="Id odoo version")

    def open_wizard(self):
        action = self.env.ref('kzm_instance_request.purchase_order_action').read()[0]
        return action
