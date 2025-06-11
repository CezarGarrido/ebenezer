const saveInput = document.querySelector("input[name=_save]");
if (saveInput) {
    saveInput.value = "[F10] Salvar";
}

var deleteLink = document.querySelector('a.form-control[href$="/delete/"]');
if (deleteLink) deleteLink.innerText = "[F6] Excluir"


hotkeys('f6,f10,f11,f12,f9,esc', function (event, handler) {
    event.preventDefault();
    switch (handler.key) {
        case 'f10':
            var saveInput = document.querySelector('input[name="_save"]');
            if (saveInput) saveInput.click();
            break;
        case 'f11':
            var continueInput = document.querySelector('input[name="_continue"]');
            if (continueInput) continueInput.click();
            break;
        case 'f12':
            var addAnotherInput = document.querySelector('input[name="_addanother"]');
            if (addAnotherInput) addAnotherInput.click();
            break;
        case 'f6':
            var deleteLink = document.querySelector('a.form-control[href$="/delete/"]');
            if (deleteLink) window.location.href = deleteLink.href;
            break;
        case 'esc':
            window.history.back();
    }
});

const links = document.querySelectorAll('a.dropdown-item.dropdown-footer');
links.forEach(link => {
    const href = link.getAttribute('href');
    if (href.startsWith('/admin/auth/user/') && href.endsWith('/change/')) {
        // Cria o ícone
        const icon = document.createElement("i");
        icon.className = "fas fa-user mr-3";
        // Limpa o conteúdo atual
        link.textContent = "";
        // Adiciona ícone e novo texto
        link.appendChild(icon);
        link.appendChild(document.createTextNode("Ver Perfil"));
    }
});


(function ($) {
    $(document).ready(function () {
        $('.admin-autocomplete').each(function () {
            const $select = $(this);
            let originalVal = null;
            $select.on('select2:opening', function () {
                originalVal = $select.val();
            });

            $select.on('select2:open', function () {
                document.querySelector('.select2-search__field').focus();

                if (originalVal) {
                    // Oculta o texto renderizado no input
                    $('.select2-selection__rendered').text('');
                    // Força a lista a considerar o item ainda como selecionado
                    // Isso exige um pequeno delay para garantir que a lista carregou
                    setTimeout(() => {
                        $(`.select2-results__option[aria-selected=true]`).removeAttr('aria-selected');
                        $(`.select2-results__option[id$="-${originalVal}"]`).attr('aria-selected', 'true');
                    }, 0);
                }
            });
        });
    });
})(django.jQuery);
