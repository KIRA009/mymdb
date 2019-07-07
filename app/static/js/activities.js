const user = JSON.parse($('#user').html()).user;
$('#user').remove();
$('#toggle').click(function() {
    $.post('/app/activities/', () => {
        $(this).toggleClass('toggled');
    })
})

$('.fa-copy').click(function() {
    if ($(this).hasClass('copied'))
        return
    let input = document.createElement('input');
    input.value = window.location.host + '/app/activities/' + user;
    document.body.append(input);
    input.select();
    document.execCommand('copy');
    document.body.removeChild(input);
    $(this).addClass('copied');
    setTimeout(() => $(this).removeClass('copied'), 2000);
})