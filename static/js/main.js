$(document).ready(function (){
    $(".delete").click(function (){
        $('#deleteModal').modal('show');
        $("#deleteForm").attr("action",`delete/${$(this).attr('data-id')}`)
    })

    $("#copy").click(function (){
        copyFromMap()
    })
    function copyFromMap() {
        /* Get the text field */
        var lng = $("#lng").val();
        var lat = $("#lat").val();

        $("#new_lng").val(lng)
        $("#new_lat").val(lat)

    }
})