/** @odoo-module **/

import { useRef, onMounted, useState, onWillDestroy } from "@odoo/owl";

export function useAutofocus(name){
    const input = useRef(name);
    onMounted(() => input.el && input.el.focus());
}

export function useMouse(){
    const position = useState({x:0, y:0});

    function update(e){
        position.x = e.clientX;
        position.y = e.clientY;
    }
    window.addEventListener('mousemove', update);
    onWillDestroy(() => window.removeEventListener('mousemove', update));
    return position;
}