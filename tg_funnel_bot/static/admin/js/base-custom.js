$(() => {
    $('.model-telegrambotclientmodel .changelink').hide()

    $('.model-botmessagessettingsmodel > td > .addlink').text('создать нового бота')
    $('.model-botmessagessettingsmodel .changelink').text('изменить настройки вопросов бота')

    $('#logout-form button[type="submit"]').text('выйти')
    $('#login-form input[type="submit"]').val('войти')

    $('.deletelink').text('удалить')
    $('input[name="_addanother"]').hide()
    $('input[name="_continue"]').val('Сохранить и продолжить редактирование')
    $('input[name="_save"]').val('Сохранить')
})