'user strict';


// This adds more form entry fields for the ingredients onto the
// create-recipe form. Then it increments the form count so that
// the view accepts the new total number of forms for processing
$(document).ready(function(){
    $('.add-ingredient').click(function(e){
        e.preventDefault();
        var count = $('#items-form-container').children().length;
        // gets the template in script tags at the bottom of the page
        var tmplMarkup = $('#item-template').html();
        // replaces the prefix value with the correct form number
        var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
        $('div#items-form-container').append(compiledTmpl);

        // updates the total form count
        var forms = parseInt($('#id_form-TOTAL_FORMS').val(), 10);
        forms += 1;
        $('#id_form-TOTAL_FORMS').val(forms);
    })
})

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

$('#exclude-btn').click(function(e){
    e.preventDefault();
    var id = $('#exclude-section').attr('recipe-id')
    $.ajax({
        url: '/recipe/' + id + '/',
        method: 'PUT',
        beforeSend: function(xhr){
            xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"))
        },
        success: function(){
            $('#exclude-section').append('<p><center>This has recipe been excluded from future searches</center></p>')
        }
    })
})

$('.filters').on('change', '#exclude-results', function(e){
    e.preventDefault();
    if ($(this).prop("checked")){
        $('.exclude-recipe').hide();
    } else{
        $('.exclude-recipe').show();
    }
})