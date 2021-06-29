$(function() {
    $('.menus a').click(function() {
        var index = $(this).index()
        $('.menus a').removeClass('active');
        $(this).addClass('active');
        $('#boxs').find('.box').hide();
        $('#boxs').find('.box').eq(index).fadeIn()

    })
})