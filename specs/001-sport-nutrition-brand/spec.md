# Feature Specification: Sport Nutrition Brand — Bogotá

**Feature Branch**: `001-sport-nutrition-brand`

**Created**: 2026-09-01

**Status**: Draft

**Input**: User description: "Based on the sport nutrition benchmark, lets brainstorm in creating a sport nutrition brand in Bogota/Colombia"

## Clarifications

### Session 2026-09-01

- Q: Given a very small personal network (3–10 people) and no sales/marketing background, how should the brand acquire its first customers? → A: Wholesale/partner-first as the primary channel — target ~3–5 local bike shops, gyms, or cycling clubs as resellers whose existing customers become the actual buyers. Ambassador/creator product seeding (2–3 local athletes/creators given free product) is a low-cost secondary amplifier that also gives partner conversations social proof to point to. Paid digital advertising is explicitly deferred until the wholesale channel produces at least one repeatable sale — not required for launch.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - First Wholesale Partner Signs On (Priority: P1)

A Bogotá bike shop, gym, or cycling club agrees to stock and resell the brand's products, becoming the actual point of sale to its own existing members and customers.

**Why this priority**: This is now the critical first step in the go-to-market strategy: with only a 3–10 person personal network and no sales background, reaching end customers directly isn't realistic. A handful of partner relationships — not hundreds of individual consumer sales — is the highest-leverage, most achievable first milestone, and nothing else in the funnel matters until at least one partner is stocking product.

**Independent Test**: Can be fully tested by signing one wholesale partner on agreed terms and confirming they place and receive a stocking order.

**Acceptance Scenarios**:

1. **Given** a shop, gym, or club has been approached with the product and terms, **When** they agree to stock it, **Then** they place a first stocking order and receive the agreed quantity at the agreed wholesale price within the agreed lead time.
2. **Given** a wholesale partner's stock is running low, **When** they reorder, **Then** the reorder process is at least as fast as their first order.

---

### User Story 2 - End Customer Buys Through a Partner or Ambassador (Priority: P2)

An athlete training with a partner gym/club, shopping at a partner bike shop, or following a seeded local ambassador discovers the brand and buys a starter hydration or energy product.

**Why this priority**: This is where revenue actually materializes, but it depends on User Story 1 (a partner must exist to sell through, or an ambassador's post must point somewhere to buy) and is therefore secondary to establishing the channel itself.

**Independent Test**: Can be fully tested by confirming at least one end customer completes a paid purchase either in-store at a wholesale partner or online after seeing an ambassador's post, without Daniel personally making the sale.

**Acceptance Scenarios**:

1. **Given** a customer encounters the product at a partner location or through an ambassador's content, **When** they decide to buy, **Then** they can complete the purchase (in-store at the partner, or online) and receive the product within the promised delivery window.
2. **Given** a customer has a stated dietary restriction (e.g., vegan, lactose-free), **When** they check product ingredients before buying, **Then** they can clearly determine whether the product fits their restriction without contacting support.

---

### User Story 3 - Repeat Purchase via Subscription (Priority: P3)

An athlete who liked their first order sets up a recurring monthly delivery directly with the brand so they never run out before a race or big training block.

**Why this priority**: Recurring revenue is what turns one-off sales into predictable monthly income and is central to Daniel's $2,000–$3,000/month recurring-revenue goal. It only matters once a purchase funnel (P1 + P2) is already producing customers.

**Independent Test**: Can be fully tested by offering a subscription option at checkout and confirming a customer successfully enrolls and receives a second automatic order without manually re-ordering.

**Acceptance Scenarios**:

1. **Given** a customer has completed at least one purchase, **When** they opt into a recurring delivery plan, **Then** their next order is generated and fulfilled automatically on the chosen cadence without further action from them.
2. **Given** a subscribed customer wants to change or cancel their plan, **When** they request the change, **Then** the change takes effect before the next scheduled order is generated.

---

### Edge Cases

- What happens when a wholesale partner agrees to stock the product but doesn't actively promote or sell it (passive shelf presence with no real sales)?
- What happens when a customer has an allergy or a competition-restricted-substance concern and the product's ingredient list doesn't clearly address it?
- How does the brand handle a delivery request outside the Bogotá metro area?
- What happens when a co-packer's minimum order quantity exceeds what current demand justifies?
- How does the brand respond if an incumbent competitor matches or undercuts its pricing?
- What happens when a product's sanitary/regulatory registration is delayed and a launch date has already been promised to customers or partners?
- How does a subscription order get handled if a product is temporarily out of stock?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The brand MUST launch with a focused initial product line of 2–3 SKUs centered on endurance/hydration nutrition (e.g., electrolyte mix, energy gel or chew) rather than a broad general-supplement catalog.
- **FR-002**: The brand MUST source products through a private-label or co-packing manufacturer rather than developing formulations in-house.
- **FR-003**: Every SKU MUST carry the required Colombian sanitary/regulatory registration (INVIMA) before it is offered for sale.
- **FR-004**: The brand MUST provide a way for customers to browse products, see ingredients/pricing in Colombian pesos, and complete a purchase using a locally accepted payment method.
- **FR-005**: The brand MUST fulfill Bogotá-metro orders within a stated, published delivery window.
- **FR-006**: The brand MUST reach and acquire its first end customers primarily by placing products with wholesale partners (bike shops, gyms, cycling clubs) who sell to their own existing customers, rather than through Daniel directly marketing to individual consumers or through paid digital advertising.
- **FR-007**: The brand MUST offer customers a recurring/subscription purchase option in addition to one-off purchases.
- **FR-008**: The brand MUST offer wholesale terms that let local bike shops, gyms, or clubs stock and resell products.
- **FR-009**: The brand MUST track cost of goods, acquisition cost, and margin per SKU so unsustainable products or channels can be identified before the product line is expanded.
- **FR-010**: Every product's ingredient list MUST be presented clearly enough for an athlete to self-assess dietary fit (vegan/lactose-free/etc.) and competition-eligibility (banned-substance) concerns without contacting support.
- **FR-011**: The brand MUST seed free product to a small number (2–3) of local athlete/creator ambassadors as a low-cost way to generate visible social proof and content, supporting wholesale partner conversations and organic discovery.
- **FR-012**: Paid digital advertising MUST NOT be required for initial launch and MUST be deferred until the wholesale/partner channel has produced at least one validated, repeatable sale.

### Key Entities

- **Product SKU**: A single sellable item (e.g., electrolyte mix, energy gel), with its ingredients, price, regulatory registration status, and cost of goods.
- **Customer**: An individual athlete, with contact details, purchase history, subscription status, any stated dietary preference or restriction, and the channel (wholesale partner, ambassador referral, direct) that acquired them.
- **Subscription**: A recurring order tied to a customer, defined by product mix and delivery frequency.
- **Wholesale Partner**: A bike shop, gym, or club that stocks and resells products, with its own pricing terms and order history.
- **Ambassador**: A local athlete or content creator seeded with free product in exchange for visibility/content, tracked separately from paying customers.
- **Order**: A single transaction (direct or wholesale), including channel, items, and fulfillment status.
- **Supplier / Co-packer**: The manufacturing partner producing the SKUs, with its minimum order quantity, lead time, and unit cost.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The brand signs its first wholesale partner (bike shop, gym, or cycling club) within 45 days of launch.
- **SC-002**: The brand completes its first end-customer paying transaction (through a partner or ambassador referral) within 60 days of launch.
- **SC-003**: The brand reaches $2,000–$3,000/month in recurring revenue within 6 months of launch.
- **SC-004**: At least 30% of first-time customers make a second purchase or start a subscription within 90 days of their first order.
- **SC-005**: Gross margin per SKU stays above 55% after cost of goods, wholesale partner margin, and delivery costs.
- **SC-006**: At least 3 local wholesale partners are actively stocking and reselling the brand's products within 6 months of launch.
- **SC-007**: Average cash cost to acquire a new paying customer stays under $30, achieved through wholesale partner placement and free-product ambassador seeding rather than paid advertising.

## Assumptions

- **Niche**: The brand targets endurance athletes (cyclists, hikers, runners) rather than the general gym/bodybuilding protein-powder segment, both because it matches Daniel's personal experience and credibility as a practicing cyclist/hiker — even though his own personal network is small (3–10 people) — and because that broader protein-powder segment is already dominated by a small number of large incumbents in Colombia.
- **Manufacturing model**: Products are produced by a private-label/co-packing manufacturer rather than developed in-house, consistent with Daniel not having a food-science/formulation background and wanting to keep upfront capital low.
- **Capital**: Launch is funded from the $5,000–$10,000 already earmarked for a side business, deployed in stages rather than all at once.
- **Time**: The business is built within the 10–15 hours/week Daniel has available alongside his full-time job, so early operations (fulfillment, customer support) must stay lightweight.
- **Acquisition channel**: Primary customer acquisition is wholesale/partner-first — targeting ~3–5 local bike shops, gyms, or cycling clubs as resellers — because Daniel's personal network is small (3–10 people) and he has no sales or marketing background, so a handful of partner relationships is more achievable than direct consumer selling. A small number of local athlete/creator ambassadors receive free product as a low-cost secondary tactic to generate visible social proof. Paid digital advertising is explicitly deferred until the wholesale channel proves at least one repeatable sale — Colombian DTC supplement paid-acquisition costs (commonly $80–$130 per customer) would consume the available budget too quickly for an unvalidated, bootstrapped launch.
- **Market size and structure**: Colombia's sports nutrition category is a small, low-growth market (roughly $45M, low single-digit annual growth) with the top few companies holding the large majority of share, so success depends on owning a specific underserved niche (endurance/hydration) reached through partners rather than competing broadly for direct consumer attention.
- **Regulatory compliance**: Sanitary/regulatory registration (INVIMA) for each product is a hard prerequisite for sale, not an optional or later step.
- **Geographic scope**: v1 distribution is limited to the Bogotá metro area; expansion to other Colombian cities is out of scope for this spec.
- **Currency and pricing**: Customers pay in Colombian pesos (COP); Daniel's income and cost baseline are tracked in USD for his own financial goals.
