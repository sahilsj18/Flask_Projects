document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".task-checkbox").forEach(checkbox => {
        checkbox.addEventListener("change", () => {
            fetch(`/update/${checkbox.dataset.id}`, {
                method: "POST",
                body: JSON.stringify({ completed: checkbox.checked }),
                headers: { "Content-Type": "application/json" }
            });
        });
    });

    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", () => {
            fetch(`/delete/${button.dataset.id}`, { method: "POST" })
                .then(() => location.reload());
        });
    });
});
