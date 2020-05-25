
function load_modal(myid){

  params = "op_id=" + myid

  $.ajax({
      url: '/details/modal/',
      type: 'get',
      data: params,
      dataType: 'json',
      beforeSend: function () {
        $("#MODAL").modal("show");
      },
      success: function (data) {
        $("#MODAL_BODY").html(data.html_form);
      }
    });
}


function save_modal(){

  //GET EDITABLE DATAS FROM MODAL
  var op_id=$("#MODAL_opid").html();
  var my_date=$("#MODAL_date").val();
  var cat = $("#MODAL_cat").find(":selected").val();
  var my_comment= $("#MODAL_comment").val();

  //SET PARAMETER STRING TO send
  var params="op_id=" + op_id;
  params += "&" + "date=" + my_date;
  params += "&" + "cat=" + cat;
  params += "&" + "comment=" + my_comment;

  $.ajax({
      url: '/details/modal/save/',
      type: 'get',
      data: params,
      dataType: 'json',
      success: function (data) {
            $("#MODAL").modal("hide");
      }
    });

}