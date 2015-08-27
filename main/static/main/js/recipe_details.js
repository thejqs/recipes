
var scale_servings_element = $('#scale-servings')
var base_servings = parseFloat(scale_servings_element.text())

// scale_servings_element.html('')

$('#scale-servings').spinner({
    min: 0,
})

$('.ui-spinner-button').click(function() {
    $(this).siblings('input').change()
})

$('#scale-servings').change(function() {
    var things = $('.ingredient-quantity')
    things.each(function() {
        var value = 
        console.log(this.innerHTML)
    })
})

