/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Card extends Component {
}
Card.template = "owl_playground.card";
Card.props = {slots: {
                    type: Object,
                    shape: {
                         title: {
                              type: Object,
                              optional:true
                              },
                         default: Object}}}