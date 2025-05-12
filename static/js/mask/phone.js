(function($) {
    $(document).ready(function() {

        function applyPhoneMask(element) {
            if (!element.cleave) {
                new Cleave(element, {
                    delimiters: ['(', ') ', '-', ''],
                    blocks: [0, 2, 5, 4],
                    phoneRegionCode: 'BR'
                });
            }
        }

        function maskAllPhoneFields(context) {
            $(context).find('[data-mask-phone]').each(function () {
                applyPhoneMask(this);
            });
        }

        // Aplica nos campos existentes
        maskAllPhoneFields(document);

        // Quando adicionar novo inline
        $(document).on('formset:added', function (event, $row, formsetName) {
            maskAllPhoneFields($row);
        });

        // Segurança extra
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                $(mutation.addedNodes).each(function() {
                    if (this.nodeType === 1) {
                        maskAllPhoneFields(this);
                    }
                });
            });
        });

        observer.observe(document.body, { childList: true, subtree: true });

    });
})(django.jQuery);