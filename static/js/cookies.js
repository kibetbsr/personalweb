document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("law-container");
    const form = document.getElementById("law-form");
    const numberInput = document.getElementById("law-number");
    const statementInput = document.getElementById("law-statement");

    // Fetch and display laws
    function fetchLaws() {
        fetch("http://127.0.0.1:8000/api/laws/")
            .then(response => response.json())
            .then(data => {
                container.innerHTML = ""; // Clear previous laws
                data.forEach(displayLaw);
            })
            .catch(error => console.error("Error fetching laws:", error));
    }

    // Function to display a single law
    function displayLaw(law) {
        const lawCard = document.createElement("div");
        lawCard.classList.add("law-card");

        const lawNumber = document.createElement("h3");
        lawNumber.textContent = `Law ${law.number}`;

        const lawStatement = document.createElement("p");
        lawStatement.textContent = law.statement;

        lawCard.appendChild(lawNumber);
        lawCard.appendChild(lawStatement);
        container.appendChild(lawCard);
    }

    fetchLaws(); // Load laws on page load

    // Add a new law and display it immediately
    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const number = numberInput.value.trim();
        const statement = statementInput.value.trim();

        if (!number || !statement) {
            alert("Both fields are required!");
            return;
        }

        const newLaw = { number: parseInt(number), statement };

        fetch("http://127.0.0.1:8000/api/laws/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newLaw)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to add law. Maybe the number already exists?");
            }
            return response.json();
        })
        .then(data => {
            displayLaw(data); // Show the newly added law immediately
            form.reset(); // Clear input fields
        })
        .catch(error => alert(error.message));
    });
});
