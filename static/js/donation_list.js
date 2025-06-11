window.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchbar');
    if (searchInput) {
        searchInput.setAttribute("placeholder", "Busque pela doação ou doador...")
        searchInput.classList.add("w-100")
        const label = document.createElement('label');
        label.setAttribute('for', 'searchbar-q');
        label.textContent = 'Busca';
        label.classList.add('form-label');

        // Força quebra de linha com CSS
        label.style.display = 'block';
        label.style.marginBottom = '0.25rem';

        // Ajusta id do input
        searchInput.id = 'searchbar-q';

        const formGroup = searchInput.closest('.form-group');
        if (formGroup) {

            const wrapper = document.createElement('div');
            wrapper.style.display = 'flex';
            wrapper.style.flexDirection = 'column';
            wrapper.appendChild(label);
            wrapper.appendChild(searchInput.cloneNode(true)); // clona o input

            searchInput.replaceWith(wrapper);
        }

        // Mover o botão para uma nova linha se estiver no mesmo grupo
        const button = formGroup.querySelector('button[type="submit"]');
        if (button) {
            const buttonGroup = document.createElement('div');
            buttonGroup.className = 'form-group mt-2';
            buttonGroup.appendChild(button);
            formGroup.parentElement.insertBefore(buttonGroup, formGroup.nextSibling);
        }

        // Adiciona 'mt-4' ao botão de submit para alinhar verticalmente
        const buttonGroup = document.getElementById('search_group');
        const submitBtn = buttonGroup?.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.classList.add('mt-4');
        }
    }
});
