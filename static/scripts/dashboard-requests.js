let requests = [];

async function loadRequests() {
  try {
    const response = await fetch("/api/admin/ticket-requests?status=pending");
    const data = await response.json();

    if (data.status === "ok") {
      requests = data.requests;
      renderRequests();
    }
  } catch (error) {
    console.error("Erreur lors du chargement des demandes:", error);
    document.getElementById("requests-container").innerHTML = `
      <div class="text-center text-red-500 py-8">
        <p>Erreur lors du chargement des demandes</p>
      </div>
    `;
  }
}

function formatDate(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now - date;
  const diffMins = Math.floor(diffMs / 60000);

  if (diffMins < 1) return "À l'instant";
  if (diffMins < 60) return `Il y a ${diffMins} min`;
  if (diffMins < 1440) return `Il y a ${Math.floor(diffMins / 60)}h`;
  return date.toLocaleDateString("fr-FR", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
}

function renderRequests() {
  const container = document.getElementById("requests-container");

  if (requests.length === 0) {
    container.innerHTML = `
      <div class="text-center text-gray-500 py-8">
        <p>Aucune demande en attente</p>
      </div>
    `;
    return;
  }

  container.innerHTML = requests.map((req) => {
    const statusClass = req.status === "pending" 
      ? "bg-orange-500/20 text-orange-400" 
      : req.status === "validated"
      ? "bg-emerald-500/20 text-emerald-400"
      : "bg-red-500/20 text-red-400";

    return `
      <div class="glass rounded-xl p-4 neon-border-blue mb-4" data-request-id="${req.id}">
        <div class="flex justify-between items-center mb-3">
          <span class="status-pill ${statusClass} uppercase">${req.status === "pending" ? "En attente" : req.status === "validated" ? "Validé" : "Refusé"}</span>
          <span class="text-[10px] text-gray-500">${formatDate(req.created_at)}</span>
        </div>

        <div class="mb-3">
          <p class="text-xs font-bold text-white mb-1">
            Plan choisi :
            <span class="text-purple-400 font-black">${req.category_price} - ${req.category_name}</span>
          </p>
          <p class="text-[10px] text-gray-400 mb-2">
            Client : <span class="text-white font-semibold">${req.client_name}</span> | 
            Téléphone : <span class="text-white font-semibold">${req.client_phone}</span>
          </p>

          ${req.sms_content ? `
            <div class="sms-box text-orange-200 mb-2">
              "${req.sms_content}"
            </div>
          ` : ""}

          ${req.ticket_access_key ? `
            <div class="bg-emerald-900/30 border border-emerald-500/50 rounded-lg p-3 mb-2">
              <p class="text-[10px] text-emerald-300 mb-1">Code ticket validé :</p>
              <p class="text-lg font-mono font-bold text-emerald-400">${req.ticket_access_key}</p>
            </div>
          ` : ""}
        </div>

        ${req.status === "pending" ? `
          <div class="grid grid-cols-2 gap-3">
            <button
              onclick="validateRequest('${req.id}')"
              class="bg-emerald-600 py-3 rounded-lg text-xs font-bold uppercase hover:bg-emerald-500 transition-all"
            >
              ✅ Valider
            </button>
            <button
              onclick="refuseRequest('${req.id}')"
              class="bg-gray-800 py-3 rounded-lg text-xs font-bold uppercase hover:bg-red-900 transition-all"
            >
              ❌ Rejeter
            </button>
          </div>
        ` : req.status === "validated" && req.ticket_access_key ? `
          <div class="flex gap-2">
            <a
              href="https://wa.me/${req.client_phone.replace(/\s+/g, "")}?text=${encodeURIComponent(`Votre code ticket Wi-Fi: ${req.ticket_access_key}`)}"
              target="_blank"
              class="flex-1 bg-emerald-600 py-2 rounded-lg text-xs font-bold uppercase hover:bg-emerald-500 transition-all text-center"
            >
              📱 Envoyer via WhatsApp
            </a>
            <a
              href="sms:${req.client_phone.replace(/\s+/g, "")}?body=${encodeURIComponent(`Votre code ticket Wi-Fi: ${req.ticket_access_key}`)}"
              class="flex-1 bg-blue-600 py-2 rounded-lg text-xs font-bold uppercase hover:bg-blue-500 transition-all text-center"
            >
              💬 Envoyer via SMS
            </a>
          </div>
        ` : ""}
      </div>
    `;
  }).join("");
}

async function validateRequest(requestId) {
  try {
    const response = await fetch(`/api/admin/validate-request/${requestId}`, {
      method: "POST",
    });

    const data = await response.json();

    if (data.status === "ok") {
      alert("Demande validée avec succès !");
      loadRequests();
    } else {
      alert("Erreur: " + (data.message || "Une erreur est survenue"));
    }
  } catch (error) {
    console.error("Erreur:", error);
    alert("Une erreur est survenue. Veuillez réessayer.");
  }
}

async function refuseRequest(requestId) {
  if (!confirm("Êtes-vous sûr de vouloir refuser cette demande ?")) {
    return;
  }

  try {
    const response = await fetch(`/api/admin/refuse-request/${requestId}`, {
      method: "POST",
    });

    const data = await response.json();

    if (data.status === "ok") {
      alert("Demande refusée.");
      loadRequests();
    } else {
      alert("Erreur: " + (data.message || "Une erreur est survenue"));
    }
  } catch (error) {
    console.error("Erreur:", error);
    alert("Une erreur est survenue. Veuillez réessayer.");
  }
}

// Charger les demandes au chargement de la page
document.addEventListener("DOMContentLoaded", () => {
  loadRequests();
  // Recharger toutes les 10 secondes
  setInterval(loadRequests, 10000);
});
