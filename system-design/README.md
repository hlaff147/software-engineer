# 🏛️ System Design Architecture Diagrams

> High-level visual architecture references and diagrams for large-scale distributed systems, financial transaction processing, loan engines, and consensus guarantees.

---

## 📊 Catalog of Architecture Diagrams

| Diagram | Architectural Concept & Scope |
|---------|-------------------------------|
| [`CAP.png`](./CAP.png) | **CAP Theorem Guarantees & Trade-offs**: Consistency vs. Availability in the presence of Network Partitions (CP vs. AP systems). |
| [`payment_system_picpay_payment_example.png`](./payment_system_picpay_payment_example.png) | **Payment Processing Architecture**: High-throughput payment gateway, idempotency layers, ledger persistence, and notification dispatch. |
| [`Saga1-2025-12-27-235823.png`](./Saga1-2025-12-27-235823.png) | **Saga Pattern (Choreography)**: Distributed transaction management via asynchronous domain events and compensating transactions. |
| [`Saga2-2025-12-27-235823.png`](./Saga2-2025-12-27-235823.png) | **Saga Pattern (Orchestration)**: Centralized state-machine orchestrator coordinating multi-step transactions and rollback procedures. |
| [`emprestimo_pf_system_design.png`](./emprestimo_pf_system_design.png) | **Personal Loan System Design**: Customer credit underwriting pipeline, risk scoring engine, and automated offer disbursement. |
| [`emprestimo_imovel_system_des.png`](./emprestimo_imovel_system_des.png) | **Real Estate Mortgage System Design**: Multi-stage state machine for collateral appraisal, compliance verification, and contract generation. |
| [`2025-12-27-213435.png`](./2025-12-27-213435.png) | **Ride Matching & Geolocation System**: Spatial indexing (Uber H3 / QuadTree) and real-time state synchronization. |
| [`2025-12-27-233225.png`](./2025-12-27-233225.png) | **Canary Deployment & Routing Pipeline**: Progressive traffic shifting, observability baselining, and automated rollback triggers. |
| [`2025-12-28-053618.png`](./2025-12-28-053618.png) | **High-Concurrency Ticket Booking**: Flash-sale seat reservation, distributed locking with Redis Redlock, and queue throttling. |
| [`Untitled diagram-2025-12-27-061426.png`](./Untitled%20diagram-2025-12-27-061426.png) | **Distributed Ledger & Double-Entry Accounting**: Immutable balance journal and audit log isolation. |

---

## 🔗 Related Resources

- [Study Interview & System Design Notes](../study_interview_system_design)
- [Mastercard SDE-2 Interview Prep](../study_interview_system_design/MASTERCARD_SDE2_INTERVIEW_PREP.md)
