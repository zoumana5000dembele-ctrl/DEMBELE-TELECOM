const submitButton = document.getElementById("update-stock-button");
const ticketAccessKeysInput = document.getElementById("ticket-access-keys");
const ticketCategoryIdInput = document.getElementById("ticket-category-select");

async function addTickets() {
    try {
      const response = await fetch("/api/add-tickets", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ticket_access_keys: ticketAccessKeysInput.value,
          ticket_category_id:ticketCategoryIdInput.value
        }),
      });
      if (response.ok) {
        const result = await response.json();
        alert("Tickets added successfully! \nVeuillez rafraichir la page.");
               console.log(result);
      } else {
        alert("Failed to add tickets.");
        console.error("Error:", response.statusText);
      }
    } catch (error) {
      alert("An error occurred while adding tickets.");
      console.error("Error:", error);
    }
}

submitButton?.addEventListener("click", addTickets);

