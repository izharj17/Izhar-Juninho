$(document).ready(function() {
    // Show the second form and hide the first one
    $('#nextBtn').on('click', function() {
        $('#form1').hide();
        $('#form2').show();
    });

    // Show the first form and hide the second one
    $('#prevBtn').on('click', function() {
        $('#form2').hide();
        $('#form1').show();
    });
});

// odoo.define('website_ppdb.sibling_table_container', function (require) {
//     "use strict";

//     const $ = require('jquery');

//     // Function to add a new row
//     function addRow() {
//         var table = $('#sibling_table tbody');
//         var newRow = $('<tr>' +
//             '<td style="border: 1px solid #000;">&#160;</td>' +
//             '<td style="border: 1px solid #000;">&#160;</td>' +
//             '<td style="border: 1px solid #000;">&#160;</td>' +
//             '<td style="border: 1px solid #000;">' +
//             '<button type="button" class="btn btn-danger btn-sm remove-line">Remove</button>' +
//             '</td>' +
//             '</tr>');
//         table.append(newRow);
//     }

//     // Event listener for adding a new row
//     $(document).on('click', '#add_line', addRow);

//     // Event delegation for removing a row
//     $(document).on('click', '.remove-line', function () {
//         $(this).closest('tr').remove();
//     });
// });




