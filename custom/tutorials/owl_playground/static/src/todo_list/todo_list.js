/** @odoo-module **/

import { Component, useState, useRef } from '@odoo/owl';
import { Todo } from '../todo/todo';
import { useAutofocus } from '../utils';
import { RootMouseMove } from '../root_mouse_move';

export class TodoList extends Component{
    static components = { Todo , RootMouseMove };
    setup(){
        this.todolist = useState([]);
        this.nextId = 1;
        useAutofocus('input');
        //this.checked = this.checked.bind(this);

    }

    removeTodo(todo_id){
        const index = this.todolist.findIndex((element) => element.id == todo_id);
        if(index >= 0){
            this.todolist.splice(index, 1);
        }
    }

    toggleTodo(todo_id){
        const todo = this.todolist.find((element) => element.id == todo_id);
        if(todo){
           todo.done = !todo.done;
        }
    }

    addTodo(ev){
        if(ev.key === 'Enter'){
            const input_content = ev.target.value;
            this.todolist.push({id:this.nextId++, description: input_content, done: false});
            ev.target.value = '';
            ev.target.blur();
        }
    }
}
TodoList.template = "owl_playground.todo_list";