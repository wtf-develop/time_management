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

function drawCalendar(events) {
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
        //defaultDate: '2020-05-12',
        //navLinks: true, // can click day/week names to navigate views
        editable: false,
        eventLimit: true, // allow "more" link when too many events
        events: events
    });

    calendar.render();
    //$('.feather-arrow-left').attr("data-feather", "arrow-left");
    //$('.feather-arrow-right').attr("data-feather", "arrow-right");
    $('.fc-button-primary').addClass('btn-dark');
    //feather.replace();

}