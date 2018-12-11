$(document).ready(function(){
    $("#user-changelogFilter").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $(".dropdown-menu li").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

        // --- DRAGGABLE FILTER FORM CAPABILITY --- \\
    var filterform_active = false;
    var table_filter = document.getElementById("draggable-filter");
    var panel_base = document.getElementById("panel-base");
    var shadow = document.getElementById("shadow-layer");
    var error_box = document.getElementById('error-box');

    function today_str() {
        today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth()+1; //January is 0!
        var yyyy = today.getFullYear();
        if(dd < 10) {
            dd = '0' + dd;
        }
        if(mm < 10) {
            mm = '0' + mm;
        }
        return yyyy + '-' + mm + '-' + dd;
    }

    function deactivate_form() {
        $(table_filter).css('display', 'none');
        $(shadow).css('display', 'none');
        filterform_active = false;
    };

    function activate_form() {
        $(table_filter).css('display', 'block');
        $(table_filter).css('top', $('#filter-table').offset().top);
        $(table_filter).css('left', $('#filter-table').offset().left + $('#filter-table').width() + 1);
        filterform_active = true;
        $(shadow).css('display', 'block');
        $(shadow).css('min-width', panel_base.scrollWidth);
        $(shadow).css('min-height', panel_base.scrollHeight);
        $(error_box).css('display', 'none');
    };

    $("#filter-button").on("click", function(){
        form = document.getElementById("draggable-filter");
        if (!filterform_active) {
            activate_form();
        } else {
            deactivate_form();
        }
    });

    $("#filter-close").on("click", function(){
        form = document.getElementById("draggable-filter");
        $(form).css('display', 'None');
        filterform_active = false;
        deactivate_form();
    });

    dragElement(document.getElementById("draggable-filter"));
    function dragElement(elmnt) {
        var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
        if (document.getElementById("filter-bar")) {
            // if present, the header is where you move the DIV from:
            document.getElementById("filter-bar").onmousedown = dragMouseDown;
        } else {
            // otherwise, move the DIV from anywhere inside the DIV:
            elmnt.onmousedown = dragMouseDown;
        }

        function dragMouseDown(e) {
            e = e || window.event;
            e.preventDefault();
            // get the mouse cursor position at startup:
            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;
            // call a function whenever the cursor moves:
            document.onmousemove = elementDrag;
        }

        function elementDrag(e) {
            e = e || window.event;
            e.preventDefault();
            // calculate the new cursor position:
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;
            // set the element's new position:
            elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
            elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
        }

        function closeDragElement() {
            // stop moving when mouse button is released:
            document.onmouseup = null;
            document.onmousemove = null;
        }
    }
    // ---------------------------------------- \\


    // --- TABLE SETTINGS - SERVERS FILTER --- \\
    $("#button-servers-exclude").click(function(){
        $("#select-servers-included > option:selected").each(function(){
            $(this).remove().appendTo("#select-servers-excluded");
        });
        var my_options = $("#select-servers-excluded option");
        var selected = $("#select-servers-excluded").val();

        my_options.sort(function(a,b) {
            if (a.text > b.text) return 1;
            if (a.text < b.text) return -1;
            return 0
        })

        $("#select-servers-excluded").empty().append( my_options );
        $("#select-servers-excluded").val(selected);
    });

    $("#button-servers-include").click(function(){
        $("#select-servers-excluded > option:selected").each(function(){
            $(this).remove().appendTo("#select-servers-included");
        });
        var my_options = $("#select-servers-included option");
        var selected = $("#select-servers-included").val();

        my_options.sort(function(a,b) {
            if (a.text > b.text) return 1;
            if (a.text < b.text) return -1;
            return 0
        })

        $("#select-servers-included").empty().append( my_options );
        $("#select-servers-included").val(selected);
    });
    // ---------------------------------------- \\

    // --- TABLE SETTINGS - ATTRIBUTES FILTER --- \\
    $("#button-attr-exclude").click(function(){
        $("#select-attr-included > option:selected").each(function(){
            $(this).remove().appendTo("#select-attr-excluded");
        });
        var my_options = $("#select-attr-excluded option");
        var selected = $("#select-attr-excluded").val();

        my_options.sort(function(a,b) {
            if (a.text > b.text) return 1;
            if (a.text < b.text) return -1;
            return 0
        })

        $("#select-attr-excluded").empty().append( my_options );
        $("#select-attr-excluded").val(selected);
    });

    $("#button-attr-include").click(function(){
        $("#select-attr-excluded > option:selected").each(function(){
            $(this).remove().appendTo("#select-attr-included");
        });
        var my_options = $("#select-attr-included option");
        var selected = $("#select-attr-included").val();

        my_options.sort(function(a,b) {
            if (a.text > b.text) return 1;
            if (a.text < b.text) return -1;
            return 0
        })

        $("#select-attr-included").empty().append( my_options );
        $("#select-attr-included").val(selected);
    });
    // ---------------------------------------- \\

    // --- TABLE SETTINGS - FORM BUTTONS --- \\
    $("#btn-ff-apply").click(function(){
        // validating dates ...
        var proceed = true;
        var firstday = new Date('2018-12-01 00:00:00')
        var startdate = new Date(document.getElementById('input-startdate').value + " 00:00:00");
        var enddate = new Date(document.getElementById('input-enddate').value + " 23:59:59");
        error_box.innerHTML = '';

        if (startdate == 'Invalid Date' ) {
            startdate = firstday;
            document.getElementById('input-startdate').valueAsDate = startdate;
        }

        if (enddate == 'Invalid Date' ) {
            enddate = new Date();
            enddate.setHours(23, 59, 59, 0);
            document.getElementById('input-enddate').valueAsDate = enddate;
        }

        if (startdate > enddate){
            error_box.innerHTML = error_box.innerHTML + '<p class="error-font smaller-text left">- Start Date can not be after End Date</p>'
            proceed = false;
        }

        if (startdate > new Date()) {
            error_box.innerHTML = error_box.innerHTML + '<p class="error-font smaller-text left">- Start Date can not be in the future.</p>'
            proceed = false;
        }

        if (proceed) {
            included_servers = document.getElementById('select-servers-included').options;
            excluded_servers = document.getElementById('select-servers-excluded').options;
            rows = $('#table-users-changelog tr');
            columns = $('#table-users-changelog th');

            included_attrs = new Array();
            sel = document.getElementById('select-attr-included');
            for (i = 0; i < sel.length; i++) {
                included_attrs.push(sel.options[i].text);
            }

            excluded_attrs = new Array();
            sel = document.getElementById('select-attr-excluded');
            for (i = 0; i < sel.length; i++) {
                excluded_attrs.push(sel.options[i].text);
            }

            // Processing  Servers Filters ...
            for (i = 1; i < rows.length; i++) {
                server = rows[i].getElementsByTagName("TD")[0].getElementsByTagName("P")[0].innerHTML
                for (j = 0; j < included_servers.length; j++) {
                    if (included_servers[j].value == server) {
                        rows[i].style.display = '';
                    }
                }
                for (j = 0; j < excluded_servers.length; j++) {
                    if (excluded_servers[j].value == server) {
                        rows[i].style.display = 'none';
                    }
                }
            }

            // Processing  Columns Filters ...

            for (i = 0; i < columns.length; i++) {
                column = columns[i].id.replace('-col', '')

                if (included_attrs.includes(column)) {
                    rows[0].getElementsByTagName("TH")[i].style.display = '';
                    for (j = 1; j < rows.length; j++) {
                        rows[j].getElementsByTagName("TD")[i].style.display = '';
                    }
                }

                if (excluded_attrs.includes(column)) {
                    rows[0].getElementsByTagName("TH")[i].style.display = 'none';
                    for (j = 1; j < rows.length; j++) {
                        rows[j].getElementsByTagName("TD")[i].style.display = 'none';
                    }
                }
            }

            // Processing Dates Filter.
            for (i = 1; i < rows.length; i++) {
                date = new Date(rows[i].getElementsByTagName("TD")[6].getElementsByTagName("P")[0].innerHTML);
                if ( date > enddate ) {
                    rows[i].style.display = 'none';
                } else if ( date < startdate ) {
                    rows[i].style.display = 'none';
                } else {
                    rows[i].style.display = '';
                }
            }

            error_box.style.display = 'none';
            deactivate_form();
        }
        else {
            error_box.style.display = '';
        }
    });

    $("#btn-ff-reset").click(function(){
        $("#select-servers-excluded > option").each(function(){
            $(this).remove().appendTo("#select-servers-included");
        });
        $("#select-attr-excluded > option").each(function(){
            $(this).remove().appendTo("#select-attr-included");
        });
        document.getElementById('input-startdate').value = '';
        document.getElementById('input-enddate').value = '';
        $(error_box).css('display', 'none');
    });

    $("#btn-ff-cancel").click(function(){
        deactivate_form();
    });
    // ---------------------------------------- \\
});

