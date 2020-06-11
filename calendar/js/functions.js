var calendarEl;
var calendar;

function buildWebUI() {
    J2H.getJSON('api/get_month_plan.py?devid=' + getDevId(), function(json) {
        if (isGoodResponse(json)) {
            $('#content').html(J2H.process('page_structure', json))
            drawCalendar();
        }
    })
}

function drawCalendar() {
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
        defaultDate: '2020-05-12',
        //navLinks: true, // can click day/week names to navigate views
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        events: [{
                title: 'All Day Event',
                start: '2020-05-01',
            },
            {
                title: 'Long Event',
                start: '2020-05-07',
                end: '2020-05-10'
            },
            {
                groupId: 999,
                title: 'Repeating Event',
                start: '2020-05-09T16:00:00'
            },
            {
                groupId: 999,
                title: 'Repeating Event',
                start: '2020-05-16T16:00:00'
            },
            {
                title: 'Conference',
                start: '2020-05-11',
                end: '2020-05-13'
            },
            {
                title: 'Meeting',
                start: '2020-05-12T10:30:00',
                end: '2020-05-12T12:30:00'
            },
            {
                title: 'Lunch',
                start: '2020-05-12T12:00:00'
            },
            {
                title: 'Meeting',
                start: '2020-05-12T14:30:00'
            },
            {
                title: 'Happy Hour',
                start: '2020-05-12T17:30:00'
            },
            {
                title: 'Dinner',
                start: '2020-05-12T20:00:00'
            },
            {
                title: 'Birthday Party',
                start: '2020-05-13T07:00:00'
            },
            {
                title: 'Click for Google',
                url: 'http://google.com/',
                start: '2020-05-28'
            }
        ]
    });

    calendar.render();
    //$('.feather-arrow-left').attr("data-feather", "arrow-left");
    //$('.feather-arrow-right').attr("data-feather", "arrow-right");
    $('.fc-button-primary').addClass('btn-dark');
    //feather.replace();

}