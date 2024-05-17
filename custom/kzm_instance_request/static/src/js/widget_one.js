/** @odoo-module **/
const {xml, Component} = owl;
import { standardFieldProps } from "@web/views/fields/standard_field_props";
// Import the registry
import {registry} from "@web/core/registry";

export class WidgetOne extends Component {
    setup() {
        // This setup is useless here because we don't do anything
        // But this is where you will use Hooks
        super.setup();
        console.log("C'est le premier test!!");

    }
}

WidgetOne.template = 'kzm_instance_request.WidgetOne';
WidgetOne.props = {
    ...standardFieldProps,
};
console.log("Props: ", WidgetOne.props);
// Add the field to the correct category
registry.category("fields").add("widget_one", WidgetOne);