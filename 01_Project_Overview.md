# Heat-Pump-Assisted Solvent Recovery Distillation
## Project Overview: Goal, Motivation, and Scope

---

## 1. Goal

Design, simulate, and economically evaluate the retrofit of an ethanol–water solvent recovery distillation column using a high-temperature industrial heat pump to recover condenser waste heat and supply part of the reboiler duty.

Specifically, the project sets out to:

1. Build and converge a realistic baseline distillation column model.
2. Quantify the condenser (waste heat source) and reboiler (heat sink) duties and temperatures.
3. Establish, through pinch analysis, why direct heat recovery is thermodynamically impossible and a heat pump is required.
4. Design a mechanical vapor-compression heat pump cycle to bridge that gap.
5. Quantify how much of the reboiler demand the heat pump can realistically cover. 
6. Build a preliminary techno-economic case covering energy cost savings, CO2 emissions avoided, CAPEX, simple payback, and sensitivity analysis.

---

## 2. Why This Project

Industrial process heat is an important area for energy efficiency and decarbonization because many chemical processes require continuous high-temperature heating.

Distillation is particularly interesting for heat integration because the condenser rejects heat while the reboiler simultaneously requires heat. However, the condenser temperature may be too low to directly supply the reboiler.

A high-temperature heat pump can overcome this temperature mismatch by using electrical work to upgrade low-temperature waste heat to a higher temperature.

Solvent recovery distillation is widely used in chemical, pharmaceutical, food, and related industries, making the concept applicable to a broad range of industrial processes.

---

## 3. What This Project Covers

### Case study
A continuous distillation column is modelled for recovery of ethanol from a dilute aqueous feed (20 wt% ethanol / 80 wt% water, 1000 kg/h). The column configuration and product specifications are defined in the DWSIM baseline model.

### Technical scope
| In scope | Out of scope (noted as future work) |
|---|---|
| Steady-state distillation column simulation | Dynamic/transient simulation |
| Pinch analysis and heat integration | Physical heat exchanger modelling and sizing (UA, area, pressure drop) | 
| Mechanical vapor-compression heat pump design | Multi-stage or cascade heat pump configurations |
| Techno-economic analysis (OPEX, CO2, and CAPEX/payback) | Full electrification / low-carbon supply of the residual auxiliary heat load |
| Sensitivity analysis on key economic and technical assumptions | Detailed piping/instrumentation (P&ID) design |

---
## 4. Key Preliminary Result

The baseline distillation model requires approximately 269 kW of reboiler heat while approximately 175 kW is available from the distillation condenser.

Because the condenser heat is available at a lower temperature than the reboiler requires, direct heat recovery is not sufficient.

The conceptual heat pump upgrades the available heat and supplies approximately 204 kW to the reboiler, corresponding to approximately 76% coverage of the reboiler duty.

The remaining approximately 24% is supplied by auxiliary heating.

---

## 5. Heat pump design basis

The conceptual heat pump uses R1233zd(E) as the refrigerant and CoolProp for refrigerant thermodynamic properties.

The current design basis uses:

- Evaporation temperature: 70°C
- Condensation temperature: approximately 103.94°C
- Compressor adiabatic efficiency: 75%
- Refrigerant mass flow: approximately 1.47 kg/s
- Compressor power: approximately 29 kW
- Heat pump condenser duty: approximately 204 kW
- Heating COP: approximately 7.1

## 6. Current Model Limitations

The current model is a conceptual steady-state study.

The heat pump evaporator and condenser are represented using simplified Heater/Cooler blocks rather than detailed physical heat exchanger models. Therefore, heat exchanger area, overall heat-transfer coefficients, detailed pressure drops, equipment geometry, and vendor-specific compressor performance are not yet modelled.

The compressor efficiency, temperature approaches, operating hours, energy prices, and CAPEX are engineering assumptions used for preliminary analysis.

These assumptions will be tested through sensitivity analysis and can be refined in future versions.

---
## 7. Tools and skills demonstrated

- **DWSIM** (open-source process simulator) — flowsheet simulation, NRTL thermodynamics for the non-ideal ethanol-water system, CoolProp for refrigerant properties
- **Python** (pandas, matplotlib) — pinch/composite curve analysis, techno-economic modeling, sensitivity analysis
- **Process engineering fundamentals** — mass and energy balances, distillation design, heat integration, vapor-compression refrigeration cycle design
- **Engineering documentation practice** — explicit separation of baseline (simulated), assumed (design choices), and calculated (derived) values throughout

---
