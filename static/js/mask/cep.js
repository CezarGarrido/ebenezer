(function ($) {
    // Função para aplicar a máscara a todos os campos com data-mask-cep
    function applyCepMask() {
        $('[data-mask-cep]').mask('00000-000');
    }

    // Aplica a máscara quando o documento está pronto
    $(document).ready(function () {
        applyCepMask();

        $(document).on("focus", "[data-mask-cep]", function () {
            $(this).mask("00000-000", {
                reverse: true
            });
        });

    });
})(django.jQuery);