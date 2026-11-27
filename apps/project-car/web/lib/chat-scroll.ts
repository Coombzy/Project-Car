export const CHAT_STICK_PX = 80;

export function shouldStickToChatBottom(
  node: { scrollTop: number; scrollHeight: number; clientHeight: number },
  threshold = CHAT_STICK_PX,
): boolean {
  return node.scrollHeight - node.scrollTop - node.clientHeight <= threshold;
}
