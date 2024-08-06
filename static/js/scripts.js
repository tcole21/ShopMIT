document.addEventListener("DOMContentLoaded", function() {
    const deleteButtons = document.querySelectorAll(".inlineButton");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function(event) {
            if (!confirm("Are you sure you want to delete this merchant?")) {
                event.preventDefault();
            }
        });
    });
});
