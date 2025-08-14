// Search Categories
function searchBtnClicked() {
    // Get Search Input
    var searchTermInput = document.getElementById("search_term");
    var searchTerm = searchTermInput.value;

    // Alphanumeric & Single Whitespace Regex
    searchTerm = searchTerm.replace(/[^a-zA-Z0-9\s]+/g, '');
    searchTerm = searchTerm.replace(/\s+/g, ' ');

    // Update URL to include GET['q'] Parameter
    window.location.href = 'categories.php?q="' + searchTerm + '"';
}

// Delete Category
async function deleteCategory(id) {
    // Confirm Prompt
    if (confirm("Are you sure you want to delete this category & associated vectors?")) {
        try {
            // Prepare Form Data
            var data = new FormData();
            data.append('id', id);

            // Send DELETE Request
            const response = await fetch('../controllers/DeleteCategoryController.php', {
                method: 'POST',
                body: data,
            });

            // Check Response Value
            const responseVal = await response.json();
            if (responseVal.isSuccess) {
                alert('Category deleted successfully!');
                window.location.reload(true);
            } else {
                alert('Category deletion failed, please try again later.');
                window.location.reload(true);
            }
        } catch (error) {
            console.error("Error during Category deletion:", error);
            alert('Unknown error occured during Category deletion, please try again later.');
            window.location.reload(true);
        }
    }
}

// Create Category
async function createCategory() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('createCategoryModal'));

    // Get Form Data
    var category = document.getElementById("category_name").value.trim();

    // Validate Form Data
    if (category === '') {
        alert('Category cannot be empty');
    }
    else {
        // Confirm Prompt
        if (confirm("Create new Category?")) {
            try {
                // Prepare Form Data
                var data = new FormData();
                data.append('category_name', category);

                // Send DELETE Request
                const response = await fetch('../controllers/CreateCategoryController.php', {
                    method: 'POST',
                    body: data,
                });

                // Check Response Value
                const responseVal = await response.json();
                if (responseVal.isSuccess) {
                    alert('Category created successfully!');
                    modal.hide();
                    window.location.reload(true);
                } else {
                    alert('Category creation failed, please try again later.');
                    modal.hide();
                    window.location.reload(true);
                }
            } catch (error) {
                console.error("Error during creation:", error);
                alert('Unknown error occured during creation, please try again later.');
                modal.hide();
                window.location.reload(true);
            }
        } else {
            modal.hide();
        }
    }
}