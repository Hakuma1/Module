# -*- coding: utf-8 -*-
"""Import"""
from odoo import models


class PosSession(models.Model):
    """ Import """
    _inherit = 'pos.session'

    def _prepare_line(self, order_line):
        result = super(PosSession, self)._prepare_line(order_line)
        if any(order_line.order_id.payment_ids.mapped('payment_method_id.tax_id')):
            payments = order_line.order_id.payment_ids.filtered(lambda rec: rec.payment_method_id.tax_id)
            if payments:
                taxe_fin = []
                for payment in payments:
                    if order_line.id == order_line.order_id.lines[0].id:
                        tax_id = payment.payment_method_id.tax_id
                        sign = -1
                        price = sign * order_line.price_subtotal
                        check_refund = lambda x: x.qty * x.price_unit < 0
                        is_refund = check_refund(order_line)
                        tax_data = tax_id.compute_all(price_unit=price, quantity=abs(order_line.qty), currency=self.currency_id,
                                            is_refund=is_refund, fixed_multiplicator=sign)
                        taxes = tax_data['taxes']
                        for tax in taxes:
                            tax_rep = self.env['account.tax.repartition.line'].browse(tax['tax_repartition_line_id'])
                            tax['account_id'] = tax_rep.account_id.id
                        date_order = order_line.order_id.date_order
                        taxes = [{'date_order': date_order, **tax} for tax in taxes]
                        the_amout_give = payment.amount
                        ttc = 100 * the_amout_give / (payment.payment_method_id.tax_id.amount + 100)
                        taxes[0]['amount'] = -round(the_amout_give - ttc, 2)
                        taxe_fin.append(taxes[0])
                for element in taxe_fin:
                    result['taxes'].append(element)

        return result

    def _loader_params_pos_payment_method(self):
        params = super()._loader_params_pos_payment_method()
        params['search_params']['fields'].append('tax_id')
        params['search_params']['fields'].append('tax_amount')
        return params
