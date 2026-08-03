const deals = [
  {
    title: "FREE Chicken Shack", 
    category: "Food",
    benefit: "FREE",
    description: "Get a FREE Chicken Shack with a $10 minimum purchase every Sunday.",
    expires: "Ends December 27, 2026",
    expiryDate: "2026-12-27",
    posted: "Aug 2, 2026",
    image: "images/ChatGPT Image Aug 2, 2026, 07_31_34 PM.png",
    emoji: "🐔",
    code: "CHICKENSUNDAY",
    affiliateLink: "https://shakeshack.com/national-regional-offers#/"
  },
  {
    title: "FREE 2 Tickets for Elijah Peel", 
    category: "Movies",
    benefit: "FREE",
    description: "Watch Elijah Peel with up to 2 complimentary movie tickets through Fandango while supplies last.",
    expires: "Ends Aug 31, 2026 or While Supplies Last",
    expiryDate: "2026-08-31",
    posted: "Aug 2, 2026",
    image: "images/Aug 2, 2026, 11_37_41 AM.png",
    emoji: "🎬",
    code: "ELIJAHFREE",
    affiliateLink: "https://www.fandango.com/elijah-peel-2026-246405/movie-overview"
  },
  {
    title: "FREE Chips & Guac", 
    category: "Food",
    benefit: "FREE",
    description: "Get FREE Chips & Guac with the purchase of any entrée when you order through the Chipotle website or mobile app.",
    expires: "Ends Aug 1, 2026",
    expiryDate: "2026-08-01",
    posted: "Jul 30, 2026",
    image: "images/ChatGPT Image Jul 30, 2026, 08_18_50 AM.png",
    emoji: "🥑",
    code: "AVO2026",
    affiliateLink: "https://www.chipotle.com/#menu"
  },
  {
    title: "50% Off Menu-Priced Pizzas", 
    category: "Food",
    benefit: "50% OFF",
    description: "50% off all menu-priced pizzas.",
    expires: "Ends Aug 2, 2026",
    expiryDate: "2026-08-02",
    posted: "Jul 28, 2026",
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
    posted: "Jul 28, 2026",
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
    posted: "Jul 25, 2026",
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
    title: "Free Handcrafted Drink Every Monday",
    category: "Food",
    benefit: "Free",
    description:
      "Get a FREE handcrafted beverage at Capital One Café every Monday!",
    expires: "Ends September 7, 2026",
    expiryDate: "2026-09-07",
    posted: "May 13, 2026",
    image: "images/GEjMF.jpg",
    emoji: "☕",
    code: "QR Code",
    affiliateLink: "https://coffree.capitalone.com/sms/?mc=BP&cid=fzqpufjqcf"
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
