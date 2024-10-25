odoo.define('stamp_duties.PaymentScreenPaymentLinesStampDuties', function (require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const PaymentScreenPaymentLines = require('point_of_sale.PaymentScreenPaymentLines');
    var utils = require('web.utils');

    var round_pr = utils.round_precision;
    var round_di = utils.round_decimals;

    const PaymentScreenPaymentLinesStampDuties = (PaymentScreenPaymentLines) => class PaymentScreenPaymentLinesStampDuties extends PaymentScreenPaymentLines {
        formatLineAmountStampDuties(paymentline) {
            return this.env.pos.format_currency_no_symbol(paymentline.get_amount_before_stamp_duties());
        }

        formatLineStampDuties(paymentline){
            return paymentline.get_stamp_duties();
        }

    }
    Registries.Component.extend(PaymentScreenPaymentLines, PaymentScreenPaymentLinesStampDuties);
    return PaymentScreenPaymentLines;
});