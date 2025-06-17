// Search FAQ
function searchBtnClicked() {
    // Get Search Input
    var searchTermInput = document.getElementById("search_term");
    var searchTerm = searchTermInput.value;

    // Alphanumeric & Single Whitespace Regex
    searchTerm = searchTerm.replace(/[^a-zA-Z0-9\s]+/g, '');
    searchTerm = searchTerm.replace(/\s+/g, ' ');

    // Update URL to include GET['q'] Parameter
    window.location.href = 'home.php?q="' + searchTerm + '"';
}

// Function to View FAQ
function viewFaq(id) {
    // Fetch FAQ details from the server
    fetch(`../controllers/ViewFaqController.php?id=${id}`)
    .then(response => response.json())
    .then(data => {
        // Populate modal with data
        document.getElementById('r_question').value = data.question;
        document.getElementById('r_answer').value = data.answer;
        document.getElementById('r_category').value = data.category;
        document.getElementById('r_link').value = data.link;
    })
    .catch(error => {
        console.error("Error fetching service data:", error);
        alert("Unable to retrieve FAQ details. Please try again later.");
    });
}

// Function to Update FAQ
function updateFaq(id) {
    // Fetch FAQ details from the server
    fetch(`../controllers/ViewFaqController.php?id=${id}`)
    .then(response => response.json())
    .then(data => {
        // Populate modal with data
        document.getElementById('faqId').value = data.id;
        document.getElementById('u_question').value = data.question;
        document.getElementById('u_answer').value = data.answer;
        document.getElementById('u_category').value = data.category;
        document.getElementById('u_link').value = data.link;
    })
    .catch(error => {
        console.error("Error fetching service data:", error);
        alert("Unable to retrieve FAQ details. Please try again later.");
    });
}

// Function to Sync FAQ with Vector DB
async function syncFaq() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('syncModal'));
    // Fetch FAQ details from the server
    var response = await fetch(`../controllers/SyncFaqController.php?sync=1`);
    var responseVal = await response.json();

    if (responseVal.isSuccess) {
        alert('Sync successfully');
        window.location.reload(true); 
    } else {
        alert('Sync completed with failures/warnings. Please contact an Admin.');
        window.location.reload(true); 
    }
}

// Function to Update FAQ Entity
async function updateFaqForm() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('updateFaqModal'));

    // Get Form Data
    var faqId = document.getElementById('faqId').value;
    var question = document.getElementById('u_question').value.trim();
    var answer = document.getElementById('u_answer').value.trim();
    var category = document.getElementById('u_category').value.trim();
    var link = document.getElementById('u_link').value.trim();

    // Validate Form Data
    if (question === '' || answer === '' || category === '') {
        alert('Please fill in all fields.');
    } else {
        var form = document.getElementById('updateFaqForm');
    
        // Prepare Form Data
        var data = new FormData();
        data.append('id', faqId);
        data.append('question', question);
        data.append('answer', answer);
        data.append('category_id', category);

        if (link) {
            // If link is provided, append it to the form data
            data.append('link', link);
        }

        try {
            // Send POST Request
            const response = await fetch('../controllers/UpdateFaqController.php', {
                method: 'POST',
                body: data,
            });
            
            // Check Response Value
            const responseVal = await response.json();
            if (responseVal.isSuccess) {
                alert('FAQ updated successfully!');
                modal.hide()
                window.location.reload(true); 
            } else {
                alert('FAQ update failed, please try again later.');
                modal.hide();
                window.location.reload(true); 
            }
        } catch (error) {
            console.error("Error during FAQ update:", error);
            alert('FAQ update failed, please try again later.');
            modal.hide();
            window.location.reload(true); 
        }
    }
}

// Function to Delete FAQ
async function deleteFaq(id) {
    // Confirm Prompt
    if (confirm("Are you sure you want to delete this FAQ?")) {
        try {
            // Prepare Form Data
            var data = new FormData();
            data.append('id', id);

            // Send DELETE Request
            const response = await fetch(`../controllers/DeleteFaqController.php`, {
                method: 'POST',
                body: data,
            });

            // Check Response Value
            const responseVal = await response.json();
                if (responseVal.isSuccess) {
                alert('FAQ deleted successfully!');
                window.location.reload(true); 
            } else {
                alert('FAQ deletion failed, please try again later.');
                window.location.reload(true); 
            }
        } catch (error) {
            console.error("Error during FAQ deletion:", error);
            alert('FAQ deletion failed, please try again later.');
            window.location.reload(true); 
        }
    }
}