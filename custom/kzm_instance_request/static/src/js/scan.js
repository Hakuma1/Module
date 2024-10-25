/** @odoo-module **/

import { registry } from "@web/core/registry";
import { DeviceController } from "@iot/device_controller"
import { useService } from "@web/core/utils/hooks";
import session from "web.session";
import {browser} from "@web/core/browser/browser";


function onIoTActionResult(data, params) {
    if (data.result === true) {
        params.services.notification.add("Successfully sent to printer!");
        browser.location.reload();
    } else {
        params.services.notification.add("Check if the scanner is still connected", {
            title: "Connection to scanner failed",
            type: "danger",
        });
    }
}


function onValueChange(data, env) {
    if (data.status) {
        env.services.notification.add(env._t("Scanner ") + data.status);
    }
}

function customJsFunction(params) {
    console.log("params.", params)
    let user = session.uid;
    console.log('uid', user)
    console.log("const baseUrl = `${window.location.protocol}//${window.location.host}`;", `${window.location.protocol}//${window.location.host}`)
    console.log("params.services.action.currentController.action.context.params", params.services.action.currentController.action.context.params)
    const iotDevice = new DeviceController(params.services.iot_longpolling, { iot_ip: '192.168.31.7', identifier:"usb_03f0:6105" });
    //iotDevice.addListener(data => onValueChange(data, env));
    let url = `${window.location.protocol}//${window.location.host}`;
    let the_id = params.services.action.currentController.action.context.params.id;
    let the_model = params.services.action.currentController.action.context.params.model;
    iotDevice.action({ action: "action_mc_mc", the_id: the_id, model: the_model, url: url}).then(response => {
                    console.log("data------>", response);
                    onIoTActionResult(response, params);
    }).catch(error => {
        console.error("Erreur lors de l'exécution de l'action:", error);
    });
}

registry.category("actions").add("your_custom_js_action", customJsFunction);
