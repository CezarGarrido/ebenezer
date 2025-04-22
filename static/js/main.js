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