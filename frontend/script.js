const API = "http://127.0.0.1:9000";
let ratings = {};

/* =========================
   FETCH APPROVED REVIEWS
   ========================= */
async function fetchApprovedReviews() {
  const res = await fetch(`${API}/users/reviews`);
  return await res.json();
}

/* =========================
   LOAD TOOLS + REVIEWS
   ========================= */
async function loadTools() {
  const category = document.getElementById("category").value;
  const pricing = document.getElementById("pricing").value;
  const search = document.getElementById("search").value.toLowerCase();
  const sort = document.getElementById("sort").value;

  let toolsUrl = `${API}/users/tools`;
  const params = [];

  if (category) params.push(`category=${encodeURIComponent(category)}`);
  if (pricing) params.push(`pricing_type=${encodeURIComponent(pricing)}`);

  if (params.length > 0) {
    toolsUrl += `?${params.join("&")}`;
  }

  const [toolsRes, reviews] = await Promise.all([
    fetch(toolsUrl),
    fetchApprovedReviews(),
  ]);

  let tools = await toolsRes.json();

  if (search) {
    tools = tools.filter((t) => t.name.toLowerCase().includes(search));
  }

  if (sort === "high") {
    tools.sort((a, b) => b.average_rating - a.average_rating);
  }
  if (sort === "low") {
    tools.sort((a, b) => a.average_rating - b.average_rating);
  }

  const reviewsByTool = {};
  reviews.forEach((r) => {
    if (!reviewsByTool[r.tool_id]) {
      reviewsByTool[r.tool_id] = [];
    }
    reviewsByTool[r.tool_id].push(r);
  });

  const container = document.getElementById("tools");
  container.innerHTML = "";

  tools.forEach((tool) => {
    const toolReviews = reviewsByTool[tool.id] || [];

    container.innerHTML += `
      <div class="tool">

        <div class="tool-header">
          <div>
            <h3>${tool.name}</h3>
            <p>${tool.use_case || ""}</p>
          </div>

          <div class="tool-badges">
            <span class="badge category">${tool.category}</span>
            <span class="badge pricing">${tool.pricing_type}</span>
            <span class="badge rating-badge">
              <i class="fa fa-star"></i>
              ${tool.average_rating.toFixed(1)}
            </span>
          </div>
        </div>

        <div class="reviews">
          <h4>Reviews (${toolReviews.length})</h4>
          ${
            toolReviews.length === 0
              ? `<p class="no-review">No reviews yet</p>`
              : toolReviews
                  .map(
                    (r) => `
                  <p class="review">
                    ⭐ ${r.rating} – ${r.comment || "No comment"}
                  </p>
                `
                  )
                  .join("")
          }
        </div>

        <div class="review-box">
          <div>${renderStars(tool.id)}</div>
          <input type="text" placeholder="Comment" id="c-${tool.id}">
          <button onclick="submitReview('${tool.id}')">Submit Review</button>
        </div>

      </div>
    `;
  });
}

/* =========================
   STAR RATING (HIGHLIGHT)
   ========================= */
function renderStars(toolId) {
  let stars = "";
  for (let i = 1; i <= 5; i++) {
    stars += `
      <span
        class="star"
        data-tool="${toolId}"
        data-value="${i}"
        onclick="setRating('${toolId}', ${i})"
        onmouseover="hoverStars('${toolId}', ${i})"
        onmouseout="resetStars('${toolId}')"
      >★</span>
    `;
  }
  return stars;
}

function hoverStars(toolId, value) {
  const stars = document.querySelectorAll(`.star[data-tool="${toolId}"]`);
  stars.forEach((star) => {
    star.classList.toggle("active", Number(star.dataset.value) <= value);
  });
}

function resetStars(toolId) {
  const current = ratings[toolId] || 0;
  hoverStars(toolId, current);
}

function setRating(toolId, value) {
  ratings[toolId] = value;
  hoverStars(toolId, value);
}

/* =========================
   SUBMIT REVIEW
   ========================= */
async function submitReview(toolId) {
  const rating = ratings[toolId];
  if (!rating) {
    alert("Please select rating");
    return;
  }

  const comment = document.getElementById(`c-${toolId}`).value;

  await fetch(`${API}/users/review`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      tool_id: toolId,
      rating: rating,
      comment: comment,
    }),
  });

  alert("Review submitted (Pending Approval)");
}

/* Initial load */
loadTools();
