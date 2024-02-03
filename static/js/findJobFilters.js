const csrftoken = $("[name=csrfmiddlewaretoken]").val();

$(document).ready(function () {
  $("#multiSelect").select2({
    placeholder: "Select status",
    templateResult: formatOption,
  });

  $("#multiSelect").on("change", function () {
    var selectedStatus = $(this).val();
    // // console.log(selectedStatus);
    getDataFilter(selectedStatus);
  });


  $("#closeBtn").on('click', function(){
    $('#appointmentModel').modal('hide');
  })
  getDataFilter(null);

  $('#cancleJonBtn').on('click', function(){
    $('#cancelModel').modal('show');
  })
});

function getDataFilter(selectedStatus) {
  $.ajax({
    url: "/appointment/get/driver-appointment/",
    method: "POST",
    data: {
      selectedStatus: selectedStatus,
    },
    beforeSend: function (xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function (data) {
      if (data.status) {
        setCalendar(data);
      }
    },
  });
}

function getColorBasedOnStatus(status) {
  if (status === "Unassigned") {
    return "#E74C3C"; 
  } else if (status === "Assigned") {
    return "#ff8700"; 
  } else if (status === "Dispatched") {
    return "#0084DD"; 
  } else if (status === "InProgress") {
    return "#00B140"; 
  } else if (status === "Incomplete") {
    return "#0e6211"; 
  } else if (status === "Complete") {
    return "#A9A9A9"; 
  } else if (status === "Cancelled") {
    return "#000"; 
  }
}

function setCalendar(data) {
  var calendarEl = document.getElementById("calendar");
  var calendar = new FullCalendar.Calendar(calendarEl, {
    headerToolbar: {
      left: "today resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth,resourceTimelineYear,list",
      center: "title",
      right: "prev,next",
    },
    aspectRatio: 1.6,
    initialView: "resourceTimelineDay",
    resourceAreaWidth: "20%",
    selectable: true,
    selectHelper: true,
    eventLimit: true,
    select: function (start, end, jsEvent, view) {
      // console.log("Selected: " + start + " to " + end);
      alert("Selected: " + start + " to " + end);
    },
    resources: data.drivers, 
    events: data.appointments, 

    eventContent: function (arg) {
      var color = getColorBasedOnStatus(arg.event.extendedProps.status);
      var html = $("<div>", {
        class: "event-container px-1 py-2",
        style:
          "background-color: " + color + "; border:1px solid " + color + ";",
      }).append(
        $("<div>", {
          class: "event-title",
          text: arg.event.title,
        })
      );

      return { html: html[0].outerHTML };
    },
    eventClick: function (info) {
      var eventId = info.event._def.publicId;
      // // console.log(info.event._def.publicId);
      // alert(info.event._def.title);
      showAppointment(eventId)
    },
  });
  calendar.render();
}

function formatOption(option) {
  if (!option.id) {
    return option.text;
  }
  var $option = $(
    '<span><span class="badge" style="background-color:' +
      $(option.element).data("badge-color") +
      ';width:15px;height:15px;display-inline-block;"> </span> ' +
      option.text +
      "</span>"
  );
  return $option;
}

function cancelJob(appointmentId){
  $.ajax({
    url: "/appointment/cancelJob/",
    method: "POST",
    data: {
      appointmentId: appointmentId,
    },
    beforeSend: function (xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function (data) {
      if (data.status) {
        location.reload();
      }else{
        alert('Something went wrong, please try again.')
      }
    },
  });
}

function showAppointment(appointmentId){
  $.ajax({
    url: "/appointment/get/single/appointment/",
    method: "POST",
    data: {
      appointmentId: appointmentId,
    },
    beforeSend: function (xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function (data) {
      if (data.status) {
        // // console.log(data.appointmentObj);
        $('#appTitle').text(data.appointmentObj.Title);
        $('#appStartDateTime').text(data.appointmentObj.Start_Date_Time);
        $('#appEndDateTime').text(data.appointmentObj.End_Date_Time);
        $('#appReportOrigin').text(data.appointmentObj.report_to_origin);
        $('#appStatus').text(data.appointmentObj.Status);
        $('#appOrigin').text(data.appointmentObj.Origin_id);
        $('#appStaffNotes').text(data.appointmentObj.Staff_Notes);
        $('#appShiftType').text(data.appointmentObj.shiftType);
        $('#appCreatedBy').text(data.appointmentObj.Created_by_id);
        $('#appCreatedTime').text(data.appointmentObj.Created_time);
        $('#appPreStart').text(data.appointmentObj.preStartWindow);

        $('#truckNum').text(data.truckObj.adminTruckNumber);

        $('#driverName').text(data.driverObj.name);
        $('#driverPhone').text(data.driverObj.phone);
        $('#driverEmail').text(data.driverObj.email);

        $('#originBasePlant').text(data.originObj.basePlant);
        $('#originAddress').text(data.originObj.address);
        $('#originPhone').text(data.originObj.phone);
        $('#originPersonOnName').text(data.originObj.personOnName);
        $('#originManagerName').text(data.originObj.managerName);

        $('#editBtn').attr('href',`/appointment/appointmentForm/update/view/${appointmentId}/1/`)
        $('#cancelModel #yes').attr('onClick', `cancelJob(${appointmentId})`)
        $('#appointmentModel').modal('show');
      }
    },
  });
}
