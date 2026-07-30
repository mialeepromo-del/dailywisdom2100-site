const deals = [
  {
    title: "50% Off Menu-Priced Pizzas",
    category: "Food",
    benefit: "50% OFF",
    description: "50% off all menu-priced pizzas.",
    expires: "Ends Aug 2",
    posted: "Newest",
    image: "images/ChatGPT Image Jul 28, 2026, 02_36_31 PM",
    emoji: "🍕",
    code: "No code",
    affiliateLink: "https://www.dominos.com/en/deals/9413"
  },
  {
    title: "Half Price Cheesecake",
    category: "Food",
    benefit: "50% OFF",
    description:
      "Celebrate on July 30 with ANY slice of cheesecake for 50% OFF when you dine in at The Cheesecake Factory.",
    expires: "Ends July 30",
    posted: "",
    image: "ChatGPT Image Jul 28, 2026, 02_26_19 PM",
    code: "No code",
    affiliateLink: "https://www.thecheesecakefactory.com/whats-new"
  },
  {
    title: "25% Off Digital Gift Card",
    category: "Gift Cards",
    benefit: "25% OFF",
    description:
      "Highlight member-only gift card discounts and limited-quantity promotions here.",
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
    description:
      "A sample free food or rewards app promotion for your Instagram followers.",
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
    description:
      "Use this space for hotel, airline, or travel rewards deals when available.",
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
    description:
      "Feature local restaurant offers, events, and adult programs in Los Angeles and Orange County.",
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
const yearElement = document.getElementById("year");

function getDealImage(deal) {
  if (deal.image) {
    return `
      <img
        src="${deal.image}"
        alt="${deal.title}"
        class="deal-photo"
        loading="lazy"
      >
    `;
  }

  return `
    <span class="deal-emoji" aria-hidden="true">
      ${deal.emoji || "✨"}
    </span>
  `;
}

function getDealButton(deal) {
  const hasActiveLink =
    deal.affiliateLink &&
    deal.affiliateLink !== "#affiliate-link-placeholder";

  if (hasActiveLink) {
    return `
      <a
        href="${deal.affiliateLink}"
        class="deal-button"
        target="_blank"
        rel="noopener noreferrer"
      >
        Get This Deal
      </a>
    `;
  }

  return `
    <button
      type="button"
      class="deal-button placeholder"
      disabled
    >
      Link Coming Soon
    </button>
  `;
}

function renderDeals() {
  const search = searchInput.value.toLowerCase().trim();
  const category = categoryFilter.value;

  const filtered = deals.filter(deal => {
    const searchableText = `
      ${deal.title}
      ${deal.category}
      ${deal.description}
      ${deal.code}
    `.toLowerCase();

    const matchesSearch = searchableText.includes(search);
    const matchesCategory =
      category === "all" || deal.category === category;

    return matchesSearch && matchesCategory;
  });

  grid.innerHTML = filtered
    .map(
      deal => `
        <article class="deal-card">
          <div class="deal-image">
            ${getDealImage(deal)}
            <span class="badge">${deal.benefit}</span>
          </div>

          <div class="deal-body">
            <div class="deal-meta">
              <span>${deal.category}</span>
              <span>${deal.posted}</span>
            </div>

            <h3 class="deal-title">${deal.title}</h3>

            <p class="deal-description">
              ${deal.description}
            </p>

            <div class="code-box">
              <code>${deal.code}</code>

              <button
                type="button"
                class="copy-btn"
                data-code="${deal.code}"
              >
                Copy
              </button>
            </div>

            <div class="deal-meta">
              <span>${deal.expires}</span>
              <span>
                ${
                  deal.affiliateLink === "#affiliate-link-placeholder"
                    ? "Link coming soon"
                    : "View deal"
                }
              </span>
            </div>

            ${getDealButton(deal)}
          </div>
        </article>
      `
    )
    .join("");

  dealCount.textContent =
    `${filtered.length} deal${filtered.length === 1 ? "" : "s"}`;

  emptyState.hidden = filtered.length !== 0;
}

searchInput.addEventListener("input", renderDeals);
categoryFilter.addEventListener("change", renderDeals);

document.querySelectorAll(".category-card").forEach(button => {
  button.addEventListener("click", () => {
    categoryFilter.value = button.dataset.category;
    renderDeals();

    document
      .getElementById("latest")
      .scrollIntoView({ behavior: "smooth" });
  });
});

document.addEventListener("click", async event => {
  if (!event.target.matches(".copy-btn")) {
    return;
  }

  const code = event.target.dataset.code;

  try {
    await navigator.clipboard.writeText(code);

    const originalText = event.target.textContent;
    event.target.textContent = "Copied";

    setTimeout(() => {
      event.target.textContent = originalText;
    }, 1200);
  } catch {
    alert(`Code: ${code}`);
  }
});

if (yearElement) {
  yearElement.textContent = new Date().getFullYear();
}

renderDeals();
