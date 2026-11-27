function text(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

export function shownCancel(offer: {
  visible: boolean;
  label: string;
  confirmText?: string;
  note?: string;
}) {
  const confirmText = text(offer.confirmText);
  const note = text(offer.note);
  const label = confirmText || note ? offer.label.trim() || "Yes, cancel" : "Yes, cancel";
  return { visible: offer.visible, label, confirmText, note };
}
