# Memory Bank Template

To initialize a Memory Bank, copy this template to a `memory-bank` directory in the root of your project and split the sections into their respective files.

## File 1: `projectbrief.md`
**Core Mission**: To build a reliable and scalable e-commerce platform.
**Scope**: User authentication, product catalog, shopping cart, checkout.
**Success Criteria**: Sub-second page loads, 99.9% uptime, seamless payment integration.

## File 2: `systemPatterns.md`
**Architecture**: Microservices (Auth, Catalog, Order)
**Design Patterns**: Repository pattern for DB access, CQRS for orders.
**Component Relationships**: React frontend talks to API Gateway -> Routes to microservices.

## File 3: `techContext.md`
**Tech Stack**: React, Node.js, PostgreSQL, Redis.
**Dependencies**: Express, TypeORM, React Router.
**Build Commands**: `npm run build`, `docker-compose up`

## File 4: `activeContext.md`
**Current Focus**: Implementing Stripe payment gateway.
**Recent Changes**: Added Order database schema.
**Active Decisions**: Using webhooks for asynchronous payment confirmation.
## [2023-10-25] Payment Integration Session
Implemented Stripe checkout flow, next is handling webhooks.

## File 5: `progress.md`
**What Works**: Auth service, Product Catalog.
**What's Left**: Payment gateway, Order history.
**Known Blockers**: Awaiting Stripe API key from DevOps.
