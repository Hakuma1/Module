odoo.define('kzm_instance_creation_portal.fullcalendar_integration', function (require) {
    "use strict";

    const publicWidget = require('web.public.widget');
    const time = require('web.time');
    const translation = require('web.translation');
    const _t = translation._t;

    publicWidget.registry.FullCalendarWidget = publicWidget.Widget.extend({
        selector: '#calendar',
        jsLibs: [
            '/web/static/lib/fullcalendar/core/main.js',
            '/web/static/lib/fullcalendar/core/locales-all.js',
            '/web/static/lib/fullcalendar/interaction/main.js',
            '/web/static/lib/fullcalendar/moment/main.js',
            '/web/static/lib/fullcalendar/daygrid/main.js',
            '/web/static/lib/fullcalendar/timegrid/main.js',
            '/web/static/lib/fullcalendar/list/main.js'
        ],
        cssLibs: [
            '/web/static/lib/fullcalendar/core/main.css',
            '/web/static/lib/fullcalendar/daygrid/main.css',
            '/web/static/lib/fullcalendar/timegrid/main.css',
            '/web/static/lib/fullcalendar/list/main.css'
        ],
        start: function () {
            this._super.apply(this, arguments);
            console.log("this", this);
            console.log("arguments", arguments);
            this.start_date = moment($('.start_date').attr('value')).toDate();
            console.log("$('.events').attr('value')", $('.events').attr('value'))
            this.events_data = JSON.parse($('.events').attr('value'));
            console.log("events_data", this.events_data)
            console.log("start_date", this.start_date)
            this.renderCalendar();
        },
        init: function (parent, options) {
            this._super.apply(this, arguments);
        },
        renderCalendar: function () {
            this.calendar = new FullCalendar.Calendar($("#calendar")[0], {
                plugins: [ 'interaction', 'dayGrid', 'timeGrid', 'list' ],
                defaultView: 'dayGridMonth',
                defaultDate: this.start_date,
                header: {
                  left: 'prev,next today',
                  center: 'title',
                  right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
                },
                events: this.events_data,
                eventClick: this.eventFunction.bind(this),
            });
            this.calendar.render();
        },
        eventFunction: function (calEvent) {
            console.log("calEvent", calEvent)
        }
    });
    return publicWidget.registry.FullCalendarWidget;
});
