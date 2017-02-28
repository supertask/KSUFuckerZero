$(function() {
    var handle_from = $("#custom-handle-left");
    var handle_to = $("#custom-handle-right");
    var input_from = $("#slider-range input#grade-from");
    var input_to = $("#slider-range input#grade-to");

    function get_handle_name(num) {
        if(num <= 4) { return num + "回生"; }
        else { return "OB" + (num - 4) + "年目"; }
    }

    $("#slider-range" ).slider({
        range: true,
        min: 1,
        max: 9,
        values: [
            input_from.val(),
            input_to.val()
        ],
        create: function() {
            handle_from.text(get_handle_name(input_from.val()));
            handle_to.text(get_handle_name(input_to.val()));
        },
        slide: function(event, ui) {
            input_from.val(ui.values[0]);
            input_to.val(ui.values[1]);
            handle_from.text(get_handle_name(ui.values[0]));
            handle_to.text(get_handle_name(ui.values[1]));
        }
    });
});
