const deals = [
  {
    title: "50% Off Menu-Priced Pizzas", 
    category: "Food",
    benefit: "50% OFF",
    description: "50% off all menu-priced pizzas.",
    expires: "Ends Aug 2, 2026",
    expiryDate: "2026-08-02",
    posted: "Newest",
    image: "images/ChatGPT Image Jul 28, 2026, 02_36_31 PM.png",
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
    expires: "Ends July 30, 2026",
    expiryDate: "2026-07-30",
    posted: "Today",
    image: "images/ChatGPT Image Jul 28, 2026, 02_26_19 PM.png",
    emoji: "🍰",
    code: "No code",
    affiliateLink: "https://www.thecheesecakefactory.com/whats-new"
  },
  {
    title: "Movie night for less!",
    category: "Gift Cards",
    benefit: "$19.20–$20.80",
    description:
      "Grab the Regal Premiere Movie Package for 2 from Giftory for $19.20–$20.80 (price varies by state).",
    expires: "While supplies last",
    expiryDate: "",
    posted: "Today",
    image: "images/ChatGPT Image Jul 25, 2026, 04_55_24 PM.png",
    emoji: "💳",
    code: "REGALMOVIE20",
    affiliateLink:
      "https://www.giftory.com/products/regal-premiere-movie-tickets-for-two-with-popcorn"
  },
  {
    title: "$5 OFF Movie ticket with Apple Pay",
    category: "Movies",
    benefit: "$5 OFF",
    description:
      "Get $5 OFF movie tickets when you pay with Apple Pay on Fandango every Wednesday through August 19, 2026.",
    expires: "Ends August 19, 2026",
    expiryDate: "2026-08-19",
    posted: "June 24, 2026",
    image: "images/ChatGPT Image Jun 24, 2026, 08_17_35 PM.png",
    emoji: "🎁",
    code: "APPLEPAYWED",
    affiliateLink:
      "https://www.fandangomovietickets.com/applepaywednesday/"
  },
  {
    title: "Hotel Booking Bonus Offer",
    category: "Travel",
    benefit: "TRAVEL",
    description:
      "Use this space for hotel, airline, or travel rewards deals when available.",
    expires: "Check dates",
    expiryDate: "",
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
    expiryDate: "",
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

function isDealExpired(deal) {
  if (!deal.expiryDate) {
    return false;
  }

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const expiryDateParts = deal.expiryDate.split("-").map(Number);

  const expiry = new Date(
    expiryDateParts[0],
    expiryDateParts[1] - 1,
    expiryDateParts[2],
    23,
    59,
    59,
    999
  );

  return today > expiry;
}

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

function hasActiveDealLink(deal) {
  return (
    deal.affiliateLink &&
    deal.affiliateLink !== "#affiliate-link-placeholder"
  );
}

function getDealButton(deal) {
  const expired = isDealExpired(deal);

  if (expired) {
    return `
      <button
        type="button"
        class="deal-button placeholder expired-button"
        disabled
      >
        Expired
      </button>
    `;
  }

  if (hasActiveDealLink(deal)) {
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

function getDealStatusText(deal) {
  if (isDealExpired(deal)) {
    return "Offer ended";
  }

  if (!hasActiveDealLink(deal)) {
    return "Link coming soon";
  }

  return "View deal";
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
    .map(deal => {
      const expired = isDealExpired(deal);

      return `
        <article class="deal-card ${expired ? "expired" : ""}">
          <div class="deal-image">
            ${getDealImage(deal)}

            <span class="badge">
              ${deal.benefit}
            </span>

            ${
              expired
                ? `
                  <div
                    class="expired-stamp"
                    aria-label="This offer has expired"
                  >
                    EXPIRED
                  </div>
                `
                : ""
            }
          </div>

          <div class="deal-body">
            <div class="deal-meta">
              <span>${deal.category}</span>
              <span>${deal.posted}</span>
            </div>

            <h3 class="deal-title">
              ${deal.title}
            </h3>

            <p class="deal-description">
              ${deal.description}
            </p>

            <div class="code-box">
              <code>${deal.code}</code>

              <button
                type="button"
                class="copy-btn"
                data-code="${deal.code}"
                ${expired ? "disabled" : ""}
              >
                ${expired ? "Expired" : "Copy"}
              </button>
            </div>

            <div class="deal-meta">
              <span>
                ${expired ? "Expired" : deal.expires}
              </span>

              <span>
                ${getDealStatusText(deal)}
              </span>
            </div>

            ${getDealButton(deal)}
          </div>
        </article>
      `;
    })
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

  if (event.target.disabled) {
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

/* Expired deals */

.deal-card.expired {
  opacity: 0.8;
}

.deal-card.expired .deal-image {
  filter: grayscale(100%);
}

.deal-card.expired .deal-photo {
  filter: grayscale(100%);
}

.deal-card.expired .badge {
  background: rgba(245, 245, 245, 0.92);
  color: #777;
}

.deal-card.expired .deal-title,
.deal-card.expired .deal-description,
.deal-card.expired .deal-meta,
.deal-card.expired code {
  color: #7b776e;
}

.deal-card.expired .code-box {
  background: #ece9e2;
}

.deal-card.expired .copy-btn {
  color: #8e8a80;
  cursor: not-allowed;
}

.deal-card.expired .deal-button {
  background: #9b998f;
  cursor: not-allowed;
  pointer-events: none;
}

.expired-stamp {
  position: absolute;
  top: 50%;
  left: 50%;
  z-index: 5;

  transform: translate(-50%, -50%) rotate(-18deg);

  padding: 10px 26px;
  border: 4px solid rgba(90, 90, 90, 0.9);
  border-radius: 10px;

  background: rgba(255, 255, 255, 0.55);
  color: rgba(90, 90, 90, 0.95);

  font-size: clamp(1.2rem, 4vw, 2rem);
  font-weight: 800;
  line-height: 1;
  letter-spacing: 0.16em;
  text-align: center;
  white-space: nowrap;

  pointer-events: none;
}

.expired-button {
  background: #8f8d86;
}
