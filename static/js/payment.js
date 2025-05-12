$(document).ready(function () {
    const $checkbox = $('#id_paid');
    const $dateField = $('#id_paid_at');
    const $amountField = $('#id_paid_amount');
    const $methodField = $('#id_method');
    const $receivedByField = $('#id_received_by');

    function togglePaymentFields(enabled) {
        $dateField.prop('disabled', !enabled);
        $amountField.prop('disabled', !enabled);
        $methodField.prop('disabled', !enabled).trigger('change.select2'); // Atualiza o Select2
        $receivedByField.prop('disabled', !enabled).trigger('change.select2'); // Atualiza o Select2
    }

    $checkbox.change(function () {
        if ($(this).is(':checked')) {
            // Define a data atual se estiver vazia
            if (!$dateField.val()) {
                const today = new Date();
                const formattedDate = today.toISOString().split('T')[0]; // YYYY-MM-DD
                $dateField.val(formattedDate);
            }
            togglePaymentFields(true);
        } else {
            $dateField.val('');
            $amountField.val('');
            $methodField.val('');
            $dateField.val('');
            $receivedByField.val('');
            togglePaymentFields(false);
        }
    });

    // Inicializa corretamente no carregamento (caso já esteja marcado)
    togglePaymentFields($checkbox.is(':checked'));
});