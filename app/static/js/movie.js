const movie_json = JSON.parse($('#movie-json').html());
$('#movie-json').remove();

$('.navbar-toggler').html('Movie');

$('.fa-youtube').click(function() {
    window.open('https://www.youtube.com/watch?v=' + $(this).attr('data-id'), '_blank').focus();
})

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

$('.fa-star').click(function() {
    let rating = $('.fa-star').attr('rating');
    if (rating === undefined)
        return
    $('.rating i').each(function (index, el) { 
        if (el.getAttribute('rating') <= rating - 1)
            el.classList.add('active')
        else
            el.classList.remove('active');
    });
})

$('.fa-heart').click(function(e) {
    const url = $(this).attr('url');
    let resp = post(url, movie_json);
    $(this).toggleClass('active');
})

$('.fa-bookmark').click(function() {
    let title = $('#watchlisttitle');
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
    $('.rating i').each(function (index, el) { 
         if (el.getAttribute('rating') <= rating)
            el.classList.add('active')
        else
            el.classList.remove('active');
    });
})

$('.save-rating').click(function() {
    const data = {
        'rating': $('.rating i.active').length,
        'movie_id': movie_json.id,
        'movie_name': movie_json.name
    }
    let resp = post($(this).attr('url'), data)
    $('.utility .fa-star').attr('rating', data.rating);
    $('.utility .fa-star').addClass('active');
})

$('#watchlist .btn').click(function() {
    const data = {
        'action': $(this).attr('data-action'),
        'movie_id': movie_json.id,
    }
    let resp = post($(this).attr('url'), data)
    $('.utility .fa-bookmark').attr('action', data.action);
    data.action !== 'remove' ? $('.utility .fa-bookmark').addClass('active') : $('.utility .fa-bookmark').removeClass('active')
});