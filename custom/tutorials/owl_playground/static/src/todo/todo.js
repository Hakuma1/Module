/** @odoo-module **/

import { Component } from '@odoo/owl';

export class Todo extends Component{
    OnClickCheck(ev){
        this.props.toggleState(this.props.id);
    }

    onRemove(ev){
        this.props.removeTodo(this.props.id);
    }
}
Todo.template = 'owl_playground.todo';
Todo.props = {id:{type:Number}, description:{type:String}, done:{type:Boolean}, toggleState:{type: Function}, removeTodo:{type: Function}};
