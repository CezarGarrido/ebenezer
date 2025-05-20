(function () {
    function initMoneyMask($) {
        function applyMask() {
            $('[data-mask-money]').mask('#.##0,00', { reverse: true });
        }

        $(function () {
            applyMask();

            $(document).on("focus", "[data-mask-money]", function () {
                $(this).mask("#.##0,00", { reverse: true });
            });

            $('form').on('submit', function () {
                $('[data-mask-money]').each(function () {
                    const $input = $(this);
                    const valorLimpo = $input.val().replace(/\./g, '').replace(',', '.').trim();
                    $input.unmask();
                    $input.val(valorLimpo);
                });
            });
        });
    }

    if (typeof django !== 'undefined' && django.jQuery) {
        initMoneyMask(django.jQuery);
    } else {
        // Espera o DOM carregar e tenta de novo
        document.addEventListener('DOMContentLoaded', function () {
            if (typeof django !== 'undefined' && django.jQuery) {
                initMoneyMask(django.jQuery);
            } else {
                console.error("django.jQuery não foi carregado.");
            }
        });
    }
})();
