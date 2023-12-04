const csrftoken = $("[name=csrfmiddlewaretoken]").val();

var validator = new FormValidator({
    "events": ['blur', 'input', 'change']
}, document.forms[0]);
// on form "submit" event
document.forms[0].onsubmit = function (e) {

    var submit = true,
        validatorResult = validator.checkAll(this);
    console.log(validatorResult);

    return !!validatorResult.valid;
};
// on form "reset" event
document.forms[0].onreset = function (e) {
    validator.reset();
};
// stuff related ONLY for this demo page:
$('.toggleValidationTooltips').change(function () {
    validator.settings.alerts = !this.checked;
    if (this.checked)
        $('form .alert').remove();
}).prop('checked', false);

function setEndDateTime(dataRow){
    startDateTime = $("#"+dataRow.id).val()
    var formattedDatetime = startDateTime.replace("T", " ");
    $('#endDateTime').attr('min', formattedDatetime);
    $('#endDateTime').removeAttr('readonly')
}

function setTruckAndDriver(dataRow){
    startDateTime = $("#startDateTime").val()
    endDateTime = $("#endDateTime").val()

    $.ajax({
        url: "/appointment/getTruckAndDriver/",
        method: "POST",
        data: {
            'startDateTime' : startDateTime,
            'endDateTime' : endDateTime
        },
        beforeSend: function (xhr) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (data) {
            console.log(data.availableTrucksList[0]['adminTruckNumber'])
            data.availableTrucksList.forEach(function (item) {
                $("#truckNo").append(
                  '<option value="' + item['adminTruckNumber'] + '">' + item['adminTruckNumber'] + "</option>"
                );
            });
            data.availableDriversList.forEach(function (item) {
                $("#driverName").append(
                  '<option value="' + item['driverId'] + '">' + item['driverId']+'-' + item['name'] + "</option>"
                );
            });
            $('#truckNo').removeAttr('disabled')
            $('#driverName').removeAttr('disabled')
        },
      });

}