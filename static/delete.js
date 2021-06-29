function my_recipes_delete_event(recipe_id){
    $.ajax({
        type: "POST",
        url: '/profile',
        data: {'operation': 'delete',
               'recipes_id': recipe_id,
               'user_id': localStorage.getItem('userId')},
        success: function (result){
            $("#recipe_"+ (recipe_id).toString()).remove();
        }
    })
}