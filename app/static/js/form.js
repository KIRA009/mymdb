$('input').focus(function (e) { 
    e.preventDefault();
    $(this).parent().addClass('focus');
});
$('input').blur(function (e) { 
    e.preventDefault();
    $(this).parent().removeClass('focus');
});