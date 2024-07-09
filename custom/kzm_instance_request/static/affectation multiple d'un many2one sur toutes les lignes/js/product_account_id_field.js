/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import {Many2OneField} from "@web/views/fields/many2one/many2one_field";
import { _lt } from "@web/core/l10n/translation";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { Many2XAutocompleteInapco } from "./manyautocompleteinapco";

 /**
    * Dialog called if user changes a value in the account move line.
    * The wizard will open only if
    *  (1) Account move line is 3 or more
    *  (2) First account move line is changed
    *  (3) value is the same in all other account move line
 */

export class ProductAccountField extends Many2OneField {
    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    }

    get Many2XAutocompleteProps() {
        let result =  {
            value: this.displayName,
            id: this.props.id,
            placeholder: this.props.placeholder,
            resModel: this.relation,
            autoSelect: true,
            fieldString: this.props.string,
            activeActions: this.state.activeActions,
            update: this.update,
            quickCreate: this.quickCreate,
            context: this.context,
            getDomain: this.getDomain.bind(this),
            nameCreateField: this.props.nameCreateField,
            setInputFloats: this.setFloating,
            autocomplete_container: this.autocompleteContainerRef,
            kanbanViewId: this.props.kanbanViewId,
            onChangeAccount: this.onChangeAccount.bind(this),
        };
        return result;
    }


    onChangeAccount() {
        if (this.props.record.model.root.data.move_type == "in_invoice"){
            const x2mList = this.props.record.model.root.data.invoice_line_ids;
            const invoiceLines = x2mList.records.filter(line => line.data.display_type == 'product');

            if (invoiceLines.length < 3) {
                return;
            }

            const isFirstOrderLine = this.props.record.data.id === invoiceLines[0].data.id;
            if (isFirstOrderLine && sameValue(invoiceLines)) {
            this.dialogService.add(ConfirmationDialog, {
                body: _lt("Do you want to apply this value to all lines ?"),
                confirm: () => {
                    const commands = invoiceLines.slice(1).map((line) => {
                        return {
                            operation: "UPDATE",
                            record: line,
                            data: {['account_id_set_from_js']: +this.props.value[0]}
                        }
                    });
                    x2mList.applyCommands('invoice_line_ids', commands);

                },
            });
        }
        }
    }
}

export function sameValue(invoiceLines) {
    const compareValue = +invoiceLines[1].data.account_id[0];
    return invoiceLines.slice(1).every(line => +line.data.account_id[0] === compareValue);
}


ProductAccountField.components = { ConfirmationDialog, Many2XAutocompleteInapco };
ProductAccountField.template = "inapco_base.ProductAccountField";
ProductAccountField.displayName = _lt("Account");

registry.category("fields").add("aml_account_inapco_base", ProductAccountField)
