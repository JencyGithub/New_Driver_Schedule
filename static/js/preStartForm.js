$(document).ready(function () {
  $("#addQuestions").click(function () {
    var preStartName= $("#preStartName").val().trim();
    var questionCount = $("#queCount").val();
    if (questionCount && !isNaN(questionCount) && questionCount > 0 && preStartName != "" ) {
      $("#questionsContainer").empty();

      for (var i = 1; i <= questionCount; i++) {
        var questionSection = `
                <div class="x_panel mt-2">
                    <div class="container">
                        <div class="row">
                            <div class="col-md-8">
                                <div class="form-group">
                                    <label for="q${i}txt" class="label-align">Question ${i}:<span class="required">*</span></label>
                                    <input class="form-control" name="q${i}txt" required="required" id="q${i}txt" type="text" />
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label for="q${i}type" class="label-align">Question Type:<span class="required">*</span></label>
                                    <select name="q${i}type" id="q${i}type" class="form-control" required="required">
                                        <option value="Driver related">Driver related</option>
                                        <option value="Vehicle related">Vehicle related</option>
                                        <option value="Other">Other</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="form-group">
                                    <label for="q${i}o1" class="label-align">Option 1:<span class="required">*</span></label>
                                    <div class="form-check float-right">
                                        <input class="form-check-input" type="radio" value="q${i}o1wantFile" id="q${i}o1wantFile" name="wantFile${i}">
                                        <label class="form-check-label text-default" for="q${i}o1wantFile">
                                            Want file
                                        </label>
                                    </div>
                                    <input class="form-control" name="q${i}o1" required="required" id="q${i}o1" type="text" autocomplete="off"/>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="form-group">
                                    <label for="q${i}o2" class="label-align">Option 2:</label>
                                    <div class="form-check float-right">
                                        <input class="form-check-input" type="radio" value="q${i}o2wantFile" id="q${i}o2wantFile" name="wantFile${i}">
                                        <label class="form-check-label text-default" for="q${i}o2wantFile">
                                            Want file
                                        </label>
                                    </div>
                                    <input class="form-control" name="q${i}o2" id="q${i}o2" type="text" autocomplete="off"/>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="form-group">
                                    <label for="q${i}o3" class="label-align">Option 3:</label>
                                    <div class="form-check float-right">
                                        <input class="form-check-input" type="radio" value="q${i}o3wantFile" id="q${i}o3wantFile" name="wantFile${i}">
                                        <label class="form-check-label text-default" for="q${i}o3wantFile">
                                            Want file
                                        </label>
                                    </div>
                                    <input class="form-control" name="q${i}o3" id="q${i}o3" type="text" autocomplete="off"/>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="form-group">
                                    <label for="q${i}o4" class="label-align">Option 4:</label>
                                    <div class="form-check float-right">
                                        <input class="form-check-input" type="radio" value="q${i}o4wantFile" id="q${i}o4wantFile" name="wantFile${i}">
                                        <label class="form-check-label text-default" for="q${i}o4wantFile">
                                            Want file
                                        </label>
                                    </div>
                                    <input class="form-control" name="q${i}o4" id="q${i}o4" type="text" autocomplete="off"/>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                `;
        $("#questionsContainer").append(questionSection);
        $("#preStartName").attr('readonly', true);
        $("#queCount").attr('readonly', true)
      }
      $("#submit").attr("type", "submit");
    } else {
      alert("Pre-start name and Question count must me filled.");
    }
  });
});
