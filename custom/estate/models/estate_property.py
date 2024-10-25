# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date, timedelta
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate property'
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", copy=False, default=date.today() + timedelta(days=90))
    expected_price = fields.Float(string="Expected price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden area")
    garden_orientation = fields.Selection(string="Garden orientation",
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),
                                                     ('west', 'West')],
                                          help="It is the garden orientation")
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(string="State", selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                                                        ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
                                                        ('canceled', 'Canceled')], required=True, copy=False,
                             default='new')
    property_type_id = fields.Many2one('estate.property.type', string="Property type")
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    seller_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.uid)
    tag_ids = fields.Many2many('estate.property.tag', string="Property tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offer")
    total_area = fields.Float(string="Total area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(string="Best offer", compute="_compute_best_price")
    user_id = fields.Many2one('res.users', string="Salesperson", related='seller_id')

    """ Accepted offer """
    accepted_offer = fields.Integer(string="Accepted offer",
                                    compute="_compute_accepted_offer")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive')]

    @api.depends('offer_ids.state')
    def _compute_accepted_offer(self):
        for record in self:
            accepted = record.env['estate.property.offer'].search(
                [('state', '=', 'accepted'), ('property_id', '=', self.id)])
            record.accepted_offer = accepted.id

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            price = record.offer_ids.mapped('price')
            if len(price) > 0:
                record.best_price = max(price)
            else:
                record.best_price = None

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = None
                record.garden_orientation = None

    def action_do_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise ValidationError(_("Canceled property cannot be sold."))
            else:
                record.state = 'sold'
        return True

    def action_do_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise ValidationError(_("Sold property cannot be canceled."))
            else:
                record.state = 'canceled'
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_date_end(self):
        for record in self:
            if record.selling_price < record.expected_price * 0.9 and record.accepted_offer:
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! You must reduce the expected price "
                    "if you want to accept this offer.")

    @api.ondelete(at_uninstall=False)
    def not_delete_new_cancel_property(self):
        for record in self:
            if record.state != "new" and record.state != "canceled":
                raise ValidationError(_("Only new and canceled properties can be deleted!!"))
