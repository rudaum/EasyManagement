$(document).ready(function(){
    $("#userFilter").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $(".dropdown-menu li").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

    $('#user-dropdown-menu li').click(function () {
        if (user != '') {
            user = $(this).text().toLowerCase();
            window.location.replace("http://127.0.0.1:5000/users/" + user)
        };
    });


    // --- DRAGGABLE FILTER FORM CAPABILITY --- \\
    filterform_active = false;
    table_filter = document.getElementById("draggable-filter");
    panel_base = document.getElementById("panel-base");
    shadow = document.getElementById("shadow-layer");

    function deactivate_form() {
        $(table_filter).css('display', 'None');
        $(shadow).css('display', 'None');
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
        included_servers = document.getElementById('select-servers-included').options;
        excluded_servers = document.getElementById('select-servers-excluded').options;
        included_attrs = document.getElementById('select-attr-included').options;
        excluded_attrs = document.getElementById('select-attr-excluded').options;

        // Processing Filters ...

        for (i = 0; i < included_servers.length; i++) {
            row_id = "#" + included_servers[i].value + "-row";
            $(row_id).css('display', '');
        }

        for (i = 0; i < excluded_servers.length; i++) {
            row_id = "#" + excluded_servers[i].value + "-row";
            $(row_id).css('display', 'none');
        }

        for (i = 0; i < included_attrs.length; i++) {
            attr_id = included_attrs[i].value;
            $("#" + attr_id + '-col').css('display', '');
            for (j = 0; j < included_servers.length; j++) {
                cell_id = included_servers[j].value + "_" + attr_id;
                $("#" + cell_id).css('display', '');
            }
        }

        for (i = 0; i < excluded_attrs.length; i++) {
            attr_id = excluded_attrs[i].value;
            $("#" + attr_id + '-col').css('display', 'none');
            for (j = 0; j < included_servers.length; j++) {
                cell_id = included_servers[j].value + "_" + attr_id;
                $("#" + cell_id).css('display', 'none');
            }
        }
        deactivate_form();
    });

    $("#btn-ff-reset").click(function(){
        $("#select-servers-excluded > option").each(function(){
            $(this).remove().appendTo("#select-servers-included");
        });
        $("#select-attr-excluded > option").each(function(){
            $(this).remove().appendTo("#select-attr-included");
        });
    });

    $("#btn-ff-cancel").click(function(){
        deactivate_form();
    });
    // ---------------------------------------- \\



});

