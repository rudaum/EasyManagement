// --- START OF GLOBAL VARS DEFINITION --- \\
var TABLES = document.getElementsByClassName("table-comparison");
var IGNORED_OBJECTS = ["AIX-rpm"];
var IGNORED_ATTR = ["unsuccessful_login_count", "time_last_login", "install_date"];
var TABLES_ROWS_IDS = [];
var DIVERGENT_ATTRS = {};

// --- END OF GLOBAL VARS DEFINITION --- //

$(document).ready(function(){
    // --- DIVERGENCES LOOKUP --- \\
    var divergences_coordinates = {};

    // Looping over Module Tables
    for (var t_idx=0; t_idx<TABLES.length; t_idx++){
        var table_divergences = [];
        var table_divergences_coord = [];
        var table_row_ids = [];

        //Looping over Rows
        for (var r_idx=1; r_idx<TABLES[t_idx].rows.length; r_idx++) {
            var row_id = TABLES[t_idx].rows[r_idx].id;

            //Getting ROWS IDs (Object Names)
            table_row_ids.push(row_id);

            //Skipping Ignored objects, if the ROW ID contains it.
            if (! IGNORED_OBJECTS.includes(row_id.split('--')[0])){
                var row_coord = [];

                // looping over Cells
                for (c_idx=1; c_idx<TABLES[t_idx].rows[r_idx].cells.length; c_idx++ ) {
                    var comparison_cell = TABLES[t_idx].rows[r_idx].cells[c_idx].getElementsByTagName('div')[0];
                    var attribute_name = TABLES[t_idx].rows[0].cells[c_idx].innerText
                    var attr_values = comparison_cell.getElementsByTagName('b')
                    var last_checked = attr_values[0].innerText;
                    var isEqual = true;
                    if (IGNORED_ATTR.indexOf(attribute_name.replace(/ /g, '_')) < 0 ){
                        // checking if all attributes for this server's object are equal
                        for (var v_idx=1; v_idx<attr_values.length; v_idx++) {
                            if (attr_values[v_idx].innerText != attr_values[v_idx-1].innerText) {
                                isEqual = false;
                                break;
                            }
                        }
                        // If there are divergent attributes, store it
                        if (! isEqual) {
                            table_divergences.push(comparison_cell);
                            table_divergences_coord.push(r_idx);
                        }
                    }
                }
            }
        }
        DIVERGENT_ATTRS[TABLES[t_idx].id] = table_divergences;
        TABLES_ROWS_IDS.push(table_row_ids);
        divergences_coordinates[TABLES[t_idx].id] = table_divergences_coord;
        var badge = document.getElementsByClassName('flex-badge')[t_idx];
        badge.innerText = divergences_coordinates[TABLES[t_idx].id].length;
    }

    // --- TABLE SETTINGS - USERS Highlight Differences --- \\
    $("#check-users-highlight").click(function(){
        // Divergent attributes from Table[0] (Users)
        divergent_attr = DIVERGENT_ATTRS['users-table'];

        // Activating the Highlight
        if ($(this).attr('class') == "far fa-circle highlight-setting") {
            $(this).attr("class","far fa-check-circle highlight-setting");

            // Looping over divergences of table[0] (Users)
            for (i = 0; i < divergent_attr.length; i++) {
                divergent_attr[i].style.background = 'rgba(255,0,0,0.3)';
            }

        // Deactivating the Highlight.
        } else if ($(this).attr('class') == "far fa-check-circle highlight-setting") {
            $(this).attr("class","far fa-circle highlight-setting");
            for (i = 0; i < divergent_attr.length; i++) {
                divergent_attr[i].style.background = 'rgba(255,255,255)';
            }
        }
    });

    // --- TABLE FILTER - Show divergent Users Only --- \\
    $("#filter-divergent-users").click(function(){
        var table = document.getElementById("users-table");
        var filter_input = document.getElementById("userFilter")

        // Filtering "cleared" servers
        if ($(this).attr('class') == "far fa-circle") {
            $(this).attr("class","far fa-check-circle");

            // Disabling RPM Filter
            filter_input.disabled = true;


            for (i=1; i < table.rows.length; i++) {
                if ( ! divergences_coordinates[table.id].includes(i) ) {
                    table.rows[i].style.display = "none";
                }
            }

        // Restoring Table
        } else if ($(this).attr('class') == "far fa-check-circle") {
            $(this).attr("class","far fa-circle");

            // Re-enabling RPM Filter
            filter_input.disabled = false;

            for (i=1; i < table.rows.length; i++) {
                    table.rows[i].style.display = "";
            }
        }
    });

    // --- TABLE FILTER - User Filter --- \\
    $("#userFilter").on("keyup", function() {
        var search = $(this).val().toLowerCase().trim().split(',');
        var diff_counter = 0;

        // Looping over users rows
        for (i=0; i<TABLES_ROWS_IDS[0].length; i++) {
            var username = TABLES_ROWS_IDS[0][i].replace('--users-row', '');
            var row = document.getElementById(TABLES_ROWS_IDS[0][i]);

            // First make it invisible
            row.style.display = "none";

            // for each comma-separated Pattern provided in the Users filter
            for (j=0; j<search.length; j++) {
                if ( username.toLowerCase().includes(search[j]) ) {
                    //Then, if it is in the filter, make it visible again
                    row.style.display = "";
                }
            }
        }

        for (i = 0; i < DIVERGENT_ATTRS['users-table'].length; i++) {
            row = DIVERGENT_ATTRS['users-table'][i].parentElement.parentElement
            if (row.style.display != "none" && row.id.includes("users-row") ) {
                diff_counter++;
            }
        }
        var badge = document.getElementsByClassName('flex-badge')[0];
        badge.innerText = diff_counter;
    });


     // --- TABLE SETTINGS - RPM Highlight Differences --- \\
    $("#check-rpms-highlight").click(function(){
        // Divergent attributes from Table[1] (RPMS)
        divergent_attr = DIVERGENT_ATTRS['rpms-table'];

        // Activating the Highlight
        if ($(this).attr('class') == "far fa-circle highlight-setting") {
            $(this).attr("class","far fa-check-circle highlight-setting");
            for (i=0; i < divergent_attr.length; i++) {
                divergent_attr[i].style.background = 'rgba(255,0,0,0.3)'
            }
        // Deactivating the Highlight.
        } else if ($(this).attr('class') == "far fa-check-circle highlight-setting") {
            $(this).attr("class","far fa-circle highlight-setting");
            for (i = 0; i < divergent_attr.length; i++) {
                divergent_attr[i].style.background = 'rgba(255,255,255)'
            }
        }
    });

    // --- TABLE FILTER - Show divergent RPMS Only --- \\
    $("#filter-divergent-rpms").click(function(){
        var table = document.getElementById("rpms-table");
        var filter_input = document.getElementById("rpmFilter")

        // Filtering "cleared" servers
        if ($(this).attr('class') == "far fa-circle") {
            $(this).attr("class","far fa-check-circle");

            // Disabling RPM Filter
            filter_input.disabled = true;

            for (i=1; i < table.rows.length; i++) {
                if ( ! divergences_coordinates[table.id].includes(i) ) {
                    table.rows[i].style.display = "none";
                }
            }

        // Restoring Table
        } else if ($(this).attr('class') == "far fa-check-circle") {
            $(this).attr("class","far fa-circle");

            // Re-enabling RPM Filter
            filter_input.disabled = false;

            for (i=1; i < table.rows.length; i++) {
                    table.rows[i].style.display = "";
            }
        }
    });

    // --- TABLE FILTER - RPM Filter --- \\
    $("#rpmFilter").on("keyup", function() {
        var search = $(this).val().toLowerCase().trim().split(',');
        var diff_counter = 0;

        // Looping over users rows
        for (i=0; i<TABLES_ROWS_IDS[1].length; i++) {
            var rpmname = TABLES_ROWS_IDS[1][i].replace('--rpms-row', '');
            var row = document.getElementById(TABLES_ROWS_IDS[1][i]);

            // First make it invisible
            row.style.display = "none";

            // for each comma-separated Pattern provided in the Users filter
            for (j=0; j<search.length; j++) {
                if ( rpmname.toLowerCase().includes(search[j]) ) {
                    //Then, if it is in the filter, make it visible again
                    row.style.display = "";
                }
            }
        }

        for (i = 0; i < DIVERGENT_ATTRS['rpms-table'].length; i++) {
            row = DIVERGENT_ATTRS['rpms-table'][i].parentElement.parentElement
            if (row.style.display != "none" && row.id.includes("--rpms-row") ) {
                diff_counter++;
            }
        }
        var badge = document.getElementsByClassName('flex-badge')[1];
        badge.innerText = diff_counter;
    });

});


