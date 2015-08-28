
// get the recipe's inherent base number of servings
var base_servings = parseFloat($('#scale-servings').val())

// initialize the "last known good value" of the spinner
var last_good_value = base_servings

// initialize the spinner widget and limit it to positive values
$('#scale-servings').spinner({
    min: 1,
})

// when a spinner button is clicked, make the input fire a change event
$('.ui-spinner-button').click(function() {
    $(this).siblings('input').change()
})

// when the input box loses focus, make the input fire a change event
$('#scale-servings').blur(function() {
    $(this).change()
})


// when the input box has a changes event
$('#scale-servings').change(function() {

    // get the nenwly updated value from the spinner
    var new_value = parseFloat($(this).val())

    // if the value is invalid, reset it to the last known good value
    if (isNaN(new_value) | new_value < 1) {
        $('#scale-servings').spinner('value', last_good_value)

    // if the value is a valid number
    } else {

        // console.log(parseFloat($(this).val()))
        var things = $('.ingredient-quantity')
        things.each(function() {
            var current_qty = parseFloat(this.innerHTML)
            var single_qty = current_qty / last_good_value
            var scaled_qty = single_qty * new_value
            $(this).html(scaled_qty)
        })

        // set the newest value as "known to be good"
        last_good_value = new_value
    }
})
