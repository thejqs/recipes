
// get some basic values from the page on first load
var last_good_value = parseFloat($('#scale-servings').val())
var recipe_id = parseFloat($('#recipe-id').text())

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

function notWhole(n) {
   if (n % 1 == 0){
    return false
   }else{
    return true
   }
}

// when the input box has a "changes" event
$('#scale-servings').change(function() {

    // get the newly updated value from the spinner
    var new_value = parseFloat($(this).val())

    // if the value is invalid, reset it to the last known good value
    if (isNaN(new_value) || new_value < 1 || notWhole(new_value)) {
        $('#scale-servings').spinner('value', last_good_value)

    // if the value is a valid number
    } else {

        $.ajax({
        method: 'GET',
        url: '/recipe/' + recipe_id + '/scale/' + new_value + '/',
        beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
        },
        success: function(data) {
            
            var final_html = ''
            $.each(data, function() {
                var quantities_html = ''
                $.each(this.quantities, function() {
                    quantities_html += this.quantity +' '+ this.unit+ ', '
                })
                quantities_html = quantities_html.slice(0,-2)
                final_html += "<p class='ingredient-row complete-ingredient'>"+
                                quantities_html + ' '+ this.name +
                                "</p>"
                
            })
            $('#all-ingredients').html(final_html)

        },
    })

        // console.log(parseFloat($(this).val()))
        // var things = $('.ingredient-quantity')
        // things.each(function() {
        //     var current_qty = parseFloat(this.innerHTML)
        //     var single_qty = current_qty / last_good_value
        //     var scaled_qty = single_qty * new_value
        //     $(this).html(scaled_qty)
        // })

        // set the newest value as "known to be good"
        last_good_value = new_value
    }
})

// when the button to log an event is pressed
$('.btn-log-event').click(function() {
    $.ajax({
        method: 'POST',
        url: '/recipe/' + recipe_id + '/log/',
        beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
        },
        success: function(data) {
            // <abbr class="timeago" title="{{ event.created|date:'c' }}">{{ event.created|date:'DATE_FORMAT' }}</abbr>
            var ul_last_cooked = $('.ul-last-cooked')
            var time_elem = '<li><abbr class="timeago" title="' + data.iso_date_time + '">' + data.nice_date_time + '</abbr></li>'
            ul_last_cooked.prepend(time_elem)
            $(".ul-last-cooked abbr.timeago").timeago()
        },
    })
})


/**
 * Helper fuction for POSTing with ajax
 */
function getCookie(name) {
    var value = '; ' + document.cookie
    var parts = value.split('; ' + name + '=')
    if (parts.length == 2) return parts.pop().split(";").shift()
}
