# -*- coding: utf-8 -*-
"""Instance Management"""
from datetime import timedelta, date, datetime, time

import json
from odoo import models, fields, api, _, exceptions
from odoo.exceptions import ValidationError
import logging
from lxml import etree

_logger = logging.getLogger(__name__)


class KzmInstanceRequest(models.Model):
    """Module reprensenting instance requesting"""
    _name = 'kzm.instance.request'
    _description = 'Request for Proceedings'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(string="Designation", tracking=True, default=lambda self: _('New'))
    currency_id = fields.Many2one(comodel_name='res.currency', string='Devise')
    address_ip = fields.Char(string="IP Address")
    active = fields.Boolean(default=True)
    cpu = fields.Char(string="CPU")
    ram = fields.Char(string="RAM")
    disk = fields.Char(string="DISK")
    url = fields.Char(string="URL")
    state = fields.Selection(
        [('Draft', 'Draft'), ('Submitted', 'Submitted'), ('In process', 'In process'), ('Processed', 'Processed')],
        default='Draft', string="State", tracking=True)
    limit_date = fields.Date(string="Limit date", tracking=True)
    treat_date = fields.Datetime(string="Treat date")
    treat_duration = fields.Integer(string="Treat duration", compute='_compute_treat_duration', store=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string="Customer")
    tl_id = fields.Many2one(comodel_name='hr.employee', string="Employee")
    tl_user_id = fields.Many2one(related='tl_id.user_id', string="User on employee")
    odoo_id = fields.Many2one(comodel_name='odoo.version', string="Odoo version")
    perimeters_ids = fields.Many2many(comodel_name='perimeter', string="Perimeters")
    perimeters_count = fields.Integer(string='Perimeters count', compute='_compute_perimeters_count', store=True)
    address_id = fields.Many2one(related='tl_id.address_id', string='Address')
    sale_id = fields.Many2one(comodel_name='sale.order', string="Purchase order")
    prix = fields.Float(string="Prix", tracking=True, digits=(16, 6))

    @api.depends('perimeters_ids')
    def _compute_perimeters_count(self):
        for rec in self:
            rec.perimeters_count = len(rec.perimeters_ids)

    @api.depends('treat_date')
    def _compute_treat_duration(self):
        for rec in self:
            if rec.treat_date:
                treat = rec.treat_date.date()
                today = date.today()
                rec.treat_duration = (treat - today).days

    _sql_constraints = [
        ('unique_ip_address', 'UNIQUE (address_ip)', 'Ip Address must be unique')
    ]

    def action_draft(self):
        for record in self:
            record.state = "Draft"

    def action_submitted(self):
        for record in self:
            record.state = "Submitted"

    def action_in_process(self):
        for record in self:
            record.state = "In process"

    def action_processed(self):
        for record in self:
            self.state = "Processed"
            record.treat_date = datetime.now()

    def submitted_cron(self):
        element = self.env['kzm.instance.request'].search([('limit_date', '<=', date.today() + timedelta(days=5))])
        for record in element:
            record.action_submitted()

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('instance.increment') or _('New')
        res = super(KzmInstanceRequest, self).create(vals)
        return res

    def unlink(self):
        for record in self:
            if record.state != 'Draft':
                raise ValidationError(_("You can only delete an instance in \"Draft\" status !"))
            return super(KzmInstanceRequest, record).unlink()

    def write(self, vals):
        if vals.get('limit_date'):
            name = self.name
            deadline = vals.get('limit_date')
            date_time_obj = datetime.strptime(vals['limit_date'], '%Y-%m-%d')
            dat = date_time_obj.date()
            # print(self.limit_date)
            if dat < date.today():
                raise ValidationError(_("You cannot set a deadline later than today!"))
            users = self.env.ref('kzm_instance_request.group_instance_manager').users
            for user in users:
                self.activity_schedule('kzm_instance_request.gmail_activity_instance', user_id=user.id,
                                       note=f'You have to Process {name}', date_deadline=deadline)
        return super(KzmInstanceRequest, self).write(vals)

    @api.onchange('state')
    def onchange_state(self):
        if self.state == "Processed":
            self.treat_date = datetime.now()

    def test_button(self):
        # _logger.debug("C'est le débogage")
        # _logger.info("Test d'une requête")
        # _logger.error("Nous avons une erreur")
        # _logger.warning("Attention!!")
        # _logger.critical("Ceci est un message critique")
        # query = """select KZM.name from odoo_version as odoo join kzm_instance_request as KZM
        # on odoo.id=KZM.odoo_id;"""
        # print("self.env.cr", self.env.cr)
        # self.env.cr.execute(query)
        # result = self.env.cr.dictfetchall()
        # print(result)
        # print(len(result))
        # _logger.info(result)
        result_1 = self.env['kzm.instance.request'].search([('id', '=', 1)], limit=1)
        result_2 = self.env['kzm.instance.request'].search([('id', '=', 3)], limit=1)
        combinaison = result_1 + result_2
        print("combinaison", combinaison)
    def _get_average_cost(self):
        for record in self:
            grouped_result = record.read_group([('perimeters_count', '!=', False)], ['odoo_id', 'perimeters_count:avg'],
                                               ['odoo_id'])
            print('grouped_result ', grouped_result)

    # PORTAL
    def _get_portal_return_action(self):
        """ Return the action used to display orders when returning from customer portal. """
        self.ensure_one()
        return self.env.ref('kzm_instance_request_action_window')

    @api.model
    def get_view(self, view_id=None, view_type='form', **options):
        res = super(KzmInstanceRequest, self).get_view(view_id=view_id, view_type=view_type, **options)
        """doc = etree.XML(res['arch'])
        if view_type == 'tree':
            for node in doc.xpath("//field[@name='partner_id']"):
                print('node.get("modifiers")', node.get("modifiers"))
                if not node.get("modifiers"):
                    modifiers = {}
                else:
                    modifiers = json.loads(node.get("modifiers"))
                if 'invisible' not in modifiers:
                    modifiers['invisible'] = [(1, '=', 1)]
                print("node", node)
                node.set('modifiers', json.dumps(modifiers))
            res['arch'] = etree.tostring(doc, encoding='unicode')
            print("res['arch']", res['arch'])"""
        return res

    @api.model
    def liste_de_tous_les_elements(self):
        for record in self:
            return True
