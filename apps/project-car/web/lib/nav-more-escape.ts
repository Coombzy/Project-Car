type NavMoreKeyEvent = {
  key: string;
  preventDefault: () => void;
};

export function handleNavMoreKeydown(event: NavMoreKeyEvent, details: HTMLDetailsElement | null): void {
  if (event.key !== "Escape" || details === null || !details.open) {
    return;
  }
  event.preventDefault();
  details.open = false;
  details.querySelector("summary")?.focus({ preventScroll: true });
}
