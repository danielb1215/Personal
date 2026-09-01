# Feature Specification: Sport Nutrition Brand — Bogotá

**Feature Branch**: `001-sport-nutrition-brand`

**Created**: 2026-09-01

**Status**: Draft

**Input**: User description: "Based on the sport nutrition benchmark, lets brainstorm in creating a sport nutrition brand in Bogota/Colombia"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - First Purchase by an Endurance Athlete (Priority: P1)

A cyclist, hiker, or runner in Bogotá who trains regularly hears about the brand (through a group ride, a local event, or word of mouth) and buys a starter hydration or energy product to try before their next long training session.

**Why this priority**: Without a first paying customer there is no business. This journey validates that the product, pricing, and buying experience actually convert a real athlete into a paying customer — the minimum viable proof of concept.

**Independent Test**: Can be fully tested by launching a single SKU for sale (online storefront or in-person at a ride/event) to Daniel's existing cycling/hiking network and confirming at least one completed, paid transaction.

**Acceptance Scenarios**:

1. **Given** a new customer has never bought from the brand, **When** they view the product and complete checkout (online or in person), **Then** they receive a confirmed order and the product within the promised delivery window.
2. **Given** a customer has a stated dietary restriction (e.g., vegan, lactose-free), **When** they check product ingredients before buying, **Then** they can clearly determine whether the product fits their restriction without contacting support.

---

### User Story 2 - Repeat Purchase via Subscription (Priority: P2)

An athlete who liked their first order sets up a recurring monthly delivery of their preferred nutrition products so they never run out before a race or big training block.

**Why this priority**: Recurring revenue is what turns one-off sales into predictable monthly income and is central to Daniel's $2,000–$3,000/month recurring-revenue goal. It only matters once first purchases (P1) are already happening.

**Independent Test**: Can be fully tested by offering a subscription option at checkout and confirming a customer successfully enrolls and receives a second automatic order without manually re-ordering.

**Acceptance Scenarios**:

1. **Given** a customer has completed at least one purchase, **When** they opt into a recurring delivery plan, **Then** their next order is generated and fulfilled automatically on the chosen cadence without further action from them.
2. **Given** a subscribed customer wants to change or cancel their plan, **When** they request the change, **Then** the change takes effect before the next scheduled order is generated.

---

### User Story 3 - Local Shop or Club Becomes a Wholesale Partner (Priority: P3)

A Bogotá bike shop, gym, or cycling club agrees to stock and resell the brand's products to its own members and customers, extending reach beyond Daniel's direct network.

**Why this priority**: Wholesale partners multiply distribution without Daniel having to acquire every end customer directly, but this channel only makes sense once the product and direct-sale demand (P1/P2) are already proven.

**Independent Test**: Can be fully tested by signing one wholesale partner on agreed terms and confirming they place and receive a stocking order that they then resell.

**Acceptance Scenarios**:

1. **Given** a shop or club has agreed to wholesale terms, **When** they place a stocking order, **Then** they receive the agreed quantity at the agreed wholesale price within the agreed lead time.
2. **Given** a wholesale partner's stock is running low, **When** they reorder, **Then** the reorder process is at least as fast as their first order.

---

### Edge Cases

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
- **FR-006**: The brand MUST reach and acquire its first customers primarily through direct community channels (group rides, cycling clubs, gyms, hiking groups, events, word of mouth) rather than paid digital advertising.
- **FR-007**: The brand MUST offer customers a recurring/subscription purchase option in addition to one-off purchases.
- **FR-008**: The brand MUST offer wholesale terms that let local bike shops, gyms, or clubs stock and resell products.
- **FR-009**: The brand MUST track cost of goods, acquisition cost, and margin per SKU so unsustainable products or channels can be identified before the product line is expanded.
- **FR-010**: Every product's ingredient list MUST be presented clearly enough for an athlete to self-assess dietary fit (vegan/lactose-free/etc.) and competition-eligibility (banned-substance) concerns without contacting support.

### Key Entities

- **Product SKU**: A single sellable item (e.g., electrolyte mix, energy gel), with its ingredients, price, regulatory registration status, and cost of goods.
- **Customer**: An individual athlete, with contact details, purchase history, subscription status, and any stated dietary preference or restriction.
- **Subscription**: A recurring order tied to a customer, defined by product mix and delivery frequency.
- **Wholesale Partner**: A bike shop, gym, or club that stocks and resells products, with its own pricing terms and order history.
- **Order**: A single transaction (direct or wholesale), including channel, items, and fulfillment status.
- **Supplier / Co-packer**: The manufacturing partner producing the SKUs, with its minimum order quantity, lead time, and unit cost.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The brand completes its first paying customer transaction within 60 days of launch.
- **SC-002**: The brand reaches $2,000–$3,000/month in recurring revenue within 6 months of launch.
- **SC-003**: At least 30% of first-time customers make a second purchase or start a subscription within 90 days of their first order.
- **SC-004**: Gross margin per SKU stays above 55% after cost of goods and delivery costs.
- **SC-005**: At least 3 local wholesale partners are actively stocking and reselling the brand's products within 6 months of launch.
- **SC-006**: Average cost to acquire a new paying customer stays under $30, achieved primarily through community-based rather than paid-advertising channels.

## Assumptions

- **Niche**: The brand targets endurance athletes (cyclists, hikers, runners) rather than the general gym/bodybuilding protein-powder segment, both because this matches Daniel's own community and because that broader segment is already dominated by a small number of large incumbents in Colombia.
- **Manufacturing model**: Products are produced by a private-label/co-packing manufacturer rather than developed in-house, consistent with Daniel not having a food-science/formulation background and wanting to keep upfront capital low.
- **Capital**: Launch is funded from the $5,000–$10,000 already earmarked for a side business, deployed in stages rather than all at once.
- **Time**: The business is built within the 10–15 hours/week Daniel has available alongside his full-time job, so early operations (fulfillment, customer support) must stay lightweight.
- **Acquisition channel**: Primary customer acquisition is community-based (group rides, cycling clubs, gyms, hiking groups, events, word of mouth), not paid digital advertising — Colombian DTC supplement paid-acquisition costs (commonly $80–$130 per customer) would consume the available budget too quickly for a bootstrapped launch.
- **Market size and structure**: Colombia's sports nutrition category is a small, low-growth market (roughly $45M, low single-digit annual growth) with the top few companies holding the large majority of share, so success depends on owning a specific underserved niche (endurance/hydration) rather than competing broadly.
- **Regulatory compliance**: Sanitary/regulatory registration (INVIMA) for each product is a hard prerequisite for sale, not an optional or later step.
- **Geographic scope**: v1 distribution is limited to the Bogotá metro area; expansion to other Colombian cities is out of scope for this spec.
- **Currency and pricing**: Customers pay in Colombian pesos (COP); Daniel's income and cost baseline are tracked in USD for his own financial goals.
