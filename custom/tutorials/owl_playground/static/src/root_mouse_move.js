/** @odoo-module **/
import { Component } from '@odoo/owl'
import { useMouse } from './utils';

export class RootMouseMove extends Component{
    position = useMouse();
}
RootMouseMove.template = "owl_playground.root_mouse_move";