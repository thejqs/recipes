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
		forms += 1
		$('#id_form-TOTAL_FORMS').val(forms);
    })
})
