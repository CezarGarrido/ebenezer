(function ($) {
    $(document).ready(function () {

        function findTabLinkForPane(paneId) {
            return $('a.nav-link[href="#' + paneId + '"]').first();
        }
        function toggleInlines() {
            var tipoPessoa = $('#id_person_type').val();

            var $pfPane = $('.individual-inline-tab').first();
            var $pjPane = $('.legal-inline-tab').first();

            if (!$pfPane.length || !$pjPane.length) {
                return;
            }

            var pfPaneId = $pfPane.attr('id');
            var pjPaneId = $pjPane.attr('id');

            var $pfLink = findTabLinkForPane(pfPaneId);
            var $pjLink = findTabLinkForPane(pjPaneId);

            $pfLink.parent().addClass('d-none');
            $pjLink.parent().addClass('d-none');

            $pfPane.removeClass('show active');
            $pjPane.removeClass('show active');

            if (tipoPessoa === "F") {
                $pfLink.parent().removeClass('d-none');
            } else if (tipoPessoa === "J") {
                $pjLink.parent().removeClass('d-none');
            }
        }

        toggleInlines();

        jQuery('#id_person_type').on('select2:select', toggleInlines);

    });
})(window.jQuery);
