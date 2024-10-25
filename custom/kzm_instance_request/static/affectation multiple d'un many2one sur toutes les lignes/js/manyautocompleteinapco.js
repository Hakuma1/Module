/** @odoo-module **/

import { Many2XAutocomplete } from '@web/views/fields/relational_utils';
import { Many2OneField } from '@web/views/fields/many2one/many2one_field';
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { AutoCompleteInapco } from "./autocompleteinapco";


export class Many2XAutocompleteInapco extends Many2XAutocomplete {
        setup() {
            super.setup();
        }

        onSelect(option, params = {}) {
        if (option.action) {
            return option.action(params);
        }
        const record = {
            id: option.value,
            name: option.label,
        };
        this.props.update([record], params);
        this.props.onChangeAccount();
    }
}
Many2XAutocompleteInapco.template = "inapco_base.Many2XAutocompleteInapco";
Many2XAutocompleteInapco.components = { AutoCompleteInapco };