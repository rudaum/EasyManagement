// --- START OF GLOBAL VARS DEFINITION --- \\
var PH_COMPARED = new Option(" Choose at least 2 ","ph_compared");
PH_COMPARED.disabled = true;
PH_COMPARED.style.fontStyle = "italic";

var PH_AVAILABLE = new Option(" Are you sure? ","ph_available");
PH_AVAILABLE.disabled = true;
PH_AVAILABLE.style.fontStyle = "italic";
// --- START OF GLOBAL VARS DEFINITION --- //

$(document).ready(function(){
    // --- DRAGGABLE FILTER FORM CAPABILITY --- \\
    filterform_active = false;
    draggable_form = document.getElementById("draggable_form");
    panel_base = document.getElementById("panel-base");
    shadow = document.getElementById("shadow-layer");

    function deactivate_form() {
        $(draggable_form).css('display', 'None');
        $(shadow).css('display', 'None');
        filterform_active = false;
    };

    function activate_form() {
        var width_axis = $("#flex-main-panel").width() / 2;
        var left = width_axis - $(draggable_form).width() / 2;
        $(draggable_form).css('left', left);

        var height_axis = $("#flex-main-panel").height() / 2;
        var top = height_axis - $(draggable_form).height() / 2;
        $(draggable_form).css('top', top);
        $(draggable_form).css('display', 'flex');
        filterform_active = true;
        $(shadow).css('display', 'flex');
        $(shadow).css('min-width', '100%');
        $(shadow).css('min-height', '100%');
    };

    $("#flex-report-button").on("click", function(){
        if ( filterform_active == false) {
            activate_form();
        } else {
            deactivate_form();
        }
    });

    $("#df-button-close").on("click", function(){
        $(draggable_form).css('display', 'None');
        filterform_active = false;
        deactivate_form();
    });


    // ---------------------------------------- \\


    // --- FORM SETTINGS - SERVERS FILTER --- \\
    $(".module").click(function(){
        if ($(this).attr('class') == "far fa-circle module") {
            $(this).attr("class","far fa-check-circle module");
        } else if ($(this).attr('class') == "far fa-check-circle module") {
            $(this).attr("class","far fa-circle module");
        }
    });

    $("#button-to-compared").click(function(){
        if ($("#select-servers-compared")[0].options[0].value == PH_COMPARED.value &&
        $("#select-servers-available > option:selected").length > 0) {
            $("#select-servers-compared")[0].options[0].remove();
        }
        $("#select-servers-available > option:selected").each(function(){
            $(this).remove().appendTo("#select-servers-compared");
        });
        var my_options = $("#select-servers-compared option");
        var selected = $("#select-servers-compared").val();

        my_options.sort(function(a,b) {
            if (a.text > b.text) return 1;
            if (a.text < b.text) return -1;
            return 0
        })

        $("#select-servers-compared").empty().append( my_options );
        $("#select-servers-compared").val(selected);
        if ($("#select-servers-available > option").length < 1) {
            //$("#select-servers-available")[0].options[0].text == "Are you sure?"
            $(PH_AVAILABLE).appendTo("#select-servers-available");
        }
    });

    $("#button-to-available").click(function(){
         if ($("#select-servers-available")[0].options[0].value == PH_AVAILABLE.value &&
            $("#select-servers-compared > option:selected").length > 0) {
                $("#select-servers-available")[0].options[0].remove();
            }
        $("#select-servers-compared > option:selected").each(function(){
            $(this).remove().appendTo("#select-servers-available");
        });
        var my_options = $("#select-servers-available option");
        var selected = $("#select-servers-available").val();

        my_options.sort(function(a,b) {
            if (a.text > b.text) return 1;
            if (a.text < b.text) return -1;
            return 0
        })

        $("#select-servers-available").empty().append( my_options );
        $("#select-servers-available").val(selected);
        if ($("#select-servers-compared > option").length < 1) {
            $(PH_COMPARED).appendTo("#select-servers-compared");
        }
    });
    // ---------------------------------------- \\


    // --- TABLE SETTINGS - ATTRIBUTES FILTER --- \\

    // ---------------------------------------- \\


    // --- TABLE SETTINGS - FORM BUTTONS --- \\
    $("#btn-df-apply").click(function(){
        var error_box = document.getElementById('error-box');
        error_box.innerHTML = '';
        selected_modules = [];
        selected_servers = [];
        proceed = true;

        // getting the selected modules to compare
        $('.module').each(function(index, module) {
            if (module.className == "far fa-check-circle module") {
                selected_modules.push(module.innerText.toLowerCase());
            }
        });

        //getting the selected servers to compare
        $("#select-servers-compared option").each(function(index, server) {
            selected_servers.push(server.value.toLowerCase());
        });

        // Checking if at least one module was selected
        if (selected_modules.length < 1) {
            error_box.innerHTML = error_box.innerHTML +
            '<p>* Select at least one Module to compare.</p>'
            proceed = false;
        }

        // Checking if at least two servers were selected to be compared
        if (selected_servers.length < 2) {
            error_box.innerHTML = error_box.innerHTML +
            '<p>* Select at least two Servers to compare.</p>'
            proceed = false;
        }

        // if no errors, proceed to the comparison site.
        if (proceed) {
            //deactivate_form();
            parameters = 'selected_servers=' + selected_servers + '&selected_modules=' + selected_modules;
            console.log(parameters);
            url = window.location.href.split('/')[0] + "//" + window.location.href.split('/')[2] + '/compare/' + parameters;
            window.location.replace(url);
        };
    });

    $("#btn-df-reset").click(function(){
        if ($("#select-servers-available")[0].options[0].value == PH_AVAILABLE.value) {
            $("#select-servers-available")[0].options[0].remove();
        }

        $("#select-servers-compared > option").each(function(){
            $(this).remove().appendTo("#select-servers-available");
        });
        $(PH_COMPARED).appendTo("#select-servers-compared");
    });


    $("#btn-df-cancel").click(function(){
        deactivate_form();
    });
    // ---------------------------------------- \\



});

