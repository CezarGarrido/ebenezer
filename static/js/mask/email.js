(function ($) {
    $(document).ready(function () {
        $('[data-mask-email]').mask("A", {
            translation: {
                "A": { pattern: /[\w@\-.+]/, recursive: true }
            }
        });
    });
})(django.jQuery);
