// Function to Create FAQ Entity
function submitForm() {

    var form = document.querySelector("form");
    var q = document.getElementById('question').value.trim();
    var a = document.getElementById('answer').value.trim();
    
    var isValid = true;

    // Validate Form Data
    if (!q) {
        isValid = false;
        document.getElementById('question_val').innerText =
            "Please enter a valid question.";
    } else if (q.length > 1000){
        isValid = false;
        document.getElementById('question_val').innerText =
            "Question is too long, please keep it under 1000 characters";
    } else {
        document.getElementById('question_val').innerText = "";
    }

    if (!a) {
        isValid = false;
        document.getElementById('answer_val').innerText =
            "Please enter a valid answer.";
    } else if (a.length > 1000){
        isValid = false;
        document.getElementById('answer_val').innerText =
            "Answer is too long, please keep it under 1000 characters";
    } else {
        document.getElementById('answer_val').innerText = "";
    }

    if (isValid) {
        if (confirm("Confirm Create FAQ Entry?")) {
          form.submit();
        }
    }
}