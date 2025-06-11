window.addEventListener("load", function () {
  document.querySelectorAll("input.daterange").forEach(function (input) {
    const field = input.dataset.field;

    const picker = new DateRangePicker(input, {
      timePicker: false,
      linkedCalendars: false,
      showCustomRangeLabel: false,
      alwaysShowCalendars: true,
      opens: 'right',
      ranges: {
        'Hoje': [moment().startOf('day'), moment().endOf('day')],
        'Ontem': [moment().subtract(1, 'days').startOf('day'), moment().subtract(1, 'days').endOf('day')],
        'Últimos 7 Dias': [moment().subtract(6, 'days').startOf('day'), moment().endOf('day')],
        'Esse Mês': [moment().startOf('month'), moment().endOf('month')],
      },
      locale: {
        format: "DD/MM/YYYY",
        daysOfWeek: ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"],
        monthNames: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
        applyLabel: "OK",
        cancelLabel: "Cancelar",
      },
    }, function (start, end) {
      // input.value = start.format("DD/MM/YYYY") + " - " + end.format("DD/MM/YYYY");
    });

    // limpa valor antes do plugin ser carregado
    const param = new URLSearchParams(window.location.search).get(field);
    if (param === null || param.trim() === "") {
      input.value = "";
      picker.element.value = ''; // remove texto visível
    }

    // Botão de limpar individual
    const clearBtn = document.querySelector(`button.clear-btn[data-target="id_${field}"]`);
    if (clearBtn) {
      clearBtn.addEventListener("click", function () {
        input.value = "";
        picker.element.value = ''; // remove texto visível
        //picker.updateElement();
        picker.hide();
      });
    }
  });

});
