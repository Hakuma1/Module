# -*- coding: utf-8 -*-
""" Import """
import base64
from lxml import etree
from odoo import models, fields, api, _

translationTable = str.maketrans("ÉÀéàèùâêîôûç,-/+'", "ÉAeaeuaeiouc___ _")


class DeadlineDeclaration(models.Model):
    """ deadline.declaration"""
    _name = 'deadline.declaration'
    _description = "Declaration payment deadlines"

    name = fields.Char(default=lambda self: _('New'))
    IF = fields.Char(compute="_compute_if")
    quarter = fields.Selection([('1', 'T1'), ('2', 'T2'), ('3', 'T3'), ('4', 'T4')], required=True)
    judgment_date = fields.Date(required="True", string="Date of judgment opening proceedings")
    turnover = fields.Float(required=True)
    declaration_line_ids = fields.One2many('deadline.declaration.line', 'declaration_id')
    deadline_declaration_lines_count = fields.Integer(compute="_compute_deadline_declaration_lines_count")
    fichier_edi = fields.Binary(string="EDI File")
    edi_filename = fields.Char(string="EDI")
    declaration_date = fields.Date(required=True)
    state = fields.Selection([('draft', 'Draft'), ('submitted', 'Submitted')], default='draft')


    def load_invoices(self):
        for record in self:
            invoices = self.env['account.move'].search(
                [('move_type', '=', 'in_invoice'), ('invoice_payment_state', 'in', ['not_paid', 'in_payment']),
                 ('agreed_payment_date', '>=', self.env.company.start_declaration_payment_deadline),
                 ('agreed_payment_date', '<=', record.declaration_date),
                 ('state', '=', 'posted'), ('amount_total', '>=', 10000)])
            record.declaration_line_ids.unlink()
            for rec in invoices:
                record.declaration_line_ids = [(0, 0, {'invoice_id': rec.id})]

    def reset_declaration_line(self):
        self.declaration_line_ids.unlink()

    def add_invoices(self):
        element = self.env['add.invoices.wizard'].search([])
        if element:
            element.invoice_ids = False
        else:
            element = self.env['add.invoices.wizard'].create({})

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'add.invoices.wizard',
            'res_id': element.id,
            'target': 'new',
            'context': {'create': False, 'delete': False, 'edit': False, 'declaration': self.id},
            'type': 'ir.actions.act_window',
        }

    def generate_edi(self):
        root = etree.Element("DeclarationDelaiPaiement")
        etree.SubElement(root, "identifiantFiscal").text = str(self.IF if self.IF else '')
        etree.SubElement(root, "annee").text = str(self.declaration_date.year)
        periode = ''
        if self.env.company.declaration_payment_deadline == '1':
            periode = '5'
        elif self.env.company.declaration_payment_deadline == '2':
            if self.quarter == '1':
                periode = '1'
            elif self.quarter == '2':
                periode = '2'
            elif self.quarter == '3':
                periode = '3'
            elif self.quarter == '4':
                periode = '4'
        etree.SubElement(root, "periode").text = str(periode)

        activite = ''
        if self.env.company.activity_type == '1':
            activite = 1
        elif self.env.company.activity_type == '2':
            activite = 2
        etree.SubElement(root, "activite").text = str(activite)
        etree.SubElement(root, "chiffreAffaire").text = str(int(self.turnover) if self.turnover else '')
        liste_factures_hors_delai = etree.SubElement(root, "listeFacturesHorsDelai")
        for record in self.declaration_line_ids:
            facture_hors_delai = etree.SubElement(liste_factures_hors_delai, "FactureHorsDelai")
            etree.SubElement(facture_hors_delai, "identifiantFiscal").text = str(record.IF if record.IF else '')
            contact_address = ''
            if record.partner_id.street:
                contact_address += record.partner_id.street + ' '
            if record.partner_id.street2:
                contact_address += record.partner_id.street2 + ' '
            if record.partner_id.city:
                contact_address += record.partner_id.city + ' '
            if record.partner_id.state_id:
                contact_address += record.partner_id.state_id.name + ' '
            if record.partner_id.zip:
                contact_address += record.partner_id.zip + ' '
            if record.partner_id.country_id:
                contact_address += record.partner_id.country_id.name
            etree.SubElement(facture_hors_delai, "adresseSiegeSocial").text = str(
                contact_address.translate(translationTable))
            etree.SubElement(facture_hors_delai, "numFacture").text = str(
                record.invoice_number if record.invoice_number else '')
            etree.SubElement(facture_hors_delai, "dateEmission").text = str(
                record.release_date.strftime("%Y-%m-%d") if record.release_date else '')
            etree.SubElement(facture_hors_delai, "natureMarchandise").text = str(
                record.merchandise_type_id.name if record.merchandise_type_id else '')
            etree.SubElement(facture_hors_delai, "dateLivraisonMarchandise").text = str(
                record.delivery_date.strftime("%Y-%m-%d") if record.delivery_date else '')
            etree.SubElement(facture_hors_delai, "datePrevuePaiement").text = str(
                record.expected_payment_date.strftime("%Y-%m-%d") if record.expected_payment_date else '')
            etree.SubElement(facture_hors_delai, "montantFactureTtc").text = str(
                record.invoice_amount if record.invoice_amount else '')
            etree.SubElement(facture_hors_delai, "montantNonEncorePaye").text = str(
                record.amount_residual if record.amount_residual else '')
            etree.SubElement(facture_hors_delai, "montantPayeHorsDelai").text = str(
                record.payed_amount_out_deadline if record.payed_amount_out_deadline else '')
            etree.SubElement(facture_hors_delai, "datePaiementHorsDelai").text = str(
                record.payment_date_out_deadline.strftime("%Y-%m-%d") if record.payment_date_out_deadline else '')
            mode_paiement = ''
            if record.payment_mode == '1':
                mode_paiement = 1
            if record.payment_mode == '2':
                mode_paiement = 2
            if record.payment_mode == '3':
                mode_paiement = 3
            if record.payment_mode == '4':
                mode_paiement = 4
            if record.payment_mode == '5':
                mode_paiement = 5
            etree.SubElement(facture_hors_delai, "modePaiement").text = str(mode_paiement)
            etree.SubElement(facture_hors_delai, "referencePaiement").text = str(
                record.payment_ref if record.payment_ref else '')

        xml_data = f"{etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')}"

        xml_data = xml_data.replace("\\n", "\n")[2:-1]

        edi = base64.b64encode(xml_data.encode("utf-8"))
        self.write({
            'fichier_edi': edi.decode("utf-8"),
            'edi_filename': 'declarationDelaiPaiement.xml'

        })
        return True

    def action_deadline_declaration_line(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoice'),
            'res_model': 'deadline.declaration.line',
            'domain': [('id', 'in', self.declaration_line_ids.ids)],
            'view_mode': 'tree',
            'target': 'current',
        }

    def _compute_deadline_declaration_lines_count(self):
        for record in self:
            record.deadline_declaration_lines_count = len(record.declaration_line_ids)

    def _compute_if(self):
        for record in self:
            record.IF = self.env.company.vat

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('deadline.declaration.increment') or _('New')
        res = super(DeadlineDeclaration, self).create(vals)
        return res
