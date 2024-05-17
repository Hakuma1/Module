# -*- coding: utf-8 -*-


from odoo import models, fields, api
from lxml import etree


class OdooVersion(models.Model):
    """Odoo version"""
    _name = 'odoo.version'
    _description = 'Version of odoo'

    name = fields.Char("Version")
    description = fields.Text()

    @api.model
    def fields_view_get(self, view_id=None, view_type=None, toolbar=False, submenu=False):
        res = super(OdooVersion, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                       submenu=submenu)
        doc = etree.XML(res['arch'])
        print("f view_type == 'form'", res)
        print("f view_type == 'form'", doc)
        if view_type in ['form', 'tree']:
            for node in doc.xpath("//field[@name='partner_id']"):
                node.set('invisible', 1)
            res['arch'] = etree.tostring(doc)
        return res
