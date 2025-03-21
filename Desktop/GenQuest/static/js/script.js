$(document).ready(function () {
    $("#pdfUpload").change(function () {
        var file = $("#pdfUpload")[0].files[0];

        if (file) {
            var formData = new FormData();
            formData.append("pdf", file);

            // Show loader while uploading
            $("#uploadStatus").html("Uploading... ⏳").css("color", "blue");

            $.ajax({
                url: "/upload",
                type: "POST",
                data: formData,
                processData: false,
                contentType: false,
                success: function (response) {
                    $("#uploadStatus").text("✅ File uploaded successfully!").css("color", "lightgreen");
                    $("#generateBtn").prop("disabled", false);  // Enable generate button
                },
                error: function (response) {
                    $("#uploadStatus").text("❌ " + response.responseJSON.error).css("color", "red");
                    $("#generateBtn").prop("disabled", true);  // Keep generate button disabled
                }
            });
        }
    });

    $("#generateBtn").click(function () {
        var questionType = $("#questionType").val();
        var difficulty = $("#difficulty").val();
        var textInput = $("#textInput").val().trim();
        var fileUploaded = $("#uploadStatus").text().includes("File uploaded successfully!");
    
        if (!textInput && !fileUploaded) {
            alert("❌ Please upload a valid PDF or enter text before generating questions.");
            return;
        }
    
        $.ajax({
            url: "/generate",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                questionType: questionType,
                difficulty: difficulty,
                textInput: textInput  // Send input text
            }),
            success: function (data) {
                alert("✅ " + data.message);
                window.location.href = "/output";  // Redirect to output.html
            },
            error: function (xhr) {
                alert("❌ Error: " + xhr.responseText);
            }
        });
    });
    

    $(document).ready(function () {
        $("#generateBtn").click(function () {
            var questionType = $("#questionType").val();
            var difficulty = $("#difficulty").val();
            var textInput = $("#textInput").val().trim();
            var fileUploaded = $("#uploadStatus").text().includes("File uploaded successfully!");
    
            if (!textInput && !fileUploaded) {
                alert("❌ Please upload a valid PDF or enter text before generating questions.");
                return;
            }
    
            // Show the loader and disable button
            $("#loadingIndicator").show();
            $("#generateBtn").prop("disabled", true).text("Generating...");
    
            $.ajax({
                url: "/generate",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({
                    questionType: questionType,
                    difficulty: difficulty,
                    textInput: textInput  // Send user input text
                }),
                success: function (data) {
                    alert("✅ " + data.message);
                    window.location.href = "/output";  // Redirect to output.html
                },
                error: function (xhr) {
                    alert("❌ Error: " + xhr.responseText);
                },
                complete: function () {
                    // Hide loader and re-enable button after request completes
                    $("#loadingIndicator").hide();
                    $("#generateBtn").prop("disabled", false).text("Generate Questions");
                }
            });
        });
    });
    


    // Smooth Scroll for Navbar Links
    $(".nav-link").on("click", function(event) {
        if (this.hash !== "") {
            event.preventDefault();
            var hash = this.hash;
            $("html, body").animate(
                { scrollTop: $(hash).offset().top },
                800
            );
        }
    });

    // Theme Toggle
    const themeToggle = document.getElementById("themeToggle");

    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
        themeToggle.innerHTML = "☀️";
    }

    themeToggle.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {
            themeToggle.innerHTML = "☀️";
            localStorage.setItem("theme", "dark");
        } else {
            themeToggle.innerHTML = "🌙";
            localStorage.setItem("theme", "light");
        }
    });
});
