export function shouldSkipChatPoll(state: { inFlight: boolean; hidden: boolean }): boolean {
  return state.inFlight || state.hidden;
}
