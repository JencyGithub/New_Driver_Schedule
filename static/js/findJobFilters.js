const csrftoken = $("[name=csrfmiddlewaretoken]").val();

function getDataFilter(startDate, endDate, selectedStatus) {
  $.ajax({
    url: "/account/job/selectedStatus/",
    method: "POST",
    data: {
        selectedStatus: selectedStatus,
        startDate: startDate,
        endDate: endDate,
    },
    beforeSend: function (xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function (data) {
      setDataInTable("datatable-buttons", data.data);
    },
  });
}

function setDataInTable(tableId, data) {
  var table = $(`#${tableId}`).DataTable();
  table.clear().draw();
  $.each(data, function (index, item) {
    table.row
      .add([
        item.Status,
        item.Title,
        item.Start_Date_Time,
        item.End_Date_Time,
        '<div class="d-flex justify-content-around">' +
          '<a href="/appointment/appointmentForm/view/' +
          item.id +
          '" title="View appointment">' +
          '<i class="fa-regular fa-eye" style="font-size:1.3rem"></i>' +
          "</a>" +
          '<a href="/appointment/appointmentForm/update/' +
          item.id +
          '/?update=1" title="Edit appointment">' +
          '<i class="fa-solid fa-file-pen" style="font-size:1.3rem"></i>' +
          "</a>" +
          "</div>",
      ])
      .draw();
  });
}

$(document).ready(function () {
  $("#datatable-buttons").DataTable();

  $("#multiSelect").select2({
    placeholder: "Select status",
  });

  var predefinedRanges = {
    Today: [moment(), moment()],
    Yesterday: [moment().subtract(1, "days"), moment().subtract(1, "days")],
    "This Month": [moment().startOf("month"), moment().endOf("month")],
    "This Year": [moment().startOf("year"), moment().endOf("year")],
  };

  // Set default date range to the last 7 days
  var defaultStartDate = moment().subtract(1, "days");
  var defaultEndDate = moment();

  // Initialize the DateRangePicker with predefined ranges
  dateRangePickerInstance= $("#dateRangePicker").daterangepicker({
    ranges: predefinedRanges,
    opens: "left",
    startDate: defaultStartDate,
    endDate: defaultEndDate,
    placeholder: "Select Date",
  });

  // Optionally, define a callback function when the user applies the date range
  $("#dateRangePicker").on("apply.daterangepicker", function (ev, picker) {
    let startDate = picker.startDate.format("YYYY-MM-DD");
    let endDate = picker.endDate.format("YYYY-MM-DD");
    let selectedStatus = $("#multiSelect").val();

    getDataFilter(startDate, endDate, selectedStatus);

    // console.log('Start Date: ' + picker.startDate.format('YYYY-MM-DD'));
    // console.log('End Date: ' + picker.endDate.format('YYYY-MM-DD'));
  });
  
  // Event listener for changes in the selected values
  $("#multiSelect").on("change", function () {

    var startDate = $('#dateRangePicker').data('daterangepicker').startDate.format('YYYY-MM-DD');
    var endDate = $('#dateRangePicker').data('daterangepicker').endDate.format('YYYY-MM-DD');

    var selectedStatus = $(this).val();
    console.log(selectedStatus)
    getDataFilter(startDate, endDate, selectedStatus);
    /*

    $.ajax({
      url: "/account/job/selectedStatus/",
      method: "POST",
      data: {
        selectedStatus: selectedStatus,
      },
      beforeSend: function (xhr) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      },
      success: function (data) {
        setDataInTable("datatable-buttons", data.data);
      },
    });
    */
  });
});
