# AI control

Ben locked this on 2026-10-04. As much of the shop app as possible is controllable by an AI, not only by a human at the screen.

An AI is a client of the same API. The actor is recorded. It can create a request, approve a shop-hoist request, read bookings, and read a parts or crib row. It cannot open the shop, take a payment, or approve a request it created.

A member action that already needs approval still needs approval. The AI is one of the approvers. It is not a bypass.

Human and AI call the same approve and deny routes. The stored action names the actor, human or AI, and the request id. A draft is not sent until one of them accepts it. An AI cannot approve a request it created, debit tokens before approval, or refund without a human accept.

Proof: `apps/project-car/api/tests/test_staff_actions.py`.

Git only. Do not deploy Doc. Do not add Stripe.
