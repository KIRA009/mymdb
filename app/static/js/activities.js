$('#toggle').click(function() {
    $.post('/app/activities/', () => {
        $(this).toggleClass('toggled');
    })
})