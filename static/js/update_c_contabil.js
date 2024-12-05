document.addEventListener('DOMContentLoaded', function () {
    const categoriaSelect = document.getElementById('id_categoria');
    const cContabilInput = document.getElementById('id_c_contabil');

    categoriaSelect.addEventListener('change', function () {
        const selectedOption = categoriaSelect.options[categoriaSelect.selectedIndex];

        if (selectedOption.value) {
            const cContabilValue = selectedOption.getAttribute('data-c-contabil');

            cContabilInput.value = cContabilValue;
        } else {
            cContabilInput.value = '';
        }
    });
});
