# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date, timedelta
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'
    _order = "price desc"

    price = fields.Float(string="Price")
    state = fields.Selection(string="Status", selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner", required=True)
    property_id = fields.Many2one(comodel_name='estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one('estate.property.type', string="Property type",
                                       related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The price must be strictly positive!!')]

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = timedelta(days=record.validity) + record.create_date
            else:
                record.date_deadline = date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_do_accepted(self):
        for record in self:
            accepted = record.env['estate.property.offer'].search(
                [('state', '=', 'accepted'), ('property_id', '=', self.property_id.id)])
            if len(accepted) > 0 and accepted.id != record.id:
                raise ValidationError(_("No two offers can be accepted."))
            else:
                record.state = 'accepted'
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price

    def action_do_refused(self):
        for record in self:
            if record.state == 'accepted':
                record.property_id.buyer_id = None
                record.property_id.selling_price = None
                record.state = 'refused'
            else:
                record.state = 'refused'

    def write(self, vals):
        if vals.get('price'):
            if self.state == 'accepted':
                self.property_id.selling_price = vals.get('price')
        if vals.get('partner_id'):
            if self.state == 'accepted':
                self.property_id.buyer_id = vals.get('partner_id')
        return super(EstatePropertyOffer, self).write(vals)

    def unlink(self):
        for record in self:
            if record.property_id.accepted_offer == record.id:
                record.property_id.accepted_offer = None
                record.property_id.selling_price = None
                record.property_id.buyer_id = None
            return super(EstatePropertyOffer, record).unlink()

    @api.model
    def create(self, vals):
        offer_id = super().create(vals)
        offer_id.property_id.state = 'offer_received'
        if vals['price'] < offer_id.property_id.best_price:
            raise ValidationError(_('The offer must be higher than ')+str(offer_id.property_id.best_price))
        return offer_id

