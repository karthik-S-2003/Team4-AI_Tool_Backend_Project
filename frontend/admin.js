const API = "http://127.0.0.1:800";
let token = localStorage.getItem("admin_token") || "";

/* =========================
   UI VISIBILITY HELPERS
   ========================= */
function showAdminPanel() {
  document.querySelector(".login-wrapper").style.display = "none";
  document.getElementById("admin-panel").classList.remove("hidden");
}

function showLogin() {
  document.querySelector(".login-wrapper").style.display = "flex";
  document.getElementById("admin-panel").classList.add("hidden");
}

/* =========================
   AUTH
   ========================= */
async function login() {
  const usernameInput = document.getElementById("username").value;
  const passwordInput = document.getElementById("password").value;

  if (!usernameInput || !passwordInput) {
    alert("Enter username and password");
    return;
  }

  const form = new FormData();
  form.append("username", usernameInput);
  form.append("password", passwordInput);

  const res = await fetch(`${API}/admin/login`, {
    method: "POST",
    body: form
  });

  if (!res.ok) {
    alert("Invalid admin credentials");
    return;
  }

  const data = await res.json();
  token = data.access_token;
  localStorage.setItem("admin_token", token);

  showAdminPanel();
  loadTools();
  loadReviews();
}

function logout() {
  localStorage.removeItem("admin_token");
  token = "";
  showLogin();
}

/* =========================
   TOOLS
   ========================= */
async function addTool() {
  if (!token) {
    alert("Please login as admin first");
    return;
  }

  const payload = {
    name: document.getElementById("name").value.trim(),
    use_case: document.getElementById("usecase").value.trim() || null,
    category: document.getElementById("categoryA").value,
    pricing_type: document.getElementById("pricingA").value
  };

  const res = await fetch(`${API}/admin/tools`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const err = await res.text();
    alert(err);
    return;
  }

  alert("Tool added successfully");
  loadTools();
}

async function loadTools() {
  const res = await fetch(`${API}/users/tools`);
  const tools = await res.json();

  const body = document.getElementById("tools-body");
  body.innerHTML = "";

  tools.forEach(t => {
    body.innerHTML += `
      <tr>
        <td>${t.name}</td>
        <td>${t.category}</td>
        <td>${t.pricing_type}</td>
        <td>⭐ ${t.average_rating.toFixed(1)}</td>
        <td>
          <button onclick="deleteTool('${t.id}')">Delete</button>
        </td>
      </tr>
    `;
  });
}

async function deleteTool(toolId) {
  await fetch(`${API}/admin/tools/${toolId}`, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  loadTools();
}

/* =========================
   REVIEWS
   ========================= */
async function loadReviews() {
  const res = await fetch(`${API}/admin/reviews?status=Pending`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  const reviews = await res.json();
  const div = document.getElementById("reviews");
  div.innerHTML = "";

  reviews.forEach(r => {
    div.innerHTML += `
      <p>
        ⭐ ${r.rating} - ${r.comment || ""}
        <button onclick="approve('${r.id}')">Approve</button>
        <button onclick="reject('${r.id}')">Reject</button>
      </p>
    `;
  });
}

async function approve(id) {
  await fetch(`${API}/admin/reviews/${id}/approve`, {
    method: "PATCH",
    headers: { "Authorization": `Bearer ${token}` }
  });
  loadReviews();
}

async function reject(id) {
  await fetch(`${API}/admin/reviews/${id}/reject`, {
    method: "PATCH",
    headers: { "Authorization": `Bearer ${token}` }
  });
  loadReviews();
}

/* =========================
   INIT ON PAGE LOAD
   ========================= */
if (token) {
  showAdminPanel();
  loadTools();
  loadReviews();
} else {
  showLogin();
}
