const csrftoken = $("[name=csrfmiddlewaretoken]").val();

$(document).ready(function(){
    checkRecurring()
    console.log('reload')
});

$('#repeats').on('change', function(){
    checkRecurring()
})

$('#startTime').on('change', function(){
    let startTime = $(this).val()
    var inputTime = new Date("2024-02-08T" + startTime + ":00");
    inputTime.setMinutes(inputTime.getMinutes() - 15);
    var formattedTime = inputTime.getHours() + ":" + (inputTime.getMinutes() < 10 ? '0' : '') + inputTime.getMinutes();
    $('#reportingTime').val(formattedTime);
})

function checkRecurring() {
    let repeats = $('#repeats').val();
    if (repeats == 'NoRecurring') {
        $('.noRecurring').removeClass('d-none');
        $('.dailyRecurring').addClass('d-none');
        $('.days').addClass('d-none');
    }else if(repeats == 'Daily'){
        $('.noRecurring').addClass('d-none');
        $('.dailyRecurring').removeClass('d-none');
        $('.days').addClass('d-none');
    }else if(repeats == 'Custom'){
        $('.noRecurring').addClass('d-none');
        $('.dailyRecurring').removeClass('d-none');
        $('.days').removeClass('d-none');
    }
}

var validator = new FormValidator({
    "events": ['blur', 'input', 'change']
}, document.forms[0]);
// on form "submit" event
document.forms[0].onsubmit = function (e) {
    var submit = true, validatorResult = validator.checkAll(this);
    
    $('select[required]').each(function() {
        if (!$(this).val()) {
            validatorResult.valid = false
            $(this).css('border','1px solid #CE5454');
        }else{
            $(this).css('border','1px solid #ced4da');
        }
    });
    if($('#truckNo').val() && !$('#origin').val()){
        console.log($('#truckNo').val())
        validatorResult.valid = false
        $('#origin').css('border','1px solid #CE5454')
    }

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

$('#startDateTime').on('change',function(){
    setTruckAndDriver(this);
});


function setTruckAndDriver(dataRow){
    startDateTime = $("#startDateTime").val()
    endDateTime = $("#endDateTime").val()
    console.log(startDateTime,endDateTime);
    if(startDateTime && endDateTime){
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
                $('#addDriver').removeAttr('disabled')
                $('#addTruck').removeAttr('disabled')
            },
        });
    }
}

$("#origin, #appStop, select[name^='appStop']").on('change', function(){
    let originName = $(this).val()
    console.log(originName); 
    if(originName){
        $("#origin").removeClass('isInvalid')
        $.ajax({
            url: "/appointment/getOriginDetails/",
            method: "POST",
            data: {
                'originName' : originName
            },
            beforeSend: function (xhr) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (data) {
                console.log(data);
                if(data.status == true){
                    $('#originAddress').val(data.origin.address);
                    $('#originPhone').val(data.origin.phone)
                    $('#originPersonOnName').val(data.origin.personOnName)
                    $('#originLatitude').val(data.origin.lat)
                    $('#originLongitude').val(data.origin.long)
                    $('#originAddress').attr('readonly',true)
                    $('#originPhone').attr('readonly',true)
                    $('#originPersonOnName').attr('readonly',true)
                    $('#originLatitude').attr('readonly',true)
                    $('#originLongitude').attr('readonly',true)
                    $('#locationDiv').addClass('d-none')
                    $('#errorMsgForOrigin').addClass('d-none')
                }
            },
        });
        
    }else{
        $("#origin").addClass('isInvalid')
    }
})

// function openBox(checked,id){
//     if ($(`#${checked.id}`).prop('checked')) {
//         $(`#${id}`).removeAttr('disabled');
//         $(`#${id}`).attr('required', 'true');
//     }else{
//         $(`#${id}`).attr('disabled', true)
//         $(`#${id}`).removeAttr('required');
//     }
// }

// $('#addTruck').on('change', function(){
//     if ($(`#addTruck`).prop('checked')) {
//         $(`#truckNo`).removeAttr('disabled');
//         $(`#origin`).removeAttr('disabled');
//         $(`#appStop`).removeAttr('disabled');
//         $(`#truckNo`).attr('required', 'true');
//         $(`#origin`).attr('required', 'true');
//         $(`#appStop`).attr('required', 'true');
//         $(`#originAddress`).attr('required', 'true');
//         $(`#originPhone`).attr('required', 'true');
//         $(`#originPersonOnName`).attr('required', 'true');
//         $(`#originLatitude`).attr('required', 'true');
//         $(`#originLongitude`).attr('required', 'true');
//         $(`.stopDiv`).removeClass('d-none');
//     }else{
//         $(`#truckNo`).attr('disabled', true)
//         $(`#origin`).attr('disabled', true)
//         $(`#appStop`).attr('disabled', true)
//         $(`#truckNo`).removeAttr('required');
//         $(`#origin`).removeAttr('required');
//         $(`#appStop`).removeAttr('required');
//         $(`#originAddress`).removeAttr('required');
//         $(`#originPhone`).removeAttr('required');
//         $(`#originPersonOnName`).removeAttr('required');
//         $(`#originLatitude`).removeAttr('required');
//         $(`#originLongitude`).removeAttr('required');
//         $(`.stopDiv`).addClass('d-none');

//     }
// })


function openBox(checked, id) {
    const isChecked = $(`#${checked.id}`).prop('checked');
    $(`#${id}`).prop('disabled', !isChecked).prop('required', isChecked);
}   

$('#addTruck').on('change', function(){
    const isChecked = $(this).prop('checked');
    // $('#truckNo, #origin, #appStop').prop('disabled', !isChecked);
    $('#truckNo, #origin').prop('disabled', !isChecked);
    $('#truckNo, #origin').prop('required', isChecked);
    // $('#originAddress, #originPhone, #originPersonOnName, #originLatitude, #originLongitude').prop('required', isChecked);
    // $('.stopDiv').toggleClass('d-none', !isChecked);
});


function addOrigin(){
    $('#originAddress').val('')
    $('#originPhone').val('')
    $('#originPersonOnName').val('')
    $('#originLatitude').val('')
    $('#originLongitude').val('')
    $('#errorMsgForOrigin').val('')
    $('#originAddress').removeAttr('readonly')
    $('#originPhone').removeAttr('readonly')
    $('#originPersonOnName').removeAttr('readonly')
    $('#originLatitude').removeAttr('readonly')
    $('#originLongitude').removeAttr('readonly')
    // $('#errorMsgForOrigin').removeClass('d-none')
    $('#locationDiv').removeClass('d-none')
    $("#originAddVal").val(1)
}

