$(window).on('load', function(e) {
    let page_num = window.location.pathname.slice(10,);
    page_num = (page_num === '') ? 1 : page_num
    if (page_num > 10)
        window.location = '/app/home/10'
    $('.pages span:nth-child(' + page_num + ')').addClass('active');
})

$('.front').click(function () { 
    $(this).addClass('hover');
    $(this).siblings('.back').addClass('hover');
});

$('.close-book').click(function () {
    let parent = $(this).parent();
    parent.removeClass('hover');
    parent.siblings('.front').removeClass('hover');
});

$('.more').click(function() {
    window.open('/app/movie/' + $(this).attr('data-id'), '_blank').focus();
})

$('.pages span').click(function() {
    window.location = '/app/home/' + $(this).html();
})