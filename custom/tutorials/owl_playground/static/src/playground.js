/** @odoo-module **/

import { Counter } from "./counter/counter";
import { TodoList } from "./todo_list/todo_list";
import { Card } from "./Card/card";
import { Component, useState } from "@odoo/owl";

export class Playground extends Counter {
    static template = "owl_playground.playground";
    static components = {Counter, TodoList, Card};
}