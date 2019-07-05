const post = (url, data) => {
    if (!url.endsWith('/'))
        url += '/'
    return $.ajax({
        type: "POST",
        url: url,
        data: data,
        dataType: "json",
        success: function (response) {
            return response
        },
        error: function(err) {
            return err;
        }
    });
}

$('.fa-heart').click(function(e) {
    const url = $(this).attr('url');
    let resp = post(url, {'id': $(this).parent().parent().parent().attr('movie-id')});
    $(this).toggleClass('active');
})

$('.fa-star').click(function (e) { 
    e.preventDefault();
    $(this).siblings('.form-control').toggleClass('d-none');
});

$('.option').click(function (e) { 
    e.preventDefault();
    if ($(this).hasClass('.active'))
        return;
    $('#'+$('.option.active').attr('data-id')).addClass('d-none');
    $('.option.active').removeClass('active');
    $(this).addClass('active');
    $('#'+$(this).attr('data-id')).removeClass('d-none');
});

$('.fa-star').click(function() {
    let rating = $(this).attr('rating');
    if (rating === undefined)
        return
    $(this).parent().parent().siblings('.rating-modal').find('.rating i').each(function (index, el) { 
        if (el.getAttribute('rating') <= rating - 1)
            el.classList.add('active')
        else
            el.classList.remove('active');
    });
})

$('.fa-bookmark').click(function() {
    let title = $(this).parent().parent().siblings('.watchlist').find('#watchlisttitle');
    title.empty();
    switch ($(this).attr('action')) {
        case 'watched':
            title.html('Already watched');
            break;
        case 'watch-later':
            title.html('Waiting to be watched');
            break;
        case 'remove':
            title.html('Not on watchlist');
            break;
    }
})

$('.rating i').click(function() {
    let rating = $(this).attr('rating');
    $(this).addClass('active');
    $(this).siblings('.rating i').each(function (index, el) { 
         if (el.getAttribute('rating') <= rating)
            el.classList.add('active')
        else
            el.classList.remove('active');
    });
})

$('.save-rating').click(function() {
    const data = {
        'rating': $(this).parent().siblings('.modal-body').find('.rating i.active').length,
        'movie_id': $(this).parent().parent().parent().parent().parent().attr('movie-id'),
        'movie_name': $(this).parent().parent().parent().parent().parent().attr('movie-name'),
    }
    let resp = post($(this).attr('url'), data)
    $(this).parent().parent().parent().parent().siblings('.utilities').find('.fa-star').addClass('active').attr('rating', data.rating);
})

$('.watchlist .btn').click(function() {
    const data = {
        'action': $(this).attr('data-action'),
        'movie_id': $(this).parent().parent().parent().parent().parent().attr('movie-id')
    }
    let resp = post($(this).attr('url'), data)
    data.action !== 'remove' ? $(this).parent().parent().parent().parent().siblings('.utilities').find('.fa-bookmark').addClass('active').attr('action', data.action) : 
    $(this).parent().parent().parent().parent().siblings('.utilities').find('.fa-bookmark').removeClass('active').attr('action', data.action);
});