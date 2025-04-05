document.addEventListener("DOMContentLoaded", function () {
    function findTabLinkForPane(paneId) {
        return document.querySelector(`a.nav-link[href="#${paneId}"]`);
    }

    function toggleInlines() {
        const tipoPessoa = document.getElementById("id_person_type")?.value;
        console.log("Tipo de pessoa selecionado:", tipoPessoa);

        // Encontrar os elementos de aba via classe adicionada no `classes = [...]` do inline
        const pfPane = document.querySelector('.individual-inline-tab');
        const pjPane = document.querySelector('.legal-inline-tab');

        if (!pfPane || !pjPane) {
            console.warn("Inlines não encontrados. Verifique os nomes das classes.");
            return;
        }

        const pfPaneId = pfPane.id;
        const pjPaneId = pjPane.id;

        const pfLink = findTabLinkForPane(pfPaneId);
        const pjLink = findTabLinkForPane(pjPaneId);

        // Esconde todas as abas
        [pfLink, pjLink].forEach(link => link?.parentElement?.classList.add("d-none"));
        [pfPane, pjPane].forEach(pane => pane?.classList.remove("show", "active"));

        // Mostra a aba correspondente
        if (tipoPessoa === "F") {
            pfLink?.parentElement?.classList.remove("d-none");
        } else if (tipoPessoa === "J") {
            pjLink?.parentElement?.classList.remove("d-none");
        }
    }

    toggleInlines();

    if (window.jQuery) {
        $('#id_person_type').on('select2:select', toggleInlines);
    } else {
        document.getElementById("id_person_type")?.addEventListener("change", toggleInlines);
    }
});
