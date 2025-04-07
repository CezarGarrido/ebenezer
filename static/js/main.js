
function goBack() {
    if (window.location.hash) {
        // Estamos em um hash (#detalhes, #endereco, etc.)
        // Vamos sair do hash atual redirecionando para uma página segura
    } else {
        // Se não tiver hash, volta normalmente
        window.history.back();
    }
}

// Carrega a biblioteca hotkeys.js
const script = document.createElement('script');
script.src = 'https://unpkg.com/hotkeys-js/dist/hotkeys.min.js';
script.onload = () => {
    // Define os atalhos e suas ações
    hotkeys('f10,f11,ctrl+alt+n,f9', function (event, handler) {
        console.log(handler.key)
        event.preventDefault()
        switch (handler.key) {
            case 'f10':
                document.querySelector('input[name="_save"]')?.click();
                break;
            case 'f11':
                document.querySelector('input[name="_continue"]')?.click();
                break;
            case 'f12':
                document.querySelector('input[name="_addanother"]')?.click();
                break;
            case 'f9':
                const deleteLink = document.querySelector('a.form-control[href$="/delete/"]');
                if (deleteLink) window.location.href = deleteLink.href;
                break;
        }
    });
};
document.head.appendChild(script);
