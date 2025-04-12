var script = document.createElement('script');
script.src = 'https://unpkg.com/hotkeys-js/dist/hotkeys.min.js';
script.onload = function () {
    if (typeof hotkeys === 'undefined') return;

    hotkeys('f10,f11,f12,f9', function (event, handler) {
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
            case 'f9':
                var deleteLink = document.querySelector('a.form-control[href$="/delete/"]');
                if (deleteLink) window.location.href = deleteLink.href;
                break;
        }
    });
};
document.head.appendChild(script);
