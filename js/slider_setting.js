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
        range: true, min: 1, max: 9,
        values: [ 2, 4 ],
        create: function() {
            var value  = "";
            if (input_from.val() === "") { value = $(this).slider("values",0); }
            else { value = input_from.val(); }
            input_from.val(value);
            handle_from.text(get_handle_name(value));
            $(this).slider('values', 0, value); 

            if (input_to.val() === "") { value = $(this).slider("values",1); }
            else { value = input_to.val(); }
            input_to.val(value);
            handle_to.text(get_handle_name(value));
            $(this).slider('values', 1, value); 
        },
        slide: function(event, ui) {
            input_from.val(ui.values[0]);
            handle_from.text(get_handle_name(ui.values[0]));

            input_to.val(ui.values[1]);
            handle_to.text(get_handle_name(ui.values[1]));
        }
    });
});
