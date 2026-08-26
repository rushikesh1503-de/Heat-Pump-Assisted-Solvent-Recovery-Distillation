# Heat-Pump-Assisted Solvent Recovery Distillation
## Project Overview: Goal, Motivation, and Scope

---

## 1. Goal

Design, simulate, and economically evaluate the retrofit of an ethanol–water solvent recovery distillation column from conventional steam heating to a **high-temperature industrial heat pump**, using the column's own condenser waste heat as the heat source for the reboiler.

Specifically, the project sets out to:

1. Build and converge a realistic baseline distillation column model.
2. Quantify the condenser (waste heat source) and reboiler (heat sink) duties and temperatures.
3. Establish, through pinch analysis, why direct heat recovery is thermodynamically impossible and a heat pump is required.
4. Design a mechanical vapor-compression heat pump cycle to bridge that gap.
5. Quantify how much of the reboiler demand the heat pump can realistically cover.
6. Build a techno-economic case: energy cost savings, CO2 emissions avoided, and (in progress) capital payback.

---

## 2. Why This Project

**Why this specific problem is relevant right now (Germany, 2026):**

- **Industrial process heat decarbonization is one of the most active investment areas in German industry.** Following the 2022 energy price crisis, gas substitution and process electrification remain strongly incentivized (BAFA/KfW industrial efficiency and heat pump funding schemes).
- **High-temperature industrial heat pumps have matured to commercial readiness** in exactly the temperature range this project targets (up to ~150–165°C), making this a realistic, buildable retrofit rather than a speculative concept.
- **Rising EU ETS carbon prices** are steadily increasing the cost of unabated fossil fuel use in industry, strengthening the economic case for exactly this kind of retrofit.
- **Solvent recovery distillation is a generic, widely applicable unit operation** — found across specialty chemicals, pharmaceuticals, coatings, and food processing — so the findings generalize well beyond a single sector.

---

## 3. What This Project Covers

### Case study
A continuous distillation column recovering ethanol from a dilute aqueous feed (20 wt% ethanol / 80 wt% water, 1000 kg/h), producing a 90 wt% ethanol distillate and a <1.1 wt% ethanol bottoms stream.

### Technical scope
| In scope | Out of scope (noted as future work) |
|---|---|
| Steady-state distillation column simulation | Dynamic/transient simulation |
| Pinch analysis and heat integration | Detailed heat exchanger sizing (UA, area) |
| Mechanical vapor-compression heat pump design | Multi-stage or cascade heat pump configurations |
| Techno-economic analysis (OPEX, CO2, and CAPEX/payback) | Full electrification of the residual auxiliary heat load (treated as a secondary comparison scenario only) |
| Sensitivity analysis on key economic and technical assumptions | Detailed piping/instrumentation (P&ID) design |

### Tools and skills demonstrated
- **DWSIM** (open-source process simulator) — flowsheet simulation, NRTL thermodynamics for the non-ideal ethanol-water system, CoolProp for refrigerant properties
- **Python** (pandas, matplotlib) — pinch/composite curve analysis, techno-economic modeling, sensitivity analysis
- **Process engineering fundamentals** — mass and energy balances, distillation design, heat integration, vapor-compression refrigeration cycle design
- **Engineering documentation practice** — explicit separation of baseline (simulated), assumed (design choices), and calculated (derived) values throughout

---
