var todo = {};
(function(todo, $) {

    todo.init = function(element, json) {
        jth.translate(json, ['pname']);
        element.html(jth.process('all_panels', json));
        // Adding drop function to each category of task
        /*$('.todo_content').droppable({
            classes: {
                "ui-droppable-hover": "border border-success rounded"
            },
            drop: function(event, ui) {
                var element = ui.helper;
                if ($(this).parent().attr("id") == element.parent().parent().attr("id")) return;
                var css_id = element.attr("id");
                element.attr('style', '');
                var outerhtml = $('<div>').append(element.clone()).html();
                element.remove();
                $(this).prepend(outerhtml);
                reinitDrop();
            }

        });*/

        reinitDrop();

    };

    function reinitDrop() {
/*
        if (isMobile()) {
            feather.replace();
            $('.todo_content').sortable({
                zIndex: 9999,
                delay: 300,
                revert: "invalid",
                revertDuration: 100,
                scroll: true,
                handle: '.sub-draggable'
            });
        } else {
            $('.todo_content').sortable({
                zIndex: 9999,
                delay: 0,
                revert: "invalid",
                revertDuration: 100,
                scroll: true
            });
        }*/
        $('.todo_content').disableSelection();

    }

})(todo, jQuery);