$(document).ready(function() {

    // Function for ajax request to get info from the database and display to the respective dataTables
    function get_table(table_name){
        switch(table_name){
            case "assets_table":
                input_table = assets_table
                server_url = "/get_assets_table";
                break;
            case "issuers_table":
                input_table = issuers_table;
                server_url =  "/get_issuers_table";
                break;
            case "transactions_table":
                input_table = transactions_table;
                server_url = "/get_transactions_table";
                break;
        };
        $.ajax({
            data : {
                input_date: $("#datepicker").val()
            },
            type : 'POST',
            url : server_url,
            success: function(data){
                if (data.error){
                    $('#dangerAlert-table').show();
                    $('#successAlert-table').hide();
                    $('#successAlert-recon').hide();
                    input_table.clear().draw();
                } else {
                    $('#successAlert-table').text("Table Loaded. Date Selected: " + data.date + "!").show();
                    $('#dangerAlert-table').hide();
                    input_table.clear();
                    input_table.rows.add(data.df);
                    input_table.draw();
                }
            },
            beforeSend: function(){
                $("#loader").show();
            },
            complete: function(){
                $("#loader").hide();
            }
        });
    };

    // If data not found, means positions have not been reconciled. Run reconcile function to get the database.
    // Once database is created for that date, it will then link to get_table() function to show the respective table.
    function reconcile(table_name){
        $.ajax({
            data : {
               input_date: $("#datepicker").val()
            },
            type : 'POST',
            url : "/reconcile",
            success: function(data){
                if (data.error){
                    $('#dangerAlert-table').text("Error. Please check if source files are in place for " + data.date).show();
                    $('#successAlert-table').hide();
                } else {
                    $('#successAlert-recon').text("Reconciliation Done. Date Selected: " + data.date + "!").show();
                    $('#dangerAlert-table').hide();
                    get_table(table_name);
                }
            },
            beforeSend: function(){
                $("#loader").show();
            },
            complete: function(){
                $("#loader").hide();
            }
        });
    };

    // Initialise all 3 tables but there are only 1 table on each page.
    var assets_table = $('#assets_table').DataTable();
    var issuers_table = $('#issuers_table').DataTable();
    var transactions_table = $('#transactions_table').DataTable();

    // Get which table we are on
    table_name = $("table").attr("id");

    // Datepicker
    $( "#datepicker" ).datepicker({
        dateFormat: "dd-mm-yy",
        maxDate: '0',
        onSelect: function(event){
              get_table(table_name);
        }
    }).datepicker("setDate", new Date());

    // Populate the initial date.
    reconcile(table_name);

    // Click to reconcile data and show reconciled tables.
    $('.href_reconcile').click(function(event){
        reconcile(table_name);
        event.preventDefault();
    });

    // Reset button to clear the database
    $("#clearDB_btn").click(function(){
        $.ajax({
            type : 'POST',
            url : "/reset",
            success: function(){
                alert("All reconciled data has been deleted. Page will now refresh.");
                location.reload();
            }
        });
    });



});
