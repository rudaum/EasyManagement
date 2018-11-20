$(document).ready(function(){
    $("#userFilter").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $(".dropdown-menu li").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

    $('.dropdown-menu li').click(function () {
        if (user != '') {
            //$('#' + user).hide();

            user = $(this).text().toLowerCase();
            window.location.replace("http://127.0.0.1:5000/users/" + user)
        };
    });

    $('#table-filter').on("keyup", function() {
        var filter, tr, td, tbody, i;
        filter = $(this).val().toUpperCase();

        tbody = document.getElementById("user-table-body");
        tr = tbody.getElementsByTagName("tr");
        for (i = 0; i < tr.length; i++) {
            th = tr[i].getElementsByTagName("th")[0];
            if (th) {
              if (th.innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
              } else {
                tr[i].style.display = "none";
              }
            }
        }
    });

});

