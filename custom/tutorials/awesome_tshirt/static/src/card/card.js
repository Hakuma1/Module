/** @odoo-module **/
import { Component } from "@odoo/owl";

export class Card extends Component{}
Card.template = 'awesome_tshirt.card';
Card.props = {
    slots: {
         type: Object,
         shape: {
              title: {type: Object, optional:true},
              default: {type: Object, optional: true},
         }
    },
    className: {
        type: String,
        optional: true,
    },
}