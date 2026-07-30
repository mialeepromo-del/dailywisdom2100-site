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
