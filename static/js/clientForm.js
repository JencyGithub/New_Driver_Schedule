const csrftoken = $("[name=csrfmiddlewaretoken]").val();


$(document).ready(function() {
    $(".js-example-basic-single").append(
        `<option value="AL">Alabama</option>
        <option value="WY">Wyoming</option>`
      );
    $('#clientId').select2();
    $('#truckNum').select2();

    $("#clientId").on("change", function () {
      let clientId = $(this).val();
    
      if (clientId) {
        $("#truckNum").prop("disabled", false);
        $("#truckNum").html('<option value="">Loading...</option>');
        $.ajax({
          type: "POST",
          url: "/account/getTrucks/",
          data: {
            clientName: $(this).val(),
          },
          beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          },
          success: function (data) {
            $("#truckNum").html('<option value="">Select an Item</option>');
            data.trucks.forEach(function (item) {
              $("#truckNum").append(
                `<option value="${item}">${item}</option>`
              );
            });
            $("#truckNum").trigger("change.select2");
    
            if (data.docket) {
              $("#nextBtn").val("Submit");
            } else {
              $("#nextBtn").val("Next");
            }
          },
        });
      }
    });
});



