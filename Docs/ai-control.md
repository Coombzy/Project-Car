# AI control

Ben locked this on 2026-10-04. As much of the shop app as possible is controllable by an AI, not only by a human at the screen.

An AI is a client of the same API. The actor is recorded. It can create a request, approve a shop-hoist request, read bookings, and read a parts or crib row. It cannot open the shop, take a payment, or approve a request it created.

A member action that already needs approval still needs approval. The AI is one of the approvers. It is not a bypass.

Git only. Do not deploy Doc. Do not add Stripe.
