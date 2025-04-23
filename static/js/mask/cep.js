(function ($) {
    function applyCepMask() {
        $('[data-mask-cep]').mask('00000-000');
    }

    function getPrefixFromName(nameAttr) {
        // Extrai o prefixo, ex: "addresses-0-" de "addresses-0-postal_code"
        const match = nameAttr.match(/^(.*-)[^-]+$/);
        return match ? match[1] : '';
    }

    function preencherEnderecoComPrefixo(prefixo, dados) {
        $(`[name="${prefixo}street"]`).val(dados.logradouro || '');
        $(`[name="${prefixo}neighborhood"]`).val(dados.bairro || '');
        $(`[name="${prefixo}city"]`).val(dados.localidade || '');        
        jQuery(`[name="${prefixo}state"]`).val(dados.uf || '').trigger('change').trigger('select2:select');
    }

    function buscarEnderecoPorCep(input, event) {
        event.preventDefault();

        const cep = $(input).val().replace(/\D/g, '');
        if (cep.length !== 8) return;

        const nameAttr = $(input).attr('name');
        const prefixo = getPrefixFromName(nameAttr);

        $.ajax({
            url: `https://viacep.com.br/ws/${cep}/json/`,
            method: 'GET',
            dataType: 'json',
            success: function (data) {
                if (data.erro != "true") {
                    preencherEnderecoComPrefixo(prefixo, data);
                }
            },
            error: function (xhr, status, error) {
                console.warn("Erro ao buscar CEP:", error);
            }
        });
    }

    $(document).ready(function () {
        applyCepMask();

        $(document).on("focus", "[data-mask-cep]", function () {
            $(this).mask("00000-000", { reverse: true });
        });

        $(document).on("change", "[data-mask-cep]", function (event) {
            buscarEnderecoPorCep(this, event);
        });
    });
})(django.jQuery);
