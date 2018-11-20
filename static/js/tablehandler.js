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
            e.preventDefault();
            $(this).css('cursor', 'col-resize');
            offset = (CURSOR_X - e.clientX) * -1;

            // updating cursor x pos
            CURSOR_X = e.clientX

            // setting column width
            current_width = parseInt($(DRAG_TH).css('min-width').replace('px', ''));
            $(DRAG_TH).css('min-width', current_width + offset);

            console.log('CURSOR X: ' + CURSOR_X);
            console.log('offsetWidth: ' + this.offsetWidth);
            console.log('eoofsetX: ' + e.offsetX);
            console.log('left: ' + DRAG_TH.offsetLeft);
            console.log('-----------------------------------------');
        }
    });
    // ---------------------------------------- \\
});
