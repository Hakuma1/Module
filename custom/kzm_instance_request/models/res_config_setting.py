# -*- coding: utf-8 -*-
"""Config"""
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    """res.config.settings"""
    _inherit = 'res.config.settings'

    journal_id = fields.Many2one('account.journal', related="company_id.journal_id", string=u'Journal', readonly=False)

    salary_credit_account_id = fields.Many2one('account.account', related="company_id.salary_credit_account_id",
                                               string=u'Compte de crédit', readonly=False)

    salary_debit_account_id = fields.Many2one('account.account', related="company_id.salary_debit_account_id",
                                              string=u'Compte de débit', readonly=False)

    @api.model
    def get_values(self):
        res = super().get_values()
        params = self.env['ir.config_parameter'].sudo()
        print("params1", params.get_param('journal_id'))
        print("params2", params.get_param('salary_credit_account_id'))
        print("params3", params.get_param('salary_debit_account_id'))
        res.update(
            # mamda_credit_account_id=params.get_param('mamda_credit_account_id'),
            # mamda_debit_account_id=params.get_param('mamda_debit_account_id')
            journal_id=params.get_param('journal_id'),
            salary_credit_account_id=params.get_param('salary_credit_account_id'),
            salary_debit_account_id=params.get_param('salary_debit_account_id'),
        )
        return res

    def set_values(self):
        super().set_values()
        config_parameter_sudo = self.env['ir.config_parameter'].sudo()
        # config_parameter_sudo.set_param('mamda_credit_account_id', self.mamda_credit_account_id)
        # config_parameter_sudo.set_param('mamda_debit_account_id', self.mamda_debit_account_id)
        print("config_parameter_sudo1", config_parameter_sudo.get_param('journal_id'))
        print("config_parameter_sudo2", config_parameter_sudo.get_param('salary_credit_account_id'))
        print("config_parameter_sudo3", config_parameter_sudo.get_param('salary_debit_account_id'))
        config_parameter_sudo.set_param('journal_id', self.journal_id)
        config_parameter_sudo.set_param('salary_credit_account_id', self.salary_credit_account_id)
        config_parameter_sudo.set_param('salary_debit_account_id', self.salary_debit_account_id)


class ResCompany(models.Model):
    _inherit = "res.company"

    journal_id = fields.Many2one('account.journal', string=u'Journal', readonly=False)
    salary_credit_account_id = fields.Many2one('account.account', string=u'Compte de crédit', readonly=False,
                                               store=True)
    salary_debit_account_id = fields.Many2one('account.account', string=u'Compte de débit', readonly=False, store=True)
