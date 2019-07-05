$(window).on('load', function(e) {
    if (window.location.pathname.startsWith('/app/home'))
        $('a[href="/app/home/1"]').addClass('active');
    else
        $('a[href="' + window.location.pathname +'"]').addClass('active');
})