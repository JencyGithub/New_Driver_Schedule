const csrftoken = $("[name=csrfmiddlewaretoken]").val();

$(document).ready(function () {
  if (!$("#verified").val()) {
    $(":input , select").prop("disabled", true);
    $("#verified").css("display", "none");
  }
});

$('.ormBtn').on('click', function(){
  let element = $(this)
  let elementId = $(this).attr('id').replace('orm', '')

  element.html('Loading...');
  $.ajax({
    type: "POST",
    url: "/account/orm/read/",
    data: {
      docketId: elementId
    },
    beforeSend: function (xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function (data) {
      element.html('ORM');
      if (data.status) {
        $(`#ormTextArea${elementId}`).val(`${data.docketData}`)
      }else{
        alert(data.e)
      }
    },
  });
})

function hideshow() {
  var password = document.getElementById("password1");
  var slash = document.getElementById("slash");
  var eye = document.getElementById("eye");

  if (password.type === "password") {
    password.type = "text";
    slash.style.display = "block";
    eye.style.display = "none";
  } else {
    password.type = "password";
    slash.style.display = "none";
    eye.style.display = "block";
  }
}
// A "<form>" element is optionally passed as an argument, but is not a must
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
  console.log(validatorResult);
  return !!validatorResult.valid;
};
// on form "reset" event
document.forms[0].onreset = function (e) {
  validator.reset();
};
// stuff related ONLY for this demo page:
$(".toggleValidationTooltips")
  .change(function () {
    validator.settings.alerts = !this.checked;
    if (this.checked) $("form .alert").remove();
  })
  .prop("checked", false);

  function showBreaks(shiftId){
      $("#driverBreaks").modal("show");
      $.ajax({
        type: "POST",
        url: "/account/get/driver/break/",
        data: {
            shiftId: shiftId
        },
        beforeSend: function (xhr) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (data) {
          if (data.status) {

            tableData = ''
            if(data.driverBreaks.length > 0){
                data.driverBreaks.forEach(function(breakObj) {
                    tableData += `<tr>`
                    tableData += `<td>${breakObj['startDateTime']}</td>`
                    tableData += `<td>${breakObj['endDateTime']}</td>`
                    tableData += `<td>${breakObj['description']}</td>`
                    tableData += `</tr>`
                });
            }else{
              tableData += `<tr><td><h6 class="text-secondary">No breaks found</h6></td></tr>`
            }
            $('#driverBreaks tbody').empty().append(tableData);
          }
        },
      });
  }

function checkDeficitFun(shiftObj) {  
  let selected = $(`#verified`).is(":checked");
  if (selected){
    $.ajax({
      type: "POST",
      url: "/account/check/trip/deficit",
      data: {
          shiftId: shiftObj
      },
      beforeSend: function (xhr) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      },
      success: function (data) {
        if (data.status) {
          if (data.getDeficit.length > 0) {
            let deficitMessage = "Total Deficit with Trip:\n";
            data.getDeficit.forEach(function(deficit) {
              deficitMessage += `${deficit.get_deficit}: ${deficit.deficit_value}\n`;
            });
            alert(deficitMessage);
          }
        }
      },
    });
  }

}
$("#driverBreaks .close").on("click", function(){
    console.log('close')
    $('#driverBreaks').modal('hide');
})

function returnToYard(id, tag) {
  let selected = $(`#${tag.id}`).is(":checked");

  if (selected) {
    $(`#returnQty${id}`).removeAttr("readonly");
    $(`#returnKm${id}`).removeAttr("readonly");
  } else {
    $(`#returnQty${id}`).attr("readonly", true);
    $(`#returnKm${id}`).attr("readonly", true);
  }
}

function resetRadio(id) {
  $(`#tippingToYard${id}`).removeAttr("checked");
  $(`#returnToYard${id}`).removeAttr("checked");
  $(`#returnQty${id}`).attr("readonly", true);
  $(`#returnKm${id}`).attr("readonly", true);
}
function waitingCheck(id, tag) {
  let selected = $(`#${tag.id}`).is(":checked");

  if (selected) {
    $(`#waitingTimeStart${id}`).removeAttr("readonly").attr("required", true);
    $(`#waitingTimeEnd${id}`).attr("required", true);
  } else {
    $(`#waitingTimeStart${id}`).attr("readonly", true);
    $(`#waitingTimeStart${id}`).removeAttr("required").val("");
    $(`#waitingTimeEnd${id}`).removeAttr("required").val("");
    $(`#totalWaitingInMinute${id}`).removeAttr("required").val("");
  }
}
function standByCheck(id, tag) {
  let selected = $(`#${tag.id}`).is(":checked");

  if (selected) {
    $(`#standByStartTime${id}`).removeAttr("readonly").attr("required", true);
    $(`#standByEndTime${id}`).attr("required", true);
  } else {
    $(`#standByStartTime${id}`)
      .attr("readonly", true)
      .removeAttr("required")
      .val("");
    $(`#standByEndTime${id}`)
      .attr("readonly", true)
      .removeAttr("required")
      .val("");
    $(`#standBySlot${id}`).removeAttr("required").val("");
  }
}
function openWaitingTimeEnd(lineData, count_) {
  let waitingTimeStart = lineData.value;
  if (waitingTimeStart) {
    $(`#waitingTimeEnd${count_}`).removeAttr("readonly");
  }
}
function openStandByEnd(lineData, count_) {
  let standByEndTime = lineData.value;
  if (standByEndTime) {
    $(`#standByEndTime${count_}`).removeAttr("readonly");
  }
}
function docketUpdate(docketId) {
  let docketId_ = docketId;
  let docketNumber_ = $(`#docketNumber_${docketId_}`).val();
  console.log(docketNumber_);
  if (docketId) {
    $.ajax({
      type: "POST",
      url: "/account/driverTrip/docket/update/",
      data: {
        docketId: docketId_,
        docketNumber: docketNumber_,
      },
      beforeSend: function (xhr) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      },
      success: function (data) {
        if (data.status) {
          alertify.success("Update Successfully..");
          location.reload();
        } else {
          alert("DocketNumber must be unique");
        }
      },
    });
  }
}
function countTotalWaitingTime(lineData, count_, tripId) {
  let waitingTimeStart = $(`#waitingTimeStart${count_}`).val();
  let docketNumber = $(`#docketNumber${count_}`).val();
  let waitingTimeEnd = lineData.value;
  if (waitingTimeStart && waitingTimeEnd) {
    $.ajax({
      type: "POST",
      url: "/account/driverDocket/waitingTime/count/",
      data: {
        tripId: tripId,
        waitingTimeEnd: waitingTimeEnd,
        waitingTimeStart: waitingTimeStart,
        docketId:count_,
      },
      beforeSend: function (xhr) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      },
      success: function (data) {
        console.log(data.totalWaitingTime);
        $(`#totalWaitingInMinute${count_}`).val(data.totalWaitingTime);
      },
    });
  }
}

function countStandBySlot(lineData, count_, tripId) {
  let standByStartTime = $(`#standByStartTime${count_}`).val();
  let standByEndTime = $(`#standByEndTime${count_}`).val();

  if (standByStartTime && standByEndTime) {
    $.ajax({
      type: "POST",
      url: "/account/driverDocket/standByTime/count/",
      data: {
        tripId: tripId,
        standByStartTime: standByStartTime,
        standByEndTime: standByEndTime,
      },
      beforeSend: function (xhr) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      },
      success: function (data) {
        console.log(data.totalWaitingTime);
        $(`#standBySlot${count_}`).val(data.standBySlot);
      },
    });
  }
}
