document.addEventListener('DOMContentLoaded', function() {
    var toggleButton = document.getElementById('toggleColumns');
    var hiddenColumns = document.querySelectorAll('.hidden-column');

    toggleButton.addEventListener('click', function() {
        hiddenColumns.forEach(function(column) {
            column.classList.toggle('hidden');
        });
    });
});