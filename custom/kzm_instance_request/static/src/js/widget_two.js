/** @odoo-module **/
const { useState, Component } = owl;
const { xml } = owl;
console.log("Ceci est le widget deux!!");

class WidgetTwo extends Component {

    setup() {
        this.state = useState({ value: 1 });
    }

    increment() {
        this.state.value++;
    }
}
MyComponent.template = 'kzm_instance_request.WidgetTwo';
