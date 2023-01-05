const replaceElementText = (selector, text, new_text) => {
    $(selector).text($(selector).text().replace(text, new_text))
}

$(() => {
    $('.model-telegrambotclientmodel .changelink').hide()

    $('.model-botmessagessettingsmodel > td > .addlink').text('создать нового бота')
    $('.model-botmessagessettingsmodel .changelink').text('изменить настройки вопросов бота')

    $('#logout-form button[type="submit"]').text('выйти')
    $('#login-form input[type="submit"]').val('войти')
    replaceElementText('#user-tools', 'Welcome', 'Добро пожаловать')
    replaceElementText('#user-tools', 'Change password', 'Изменить пароль')

    $('.deletelink').text('удалить')
    $('input[name="_addanother"]').hide()
    $('input[name="_continue"]').val('Сохранить и продолжить редактирование')
    $('input[name="_save"]').val('Сохранить')

    replaceElementText('#content > h1', 'Select', 'Выбрать')
    replaceElementText('#content > h1', 'to change', 'для изменений')
    replaceElementText('#content > h1', 'Change', 'Изменить')
    if ($('.actions > label').length) {
        document.querySelector('.actions > label').firstChild.textContent = 'Действие:'
    }
    $('#changelist-filter > h2').text('Фильтрация')
    replaceElementText('#changelist-filter summary', 'By ', '')
    $('#nav-filter').attr('placeholder', 'Начать писать для фильтрации...')
    $('.breadcrumbs > a:eq(0)').text('Домашняя страница')
    $('.historylink').hide()
    $('#recent-actions-module').hide()
})