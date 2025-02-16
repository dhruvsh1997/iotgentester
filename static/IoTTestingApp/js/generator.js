// IoTTestingApp/static/IoTTestingApp/js/generator.js
$(document).ready(function() {
    const numRowsSlider = $('#numRows');
    const rowValue = $('#rowValue');
    const generatorForm = $('#generatorForm');
    const dataTableContainer = $('#dataTableContainer');
    const dataTable = $('#dataTable');
    const testForm = $('#testForm');
    const tableData = $('#tableData');
    
    // Update row value display when slider moves
    numRowsSlider.on('input', function() {
        rowValue.text(this.value);
    });
    
    // Handle form submission
    generatorForm.on('submit', function(e) {
        e.preventDefault();
        
        // Show loading overlay
        const loadingOverlay = $('<div class="loading-overlay"><div class="loading-spinner"></div></div>');
        $('body').append(loadingOverlay);
        
        // Get form data
        const formData = new FormData(this);
        
        // Send AJAX request
        $.ajax({
            url: '/generate-data/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Create table headers
                const headerRow = $('<tr>');
                response.columns.forEach(column => {
                    headerRow.append($('<th>').text(column));
                });
                dataTable.find('thead').html(headerRow);
                
                // Create table body
                const tbody = dataTable.find('tbody');
                tbody.empty();
                
                response.data.forEach(row => {
                    const tr = $('<tr>');
                    response.columns.forEach(column => {
                        tr.append($('<td>').text(row[column]));
                    });
                    tbody.append(tr);
                });
                
                // Store data for testing
                tableData.val(JSON.stringify(response.data));
                
                // Show table container
                dataTableContainer.removeClass('d-none');
                
                // Remove loading overlay
                loadingOverlay.remove();
            },
            error: function(xhr, status, error) {
                alert('Error generating data: ' + error);
                loadingOverlay.remove();
            }
        });
    });
});