odoo.define('stamp_duties.OrderStampDuties', function (require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const { Orderline, Payment } = require('point_of_sale.models');
    var utils = require('web.utils');

    var round_pr = utils.round_precision;
    var round_di = utils.round_decimals;

    const PaymentStampDuties = (Payment) => class PaymentStampDuties extends Payment {

        set_amount(value){
            this.order.assert_editable();
            const tax_amount = +this.payment_method.tax_amount * value / 100
            this.before_stamp_duties = round_di(parseFloat(value) || 0, this.pos.currency.decimal_places);
            this.stamp_duties = parseFloat(round_pr(tax_amount, this.pos.currency.rounding).toFixed(2));
            value = value + this.stamp_duties
            this.amount = round_di(parseFloat(value) || 0, this.pos.currency.decimal_places);
        }

        get_amount_before_stamp_duties(){
            return this.before_stamp_duties;
        }

        get_stamp_duties(){
           return this.stamp_duties;
        }

    }
    Registries.Model.extend(Payment, PaymentStampDuties);
    const OrderlineStampDuties = (Orderline) => class OrderlineStampDuties extends Orderline {

        get_all_prices(qty = this.get_quantity()){
            var price_unit = this.get_unit_price() * (1.0 - (this.get_discount() / 100.0));
            var taxtotal = 0;

            var product =  this.get_product();
            var taxes_ids = this.tax_ids || product.taxes_id;
            taxes_ids = _.filter(taxes_ids, t => t in this.pos.taxes_by_id);
            var taxdetail = {};
            var product_taxes = this.pos.get_taxes_after_fp(taxes_ids, this.order.fiscal_position);
            var prix_base;

            var all_taxes = this.compute_all(product_taxes, price_unit, qty, this.pos.currency.rounding);
            var all_taxes_before_discount = this.compute_all(product_taxes, this.get_unit_price(), qty, this.pos.currency.rounding);
            _(all_taxes.taxes).each(function(tax) {
                taxtotal += tax.amount;
                prix_base = tax.base;
                taxdetail[tax.id] = {
                    amount: tax.amount,
                    base: tax.base,
                };
            });
            let taxe_amount = 0;
            let taxe_id = false;
            if(this.order && this.order.paymentlines && this.order.orderlines[0] == this) {
                const especes = this.order.paymentlines.filter(element => element.payment_method.tax_id);
                if(especes){
                    for(let espece of especes){
                        taxe_id = +espece.payment_method.tax_id[0];
                        const taxe_amount_given = +espece.payment_method.tax_amount || 0;
                        const taxe_amount_calc = espece.amount - (100 * espece.amount) / (100 + taxe_amount_given);
                        const taxe_amount_calc_divide = taxe_amount_calc;
                        taxe_amount += round_pr(taxe_amount_calc_divide, this.pos.currency.rounding);
                    }

                }
            }


            if(taxe_id && this.order.orderlines[0] == this){
                taxdetail[taxe_id] = {
                        amount: taxe_amount,
                        base: prix_base,
                    }
                taxtotal += taxe_amount
            }


            return {
                "priceWithTax": all_taxes.total_included,
                "priceWithoutTax": all_taxes.total_excluded,
                "priceWithTaxBeforeDiscount": all_taxes_before_discount.total_included,
                "priceWithoutTaxBeforeDiscount": all_taxes_before_discount.total_excluded,
                "tax": taxtotal,
                "taxDetails": taxdetail,
                "tax_percentages": product_taxes.map((tax) => tax.amount),
            };

        }
    }
    Registries.Model.extend(Orderline, OrderlineStampDuties);
    return {Orderline, Payment};
});