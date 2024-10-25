/** @odoo-module **/

import { Component, useSubEnv, onWillStart} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { getDefaultConfig } from "@web/views/view";
import { useService } from "@web/core/utils/hooks";
import { Domain } from "@web/core/domain";
import { Card } from "./card/card";
import { loadJS } from "@web/core/assets";
import { PieChart } from "./pie_chart/pie_chart";
import { sprintf } from "@web/core/utils/strings";


class AwesomeDashboard extends Component {
    setup(){
        useSubEnv({
                config: {
                    ...getDefaultConfig(),
                    ...this.env.config,
                },
        });
        this.cardKeys = {average_quantity: this.env._t("Average amount of t-shirt by order this month"),
            average_time: this.env._t(
                "Average time for an order to go from 'new' to 'sent' or 'cancelled'"
            ),
            nb_cancelled_orders: this.env._t("Number of cancelled orders this month"),
            nb_new_orders: this.env._t("Number of new orders this month"),
            total_amount: this.env._t("Total amount of new orders this month"),
                         }
        this.action = useService("action");
        this.tshirtService = useService("tshirtService");
        this.display = {
            controlPanel: { "top-right": false, "bottom-right": false },
        };
        onWillStart(async () => {
                                this.statistics = await this.tshirtService.loadStatistics();});
    }


    openCustomerView(ev){
        this.action.doAction("base.action_partner_form");
    }

    openOrders(title, domain) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: title,
            res_model: "awesome_tshirt.order",
            domain: new Domain(domain).toList(),
            views: [
                [false, "list"],
                [false, "form"]
            ]
        });
    }

    openLast7DaysOrders(ev){
        const domain =
            "[('create_date','>=', (context_today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'))]";
        this.openOrders("Last 7 days orders", domain);
    }

    openLast7DaysCancelledOrders() {
        const domain =
            "[('create_date','>=', (context_today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')), ('state','=', 'cancelled')]";
        this.openOrders("Last 7 days cancelled orders", domain);
    }
}

AwesomeDashboard.components = { Layout, Card, PieChart };
AwesomeDashboard.template = "awesome_tshirt.clientaction";

registry.category("actions").add("awesome_tshirt.dashboard", AwesomeDashboard);
