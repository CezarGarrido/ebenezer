
(function($) {
    $(document).ready(function() {
        
        // Sobrescreve a função showAdminPopup para centralizar as janelas
        const originalShowAdminPopup = window.showAdminPopup;
        
        window.showAdminPopup = function(triggeringLink, name_regexp, add_popup) {
            const name = window.addPopupIndex(triggeringLink.id.replace(name_regexp, ''));
            const href = new URL(triggeringLink.href);
            if (add_popup) {
                href.searchParams.set('_popup', 1);
            }
            
            const width = 800;
            const height = 500;
            const left = (screen.width - width) / 2;
            const top = (screen.height - height) / 2;
            
            const win = window.open(
                href, 
                name, 
                `height=${height},width=${width},resizable=yes,scrollbars=yes,top=${top},left=${left}`
            );
            
            window.relatedWindows.push(win);
            win.focus();
            return false;
        };
    });
})(django.jQuery);


// Carrega a biblioteca hotkeys.js
const script = document.createElement('script');
script.src = 'https://unpkg.com/hotkeys-js/dist/hotkeys.min.js';
script.onload = () => {
    // Define os atalhos e suas ações
    hotkeys('ctrl+alt+s,ctrl+alt+e,ctrl+alt+n,ctrl+alt+d', function (event, handler) {
        switch (handler.key) {
            case 'ctrl+alt+s':
                document.querySelector('input[name="_save"]')?.click();
                break;
            case 'ctrl+alt+e':
                document.querySelector('input[name="_continue"]')?.click();
                break;
            case 'ctrl+alt+n':
                document.querySelector('input[name="_addanother"]')?.click();
                break;
            case 'ctrl+alt+d':
                const deleteLink = document.querySelector('a.deletelink');
                if (deleteLink) window.location.href = deleteLink.href;
                break;
        }
    });

    // Cria e injeta o painel com as hotkeys
    const infoBox = document.createElement('div');
    infoBox.innerHTML = `
        <div style="
            position: fixed;
            bottom: 4rem;
            right: 1rem;
            background: #f9f9f9;
            border: 1px solid #ccc;
            padding: 1rem;
            font-size: 14px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            z-index: 9999;
            max-width: 250px;
            border-radius: 4px;
        ">
            <strong>Atalhos disponíveis:</strong>
            <ul style="margin-top: 0.5rem; padding-left: 1.2rem;">
                <li style="margin-bottom: 0.4rem;"><kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>S</kbd>: Salvar</li>
                <li style="margin-bottom: 0.4rem;"><kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>E</kbd>: Salvar e continuar editando</li>
                <li style="margin-bottom: 0.4rem;"><kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>N</kbd>: Salvar e adicionar outro</li>
                <li><kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>D</kbd>: Excluir</li>
            </ul>

        </div>
    `;
    document.body.appendChild(infoBox);
};
document.head.appendChild(script);