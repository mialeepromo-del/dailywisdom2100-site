const deals = [
  {
    title: "50% Off Menu-Priced Pizzas",
    category: "Food",
    benefit: "50% OFF",
    description: "A sample food deal card. Replace this with the latest promotion details.",
    expires: "Ends Aug 2",
    posted: "Newest",
    image: "images/ChatGPT Image Jul 15, 2026, 03_29_10 PM.png",
    code: "No code",
    affiliateLink: "https://www.dominos.com/en/deals/9413"
  },
  {
    title: "Free Movie Promo Code",
    category: "Movies",
    benefit: "FREE",
    description: "Use this card for free screening codes, ticket offers, or limited movie promotions.",
    expires: "Limited supply",
    posted: "Today",
    emoji: "🎬",
    code: "TBD",
    affiliateLink: "#affiliate-link-placeholder"
  },
  {
    title: "25% Off Digital Gift Card",
    category: "Gift Cards",
    benefit: "25% OFF",
    description: "Highlight member-only gift card discounts and limited-quantity promotions here.",
    expires: "While supplies last",
    posted: "Today",
    emoji: "💳",
    code: "Member offer",
    affiliateLink: "#affiliate-link-placeholder"
  },
  {
    title: "Free Treat With App Membership",
    category: "Freebies",
    benefit: "FREEBIE",
    description: "A sample free food or rewards app promotion for your Instagram followers.",
    expires: "One day only",
    posted: "Yesterday",
    emoji: "🎁",
    code: "App required",
    affiliateLink: "#affiliate-link-placeholder"
  },
  {
    title: "Hotel Booking Bonus Offer",
    category: "Travel",
    benefit: "TRAVEL",
    description: "Use this space for hotel, airline, or travel rewards deals when available.",
    expires: "Check dates",
    posted: "Jul 28",
    emoji: "✈️",
    code: "TBD",
    affiliateLink: "#affiliate-link-placeholder"
  },
  {
    title: "LA / OC Weekend Promotion",
    category: "Local",
    benefit: "LOCAL",
    description: "Feature local restaurant offers, events, and adult programs in Los Angeles and Orange County.",
    expires: "This weekend",
    posted: "Jul 27",
    emoji: "📍",
    code: "See details",
    affiliateLink: "#affiliate-link-placeholder"
  }
];

const grid = document.getElementById("dealGrid");
const searchInput = document.getElementById("searchInput");
const categoryFilter = document.getElementById("categoryFilter");
const dealCount = document.getElementById("dealCount");
const emptyState = document.getElementById("emptyState");

function renderDeals() {
  const search = searchInput.value.toLowerCase().trim();
  const category = categoryFilter.value;
  const filtered = deals.filter(deal => {
    const matchesSearch = `${deal.title} ${deal.category} ${deal.description} ${deal.code}`.toLowerCase().includes(search);
    const matchesCategory = category === "all" || deal.category === category;
    return matchesSearch && matchesCategory;
  });

  grid.innerHTML = filtered.map((deal, index) => `
    <article class="deal-card">
     <div class="deal-image">
  <img
    src="${deal.image}"
    alt="${deal.title}"
    class="deal-photo"
    loading="lazy"
  >
  <span class="badge">${deal.benefit}</span>
</div>
      <div class="deal-body">
        <div class="deal-meta"><span>${deal.category}</span><span>${deal.posted}</span></div>
        <h3 class="deal-title">${deal.title}</h3>
        <p class="deal-description">${deal.description}</p>
        <div class="code-box">
          <code>${deal.code}</code>
          <button class="copy-btn" data-code="${deal.code}">Copy</button>
        </div>
        <div class="deal-meta"><span>${deal.expires}</span><span>Affiliate link later</span></div>
        <a
  href="${deal.affiliateLink}"
  class="deal-button"
  target="_blank"
  rel="noopener noreferrer"
>
  Get This Deal
</a>
      </div>
    </article>
  `).join("");

  dealCount.textContent = `${filtered.length} deal${filtered.length === 1 ? "" : "s"}`;
  emptyState.hidden = filtered.length !== 0;
}

searchInput.addEventListener("input", renderDeals);
categoryFilter.addEventListener("change", renderDeals);

document.querySelectorAll(".category-card").forEach(button => {
  button.addEventListener("click", () => {
    categoryFilter.value = button.dataset.category;
    renderDeals();
    document.getElementById("latest").scrollIntoView({ behavior: "smooth" });
  });
});

document.addEventListener("click", async event => {
  if (event.target.matches(".copy-btn")) {
    const code = event.target.dataset.code;
    try {
      await navigator.clipboard.writeText(code);
      const original = event.target.textContent;
      event.target.textContent = "Copied";
      setTimeout(() => event.target.textContent = original, 1200);
    } catch {
      alert(`Code: ${code}`);
    }
  }


document.getElementById("year").textContent = new Date().getFullYear();
renderDeals();
