const csrftoken = $("[name=csrfmiddlewaretoken]").val();

function formatDate(date) {
  var year = date.getFullYear();
  var month = String(date.getMonth() + 1).padStart(2, '0');
  var day = String(date.getDate()).padStart(2, '0');
  return year + '-' + month + '-' + day;
}



function setDateRangeFun(checkbox) {
  var selectedValue = checkbox.value;
  $('#startDateDiv').addClass('d-none',true)
  $('#endDateDiv').addClass('d-none',true)
  $('#startDate').attr('readonly',true)
  if (selectedValue == "custom") {
    $('#startDate').removeAttr('readonly',true)
    $('#startDateDiv').removeClass('d-none',true)
    $('#endDateDiv').removeClass('d-none',true)
    $('#startDate').val("")
    $('#endDate').val("")
  }
  else if (selectedValue == "lastMonth") {
    var today = new Date();
    var lastMonthStartDate = new Date(today.getFullYear(), today.getMonth() - 1, 1);
    var lastMonthEndDate = new Date(today.getFullYear(), today.getMonth(), 0);

    // Format dates as YYYY-MM-DD for input fields
    var formattedStartDate = formatDate(lastMonthStartDate);
    var formattedEndDate = formatDate(lastMonthEndDate);

    $('#startDate').val(formattedStartDate);
    $('#endDate').val(formattedEndDate);
  }
  else if (selectedValue == "lastQuarter") {
    var today = new Date();
    var currentYear = today.getFullYear();
    var currentMonth = today.getMonth(); // Current month (0-indexed)

    // Calculate the start month and end month of the last quarter
    var endMonth = currentMonth - 1; // End month is the previous month

    // Adjust for the year change if the current month is January
    var startYear = currentYear;
    if (currentMonth < 2) {
        endMonth = 11; // December (0-indexed)
        startYear = currentYear - 1; // Adjust start year accordingly
    }

    var startMonth = endMonth - 2; // Calculate the start month based on the end month

    // Create Date objects for the start and end dates of the last quarter
    var quarterStartDate = new Date(startYear, startMonth, 1);
    var quarterEndDate = new Date(currentYear, endMonth + 1, 0); // Last day of the end month

    // Format dates as YYYY-MM-DD for input fields
    var formattedStartDate = formatDate(quarterStartDate);
    var formattedEndDate = formatDate(quarterEndDate);

    // Set the formatted dates to the input fields
    $('#startDate').val(formattedStartDate);
    $('#endDate').val(formattedEndDate);
  }

  else if (selectedValue == "lastYear") {
    var today = new Date();
    var lastFinancialYearStartDate, lastFinancialYearEndDate;

    // Check if the current month is before July (start of the fiscal year)
    if (today.getMonth() + 1 < 7) {
        // If the current month is before July, the last financial year started two years ago
        lastFinancialYearStartDate = new Date(today.getFullYear() - 2, 6, 1); // July is month index 6
        lastFinancialYearEndDate = new Date(today.getFullYear() - 1, 5, 30); // June 30th of the last year
    } else {
        // If the current month is after July, the last financial year started last year
        lastFinancialYearStartDate = new Date(today.getFullYear() - 1, 6, 1); // July is month index 6
        lastFinancialYearEndDate = new Date(today.getFullYear(), 5, 30); // June 30th of the current year
    }

    // Format dates as YYYY-MM-DD for input fields
    var formattedStartDate = formatDate(lastFinancialYearStartDate);
    var formattedEndDate = formatDate(lastFinancialYearEndDate);

    $('#startDate').val(formattedStartDate);
    $('#endDate').val(formattedEndDate);
}


  else if (selectedValue == "lastWeek") {
    var today = new Date();
    var currentDayOfWeek = today.getDay(); // Day of the week (0-indexed, Sunday = 0)

    // Calculate the difference between the current day and the previous Sunday
    var daysToSunday = currentDayOfWeek;
    var daysToSaturday = currentDayOfWeek + 6; // Add 6 days to get to Saturday

    // Calculate the start and end dates for the last week
    var lastSunday = new Date(today);
    lastSunday.setDate(today.getDate() - daysToSunday);

    var lastSaturday = new Date(today);
    lastSaturday.setDate(today.getDate() - daysToSaturday);

    // Format dates as YYYY-MM-DD for input fields
    var formattedEndDate = formatDate(lastSunday);
    var formattedStartDate = formatDate(lastSaturday);

    // Set the formatted dates to the input fields
    $('#startDate').val(formattedStartDate);
    $('#endDate').val(formattedEndDate);
  }

  if (selectedValue == "today") {
    var today = new Date();
    var formattedDate = formatDate(today); // Format today's date as YYYY-MM-DD

    // Set the start and end date inputs to today's date
    $('#startDate').val(formattedDate);
    $('#endDate').val(formattedDate);
  }
  else if (selectedValue == "yesterday") {
    var today = new Date();
    
    // Calculate yesterday's date
    var yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);

    // Format dates as YYYY-MM-DD for input fields
    var formattedDate = formatDate(yesterday);

    // Set yesterday's date to both start date and end date fields
    $('#startDate').val(formattedDate);
    $('#endDate').val(formattedDate);
  }

}


$(document).ready(function () {

  function checkDateValid() {
    var startDate = $("#startDate").val();
    var endDate = $("#endDate").val();
    flag = true;

    if (startDate == "") {
      $("#startDate").next(".errorMsg").removeClass("d-none");
      $("#startDate").addClass("isInvalid");
      flag = false;
    } else {
      $("#startDate").next(".errorMsg").addClass("d-none");
      $("#startDate").removeClass("isInvalid");
      flag = true;
    }

    if (endDate == "") {
      $("#endDate").next(".errorMsg").removeClass("d-none");
      $("#endDate").addClass("isInvalid");
      flag = false;
    } else {
      $("#endDate").next(".errorMsg").addClass("d-none");
      $("#endDate").removeClass("isInvalid");
      flag = true;
    }
    return flag;

  }
  
  

  var currentDate = new Date();
  var year = currentDate.getFullYear();
  var month = ("0" + (currentDate.getMonth() + 1)).slice(-2); // Adding 1 because months are zero-indexed
  var day = ("0" + currentDate.getDate()).slice(-2);
  var formattedDate = year + "-" + month + "-" + day;

  $("#startDate").attr("max", formattedDate);
  $("#endDate").attr("max", formattedDate);

  $("#startDate").on("change", function () {
    if ($(this).val() != "") {
      $("#endDate").removeAttr("readonly");
      $("#endDate").attr("min", $(this).val());
    }
  });
  
  // reconciliation
  $("#reconciliation").on("click", function (event) {
    event.preventDefault();
    if (checkDateValid()) {
      $("#signUpForm").submit();
    }
  }); 

});
