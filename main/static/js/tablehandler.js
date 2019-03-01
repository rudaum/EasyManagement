$(document).ready(function(){
    var DRAGGING = false;
    var DRAGGING_ZONE = false;
    var DRAG_TH, CURSOR_X

     // --- TABLE's COLUMNS RESIZE CAPABILITY --- \\
    $('.em-horiz-table-header').on("mousedown", function(e) {
        if (! DRAGGING && DRAGGING_ZONE) {
            DRAGGING = true;
            DRAG_TH = $(this)[0]
            CURSOR_X = e.clientX
            e.preventDefault();
        }
    });

    $('.em-horiz-table-header').on("mouseup", function() {
        if (DRAGGING) {
            DRAGGING = false;
            $(this).css('cursor', 'auto');
        }
    });

    $('.em-horiz-table-header').on("mousemove", function(e) {
        if (e.offsetX > this.offsetWidth - 7) {
            DRAGGING_ZONE = true;
            $(this).css('cursor', 'col-resize');
        }
        else {
            $(this).css('cursor', 'auto');
            DRAGGING_ZONE = false;
        }
        if (DRAGGING) {
            // Disabling text selection while dragging.
            e.preventDefault();

            // setting the cursor form.
            $(this).css('cursor', 'col-resize');

            // Handling cursor X and relative positions
            offset = (CURSOR_X - e.clientX) * -1;
            CURSOR_X = e.clientX

            // setting column width
            current_width = parseInt($(DRAG_TH).css('min-width').replace('px', ''));
            $(DRAG_TH).css('min-width', current_width + offset);
        }
    });
    // ---------------------------------------- \\

    already_sorting = false;
    // --- TABLE's COLUMNS SORTING CAPABILITY --- \\
    $(".fa-sort").on("click", function(){
        var table, th, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
        table = document.getElementsByClassName("table-responsive")[0];
        attr = $(this)[0].id.replace('-sort', '')
        th = document.getElementById(attr);
        switching = true;

        if (! already_sorting ) {
            already_sorting = true;
            // Set the sorting direction to ascending:
            dir = "asc";

            /* Make a loop that will continue until
            no switching has been done: */
            while (switching) {
                // Start by saying: no switching is done:
                switching = false;

                rows = table.rows;
                /* Loop through all table rows (except the
                first, which contains table headers): */
                for (i = 1; i < (rows.length - 1); i++) {
                    // Start by saying there should be no switching:
                    shouldSwitch = false;

                    /* Get the two elements you want to compare,
                    one from current row and one from the next: */
                    x = rows[i].getElementsByTagName("TD")[th.cellIndex].getElementsByTagName("p")[0].innerHTML;
                    y = rows[i + 1].getElementsByTagName("TD")[th.cellIndex].getElementsByTagName("p")[0].innerHTML;

                    /* Check if the two rows should switch place,
                    based on the direction, asc or desc: */
                    isDateX = new Date(x)
                    isDateY = new Date(y)
                    if (!isNaN(isDateX.valueOf())) {
                        if (dir == "asc") {
                            if (isDateX > isDateY) {
                                // If so, mark as a switch and break the loop:
                                shouldSwitch = true;
                                break;
                            }
                        } else if (dir == "desc") {
                            if (isDateX < isDateY){
                                // If so, mark as a switch and break the loop:
                                shouldSwitch = true;
                                break;
                            }
                        }
                    } else if (! isNaN(parseFloat(x - 0))) {
                        if (dir == "asc") {
                            if (parseFloat(x - y) > 0) {
                                // If so, mark as a switch and break the loop:
                                shouldSwitch = true;
                                break;
                            }
                        } else if (dir == "desc") {
                            if (parseFloat(x - y) < 0){
                                // If so, mark as a switch and break the loop:
                                shouldSwitch = true;
                                break;
                            }
                        }
                    } else if (isNaN(String(x))) {
                        if (dir == "asc") {
                            if (x.toLowerCase() > y.toLowerCase()) {
                              // If so, mark as a switch and break the loop:
                              shouldSwitch = true;
                              break;
                            }
                        } else if (dir == "desc") {
                            if (x.toLowerCase() < y.toLowerCase()) {
                              // If so, mark as a switch and break the loop:
                              shouldSwitch = true;
                              break;
                            }
                        }
                    }

                }
                if (shouldSwitch) {
                    /* If a switch has been marked, make the switch
                    and mark that a switch has been done: */
                    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                    switching = true;
                    // Each time a switch is done, increase this count by 1:
                    switchcount ++;
                } else {
                    /* If no switching has been done AND the direction is "asc",
                    set the direction to "desc" and run the while loop again. */
                    if (switchcount == 0 && dir == "asc") {
                        dir = "desc";
                        switching = true;
                    }
                }
            }
            already_sorting = false;
        }
    });
    // ---------------------------------------- \\
});

