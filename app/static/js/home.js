$(window).on('load', function(e) {
    let page_num = window.location.pathname.slice(10,);
    page_num = (page_num === '') ? '1/' : page_num
    page_num = page_num.slice(0, page_num.length - 1);
    if (page_num > 10)
        window.location = '/app/home/10'
    // console.log('.pages span:nth-child(' + page_num + ')');
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

$('.fa-search').click(function() {
    $('#movie-search').val('');
    $('#search-options').empty();
})

const get = (url) => {
    $('#search-options').html('Loading...');
    $.ajax({
        type: "GET",
        url: url,
        success: function (response) {
            $('#search-options').empty();
            for (var ind in response.movies) {
                let input = document.createElement('input');
                let attrs = {
                    type: 'text',
                    readonly: true,
                    class: 'form-control',
                    url: response.movies[ind][1],
                    value: response.movies[ind][0]
                }
                input.onclick = () => window.open('/app/movie/' + attrs.url, '_blank').focus();
                for (var key in attrs)
                    input.setAttribute(key, attrs[key]);
                $('#search-options').append(input);
            }
        }
    });
}

document.getElementById('movie-search').oninput = function (e) { 
    e.preventDefault();
    if (e.target.value === '')
        return;
    get("/app/search/" + e.target.value);
}