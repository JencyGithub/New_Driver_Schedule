const csrftoken = $("[name=csrfmiddlewaretoken]").val();
$("#rateCards").select2({
  placeholder: "Select options",
  width: "100%",
});
setCountryCode("countryCode1")
setCountryCode("addCountry")

var validator = new FormValidator(
  {
    events: ["blur", "input", "change"],
  },
  document.forms[0]
);
// on form "submit" event
document.forms[0].onsubmit = function (e) {
  var submit = true,
    validatorResult = validator.checkAll(this);
  if ( validatorResult.valid ) {
    validatorResult.valid = checkPhone($("#primaryContact1"));
  }

  return !!validatorResult.valid;
};
// on form "reset" event
document.forms[0].onreset = function (e) {
  validator.reset();
};

function checkPhone(value) {
  if (value.val().length != 10) {
    value.css("border", "1px solid #CE5454");
    return false;
  } else {
    value.css("border", "1px solid #ced4da");
    return true;
  }
}

function setCountryCode(givenId) {
  removeAllError()
  return new Promise((resolve, reject) => {
    fetch("/static/Account/countryCodes.json")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        const selectElement = document.getElementById(givenId);
        console.log(givenId)
        selectElement.innerHTML = "";
        data.forEach((country) => {
          const option = document.createElement("option");
          option.value = country.countryCode;
          option.text = country.countryName;
          selectElement.appendChild(option);
        });

        const defaultOption = document.createElement("option");
        defaultOption.value = "61";
        defaultOption.text = "Australia (+61)";
        defaultOption.selected = true;
        selectElement.insertBefore(defaultOption, selectElement.firstChild);
        resolve();
      })
      .catch((error) => {
        console.error("Error fetching country codes:", error);
        reject(error);
      });
  });
}

function removeAllError() {
  $("#clientOfc input, #clientOfc select, #clientOfc textarea").each(
    function () {
      $(this).css("border", "1px solid #ced4da").removeAttr('readonly').removeAttr('disabled');
    }
  );
}

function setModalWithData(ofcId, readonlyVal) {
  removeAllError();
  $.ajax({
    url: "/gearBox/client/ofc/view/",
    method: "POST",
    data: {
      ofcId: ofcId,
    },
    beforeSend: function (xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function (items) {
      setCountryCode("modalAddCountry")
        .then(() => {
          let dataObj = items.ofcObj;
          $("#modalAddDescription")
            .val(dataObj["description"])
            .attr("readonly", readonlyVal);
          $("#modalAddCity").val(dataObj["city"]).attr("readonly", readonlyVal);
          $("#modalAddState")
            .val(dataObj["state"])
            .attr("readonly", readonlyVal);
          $("#modalAddPostalCode")
            .val(dataObj["postalCode"])
            .attr("readonly", readonlyVal);
          $("#modalAddCountry")
            .val(dataObj["country"])
            .attr("readonly", readonlyVal);
          $("#modalAddress1")
            .val(dataObj["address1"])
            .attr("readonly", readonlyVal);
          $("#modalAddress2")
            .val(dataObj["address2"])
            .attr("readonly", readonlyVal);
          $("#modalAddCountry, #modalAddType").attr("disabled", readonlyVal);
          $("#rateCards").empty();
          $.each(dataObj.allRateCards, function (index, rateCard) {
            let option = $("<option>", {
              value: rateCard.id,
              text: rateCard.rate_card_name,
            });

            let isSelected = dataObj.rateCards.some(
              (rc) => rc.rateCard_id === rateCard.id
            );
            if (isSelected) {
              option.prop("selected", true);
            }

            $("#rateCards").append(option);
          });

          $("#additionalContactSection").empty();

          $.each(items.additionalInfoObjs, function (index, obj) {
            let additionalContentEdit = ``;
            additionalContentEdit += `<div class="col-12 my-2">`;
            additionalContentEdit += `<div class="row bg-light pb-3 border rounded">`;
            additionalContentEdit += `<div class="col-md-4 col-sm-4 field">`;
            additionalContentEdit += `<label for="modalPersonName${obj.id}">Person name :<span class="required">*</span></label>`;
            additionalContentEdit += `<input class="form-control" name="modalPersonName${obj.id}" id="modalPersonName${obj.id}" value="${obj.personName}" type="text" required/>`;
            additionalContentEdit += `</div>`;
            additionalContentEdit += `<div class="col-md-8 col-sm-8 field">`;
            additionalContentEdit += `<div class="flex justify-content-between">`;
            additionalContentEdit += `<label for="modalEmail${obj.id}">Person Email :<span class="required">*</span></label>`;
            // additionalContentEdit += `<i class="fa-solid fa-minus" onclick="removeContact(this)"></i>`;
            additionalContentEdit += `</div>`;
            additionalContentEdit += `<input class="form-control" name="modalEmail${obj.id}" id="modalEmail${obj.id}" value="${obj.email}" type="email" required/>`;
            additionalContentEdit += `</div>`;
            additionalContentEdit += `<div class="col-md-7 col-sm-7 field">`
            additionalContentEdit += `<label for="modalPrimaryContact${obj.id}">Primary Contact :<span class="required">*</span></label>`
            additionalContentEdit += `<div class="flex">`
            additionalContentEdit += `<div class="w-25">`
            additionalContentEdit += `<select name="modalCountryCode${obj.id}" id="modalCountryCode${obj.id}" class="form-control px-1" required>`
            additionalContentEdit += `</select>`
            additionalContentEdit += `</div>`
            additionalContentEdit += `<div class="w-75">`
            additionalContentEdit += `<input class="form-control" name="modalPrimaryContact${obj.id}" id="modalPrimaryContact${obj.id}" value="${obj.primaryContact}" type="number" required/>`
            additionalContentEdit += `</div>`
            additionalContentEdit += `</div>`
            additionalContentEdit += `</div>`
            additionalContentEdit += `<div class="col-md-5 col-sm-5 field">`
            additionalContentEdit += `<label for="modalAlternateContact${obj.id}">Alternate Contact :</label>`
            additionalContentEdit += `<div class="field">`
            additionalContentEdit += `<input class="form-control" name="modalAlternateContact${obj.id}" id="modalAlternateContact${obj.id}" value="${obj.alternativeContact}" type="number"/>`
            additionalContentEdit += `</div>`
            additionalContentEdit += `</div>`
            additionalContentEdit += `</div>`
            additionalContentEdit += `</div>`

            $('#additionalContactSection').append(additionalContentEdit);
            
            setCountryCode(`modalCountryCode${obj.id}`).then(() => {
              $(`#modalCountryCode${obj.id} option`).each(function () {
                if ($(this).val() == obj.countryCode) {
                  $(this).prop("selected", true);
                }
              });
            }).catch((error) => {
              console.error("Error setting country codes:", error);
            });

          });

          $("#modalAddType option").each(function () {
            if ($(this).val() == dataObj["locationType"]) {
              $(this).prop("selected", true);
            }
          });

          if (readonlyVal == true) {
            $(".modal-footer").addClass("d-none");
            $("#clientOfc form").removeAttr("action");
            $("input, select, textarea", "#clientOfc").attr("readonly", true);
            console.log(readonlyVal)
          } else {
            $(".modal-footer").removeClass("d-none");
            $("#clientOfc form").attr(
              "action",
              `/gearBox/client/ofc/edit/save/${ofcId}/`
            );
          }
        })
        .catch((error) => {
          console.error("Error setting country codes:", error);
        });
    },
  });
  $("#clientOfc").modal("show");
}

// Client office view
$(".modalView").on("click", function () {
  let id = $(this).attr("id").replace("view", "");
  setModalWithData(id, (readonlyVal = true));
});

// Client office edit
$(".modalEdit").on("click", function () {
  let id = $(this).attr("id").replace("edit", "");
  setModalWithData(id, (readonlyVal = false));
});

// stuff related ONLY for this demo page:
$(".toggleValidationTooltips").change(function () {
    validator.settings.alerts = !this.checked;
    if (this.checked) $("form .alert").remove();
}).prop("checked", false);

// Client office add
$(".addOffice").on("click", function () {
  let clientId = $("#clientId").val();
  $("#clientOfc .modal-body input,#clientOfc .modal-body textarea,  #clientOfc .modal-body select").each(function () {
    $(this).val("");
  });
  $(".modal-footer").removeClass("d-none");


  additionalContent = ``
  additionalContent += `<div class="col-12 text-right my-1">`
  additionalContent += `<i class="fa-solid fa-circle-plus" onclick="addContact()"></i>`
  additionalContent += `</div>`
  additionalContent += `<div class="col-12 my-1 firstAdditionalFieldSet">`
  additionalContent += `<div class="row bg-light pb-3 border rounded">`
  additionalContent += `<div class="col-md-4 col-sm-4 field">`
  additionalContent += `<label for="modalPersonName1">Person name :<span class="required">*</span></label>`
  additionalContent += `<input class="form-control" name="modalPersonName1" id="modalPersonName1" type="text" required/>`
  additionalContent += `</div>`
  additionalContent += `<div class="col-md-8 col-sm-8 field">`
  additionalContent += `<label for="modalEmail1">Person Email :<span class="required">*</span></label>`
  additionalContent += `<input class="form-control" name="modalEmail1" id="modalEmail1" type="email" required/>`
  additionalContent += `</div>`
  additionalContent += `<div class="col-md-7 col-sm-7 field">`
  additionalContent += `<label for="modalPrimaryContact1">Primary Contact :<span class="required">*</span></label>`
  additionalContent += `<div class="flex">`
  additionalContent += `<div class="w-25">`
  additionalContent += `<select name="modalCountryCode1" id="modalCountryCode1" class="form-control px-1" required>`
  additionalContent += `</select>`
  additionalContent += `</div>`
  additionalContent += `<div class="w-75">`
  additionalContent += `<input class="form-control" name="modalPrimaryContact1" id="modalPrimaryContact1" type="number" required/>`
  additionalContent += `</div>`
  additionalContent += `</div>`
  additionalContent += `</div>`
  additionalContent += `<div class="col-md-5 col-sm-5 field">`
  additionalContent += `<label for="modalAlternateContact1">Alternate Contact :</label>`
  additionalContent += `<div class="field">`
  additionalContent += `<input class="form-control" name="modalAlternateContact1" id="modalAlternateContact1" type="number"/>`
  additionalContent += `</div>`
  additionalContent += `</div>`
  additionalContent += `</div>`
  additionalContent += `</div>`

  $("#additionalContactSection").empty().append(additionalContent)

  var select = $("#rateCards");
  select.val(null).trigger("change");
  $("#clientOfc form").attr(
    "action",
    `/gearBox/client/new/ofc/save/${clientId}/`
  );
  setCountryCode("modalAddCountry");
  setCountryCode("modalCountryCode1")
  $("#clientOfc").modal("show");
});

$("#modalForm").submit(function (e) {
  e.preventDefault();
  var hasEmptyField = false;

  $("input[required], textarea[required], select[required]").each(function () {
    if ($(this).val() == "" || $(this).val() == null) {
      hasEmptyField = true;
      $(this).css("border", "1px solid #CE5454");
    } else {
      $(this).css("border", "1px solid #ced4da");
    }
  });

  $('[id^="modalPrimary"]').each(function() {
    if(!checkPhone($(this))){
      hasEmptyField = true;
      $(this).css("border", "1px solid #CE5454");
    } else {
      $(this).css("border", "1px solid #ced4da");
    }
});

  // if (hasEmptyField || !checkPhone($("#modalPrimaryContact"))) {
  if(hasEmptyField) {
    return false;
  }
  this.submit();
});

function addContact(){
  let additionalCount = parseInt($("#additionalContactCount").val()) + 1;
  console.log(additionalCount);
  let contactDetails = ``;
  contactDetails += `<div class="col-12 my-1">`;
  contactDetails += `<div class="row bg-light pb-3 border rounded">`;
  contactDetails += `<div class="col-md-4 col-sm-4 field">`;
  contactDetails += `<label for="modalPersonName${additionalCount}">Person name :<span class="required">*</span></label>`;
  contactDetails += `<input class="form-control" name="modalPersonName${additionalCount}" id="modalPersonName${additionalCount}" type="text" required/>`;
  contactDetails += `</div>`;
  contactDetails += `<div class="col-md-8 col-sm-8 field">`;
  contactDetails += `<div class="flex justify-content-between">`;
  contactDetails += `<label for="modalEmail${additionalCount}">Person Email :<span class="required">*</span></label>`;
  contactDetails += `<i class="fa-solid fa-minus" onclick="removeContact(this)"></i>`;
  contactDetails += `</div>`;
  contactDetails += `<input class="form-control" name="modalEmail${additionalCount}" id="modalEmail${additionalCount}" type="email" required/>`;
  contactDetails += `</div>`;
  contactDetails += `<div class="col-md-7 col-sm-7 field">`
  contactDetails += `<label for="modalPrimaryContact${additionalCount}">Primary Contact :<span class="required">*</span></label>`
  contactDetails += `<div class="flex">`
  contactDetails += `<div class="w-25">`
  contactDetails += `<select name="modalCountryCode${additionalCount}" id="modalCountryCode${additionalCount}" class="form-control px-1" required>`
  contactDetails += `</select>`
  contactDetails += `</div>`
  contactDetails += `<div class="w-75">`
  contactDetails += `<input class="form-control" name="modalPrimaryContact${additionalCount}" id="modalPrimaryContact${additionalCount}" type="number" required/>`
  contactDetails += `</div>`
  contactDetails += `</div>`
  contactDetails += `</div>`
  contactDetails += `<div class="col-md-5 col-sm-5 field">`
  contactDetails += `<label for="modalAlternateContact${additionalCount}">Alternate Contact :</label>`
  contactDetails += `<div class="field">`
  contactDetails += `<input class="form-control" name="modalAlternateContact${additionalCount}" id="modalAlternateContact${additionalCount}" type="number"/>`
  contactDetails += `</div>`
  contactDetails += `</div>`
  contactDetails += `</div>`;
  contactDetails += `</div>`;
  setCountryCode(`modalCountryCode${additionalCount}`)
  $("#additionalContactCount").val(additionalCount);
  $('#additionalContactSection').append(contactDetails);
}

function removeContact(element) {
  $(element).closest('.col-12.my-1').remove();
}


// $('#additionalInfoForClient .fa-circle-plus').on('click', function(){

// })