var calendarEl;
var calendar;

function buildWebUI() {
    J2H.getJSON('api/get_month_plan.py?devid=' + getDevId()+'&'+getTimezoneParameter(), function(json) {
        if (isGoodResponse(json)) {
            $('#content').html(J2H.process('page_structure', json))
            drawCalendar(json.data);
        }
    })
}

function drawCalendar(events_data) {
    calendarEl = document.getElementById('calendar');
    calendar = new FullCalendar.Calendar(calendarEl, {
        plugins: ['interaction', 'dayGrid'],
        locale: getLang(),
        //themeSystem: 'bootstrap',
        height: 'parent',
        header: {
            left: '',
            center: 'title',
            right: 'today prev,next'
        },
        defaultView: 'dayGridMonth',
        //initialView: 'dayGridMonth',
        eventDidMount: function(info) {
            var tooltip = new Tooltip(info.el, {
                title: info.event.extendedProps.description,
                placement: 'top',
                trigger: 'hover',
                container: 'body'
            });
        },
        //navLinks: true, // can click day/week names to navigate views
        editable: false,
        weekNumbers: true,
      //weekNumbersWithinDays: true,
        weekNumberCalculation: 'ISO',
        eventLimit: true, // allow "more" link when too many events
        events: events_data
    });

    calendar.render();
    //$('.feather-arrow-left').attr("data-feather", "arrow-left");
    //$('.feather-arrow-right').attr("data-feather", "arrow-right");
    $('.fc-button-primary').addClass('btn-dark');
    //feather.replace();
}