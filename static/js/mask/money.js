(function ($) {
    $(document).ready(function () {
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
    });
})(django.jQuery);
