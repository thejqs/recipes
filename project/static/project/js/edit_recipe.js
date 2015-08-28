'use strict';
loadRecipe();

function loadRecipe(){
    var id = $('#edit-recipe-form').attr('recipe-id');

    $.get('/recipe/' + id + '/json/', function(data){
        console.log
        var name = data[0].fields.name
        var instructions = data[0].fields.instructions
        var notes = data[0].fields.notes
        var source = data[0].fields.source
        var servings = data[0].fields.servings
        var rating = data[0].fields.rating
        var meal = data[0].fields.meal
        var difficulty = data[0].fields.difficulty

        $('#edit-recipe-form input[name="name"]').val(name);
        $('#edit-recipe-form input[name="instructions"]').val(instructions);
        $('#edit-recipe-form input[name="notes"]').val(notes);
        $('#edit-recipe-form input[name="source"]').val(source);
        $('#edit-recipe-form input[name="servings"]').val(servings);
        $('#edit-recipe-form select[name="rating"]').val(rating);
        $('#edit-recipe-form select[name="meal"]').val(meal);
        $('#edit-recipe-form select[name="difficulty"]').val(difficulty);
    })
}