
$("#addFieldsetBtn").click(function(event){
    event.stopPropagation();
    $('#addFieldsetModal').modal('show');
});

$('#requiredFieldValue').select2({
    placeholder: 'Select options',
    width: '100%'
});

$('#truckInformationForm').submit(function (e) {
    $('input[required], select[required]').each(function () {
        if (!$(this).val()) {
            $(this).addClass('is-invalid');
            e.preventDefault();
        } else {
            $(this).removeClass('is-invalid');
        }
    });
});

$('input[name="requiredCheck"]').on('change', function(){
    let selectedRadio =$(this).val();
    if(selectedRadio == "conditionallyRequired"){
        $('.customRequiredSection').removeClass('d-none')
        $('#requiredField').attr('required', true)
    }else{
        $('.customRequiredSection').addClass('d-none')
        $('#requiredField').removeAttr('required')
    }
})

$('#requiredField').on('change', function(){
    let selectedVal = $(this).val()
    let inputBoxes = null
    let selectBoxes = null
    $.getJSON("/static/Account/fleetInformation.json", function(data) {
        $('#requiredFieldValue').empty();
        var customInformation = data["CUSTOM-INFORMATION"];
        inputBoxes = customInformation['input-fields'].hasOwnProperty(selectedVal)
        selectBoxes = customInformation['select-fields'].hasOwnProperty(selectedVal)
        if (selectBoxes) {
            var options = Object.keys(customInformation['select-fields'][selectedVal]);
            for (var i = 0; i < options.length; i++) {
                $('#requiredFieldValue').append($('<option>', {
                    value: options[i],
                    text: options[i],
                    selected : options[i] == 'All' ? true : false  
                }));
            }            
            $('#requiredFieldValue').removeAttr('disabled').attr('required','true');
        }else{
            $('#requiredFieldValue').removeAttr('required').attr('disabled','true');
        }
    });
    // let selectBoxes = {
    //     'groups' : ['Agi','Helper','Test', 'Demo', 'Driver'],
    //     'subGroups' : [],
    //     'vehicleType' : ['Tipper','Concrite'],
    //     'serviceGroup' : ['Tipper','Concrite'],
    //     'informationMake' : ['Freightliner', 'Abc'],
    //     'informationConfiguration' : ['Tipper'],
    //     'registrationState' : ['California','New-York'],
    //     'registrationInterval' : ['New-York']
    // }

})
