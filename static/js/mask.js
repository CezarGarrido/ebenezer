(function ($) {
    $(document).ready(function () {
        $('[data-mask-cnae]').each(function () {
            var maskPattern = $(this).attr('data-mask-cnae');
            $(this).mask(maskPattern);
        });

        // Máscara para CPF (000.000.000-00)
        // $('[data-mask-cpf]').mask('000.000.000-00');

        // Máscara para CNPJ (00.000.000/0000-00)
        // $('[data-mask-cnpj]').mask('00.000.000/0000-00');

        // Máscara para CEP (00000-000)
        // $('[data-mask-cep]').mask('00000-000');

        $('[data-mask-money]').mask('#.##0,00', { reverse: true });

        // Intercepta a submissão do formulário
        $('form').on('submit', function (event) {
            var amountField = $('[data-mask-money]');
            var amountValue = amountField.val();
            if (amountValue) {
                var cleanAmount = amountValue
                    .replace('R$', '')  // Remove o símbolo de moeda, se presente
                    .replace(/\./g, '') // Remove pontos
                    .replace(',', '.')   // Troca vírgulas por pontos
                    .trim();             // Remove espaços em branco
                amountField.val(cleanAmount);
            }
        });

        console.log("Máscaras aplicadas para CPF, CNPJ e CEP.");
    });
})(django.jQuery);
