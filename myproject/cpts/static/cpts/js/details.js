
function load_modal(myid){

  params = "op_id=" + myid
//  //AJAX REQUEST TO DISPLAY MODAL CONTENT
//  $.get(
//    '/details_modal/',
//    params,
//    result_f,
//    'json'
//  );
//
//  //AJAX RESPONSE
//  function result_f(response){
//    $("#MODAL_BODY").html(response);
//  }
//
//  //DISPLAY MODAL
//  $('#MODAL').modal('show');


  $.ajax({
      url: '/details_modal/',
      type: 'get',
      data: params,
      dataType: 'json',
      beforeSend: function () {
        $("#MODAL").modal("show");
      },
      success: function (data) {
        $("#MODAL_BODY").html(data);
      }
    });
}