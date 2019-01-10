$('.title').click(function () {

        $(this).next().stop().slideToggle();
        $(this).parent().siblings().children('.second_menu_body').slideUp();
        $(this).children().addClass('active').parent().parent().siblings().children().children().removeClass('active')
});
