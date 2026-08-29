# Heat Pump Assisted Solvent Recovery Distillation
## Methodology and Results

This document explains the complete conceptual process model developed for the project, from the baseline distillation column to heat pump integration and the preliminary techno economic analysis.

The project is designed as a self learning engineering project using **DWSIM for process simulation** and **Python for heat integration and techno economic calculations**.

---

# 1. Project Objective

The objective is to investigate whether heat rejected by a solvent recovery distillation column can be recovered and upgraded with a high temperature heat pump so that it can be reused for the column reboiler.

The basic concept is:

**Distillation condenser → Heat pump evaporator → Compressor → Heat pump condenser → Distillation reboiler**

The condenser of the distillation column provides a relatively low temperature heat source. The heat pump raises this heat to a higher temperature so that it can be supplied to the reboiler.

The project therefore investigates:

- the baseline energy demand of the distillation process
- the temperature mismatch between condenser and reboiler
- heat pump thermodynamic performance
- reduction in external heating demand
- preliminary energy cost and CO₂ savings
- CAPEX, payback and sensitivity
- limitations of the conceptual model

---

# 2. Project Workflow

The project follows these stages:

| Stage | Status | Main tool |
|---|---|---|
| 1. Define case study | Complete | Engineering assumptions |
| 2. Baseline distillation model | Complete | DWSIM |
| 3. Heat integration / pinch analysis | Complete | Python |
| 4. Heat pump design and integration | Complete | DWSIM |
| 5. OPEX and CO₂ analysis | Complete | Python |
| 6. CAPEX and payback analysis | Complete | Python |
| 7. Sensitivity analysis | Complete | Python |
| 8. Detailed heat exchanger sizing | Future work | DWSIM / engineering calculations |
| 9. Full electrification scenario | Future work | Python |

---

# 3. Case Study Definition

A simplified ethanol water solvent recovery process was selected.

The feed represents a dilute ethanol stream that is separated in a distillation column. The overhead condenser rejects heat, while the reboiler requires heat.

## 3.1 Feed

| Parameter | Value |
|---|---:|
| Feed flow | 1000 kg/h |
| Feed flow | 0.278 kg/s |
| Ethanol | 20 wt% |
| Water | 80 wt% |
| Feed temperature | 298.15 K (25°C) |
| Feed pressure | 101325 Pa (1.013 bar) |

The feed contains only ethanol and water. R1233zd(E) is used only in the separate heat pump cycle.

---

# 4. Baseline Distillation Model in DWSIM

## 4.1 Software and thermodynamic model

The baseline distillation column was simulated in:

**DWSIM 10.2.3.0**

The **NRTL property package** was selected for the ethanol water mixture because the system is strongly non ideal.

The column uses the:

**Naphtali Sandholm steady state column solver**

This solves the material and energy balances for the column stages simultaneously.

---

# 5. Distillation Column Configuration

The following configuration was used in the baseline model.

| DWSIM setting | Value |
|---|---:|
| Number of theoretical stages | 12 |
| Feed stage | 8 |
| Condenser type | Total |
| Reboiler type | Kettle |
| Condenser/top pressure | 101325 Pa |
| Column pressure drop | 0 Pa |
| Condenser pressure drop | 0 Pa |
| Reflux ratio | 2 |
| Feed temperature | 298.15 K |
| Feed pressure | 101325 Pa |
| Feed flow | 1000 kg/h |
| Property package | NRTL |
| Column solver | Naphtali Sandholm |

The pressure drop is set to zero because this is a conceptual model rather than a detailed equipment design.

---

# 6. Distillation Specifications

The column is operated with a reflux ratio of **2**.

The bottoms product is specified using a product molar flow specification for ethanol of approximately:

**12.06 mol/s**

DWSIM then calculates the resulting product conditions and column duties.

The important point is that the column is first solved independently as the **baseline process**. The heat pump is added only after the baseline condenser and reboiler duties have been established.

---

# 7. Baseline Distillation Results

The converged DWSIM model gives approximately:

## 7.1 Product streams

| Stream | Temperature | Pressure | Flow |
|---|---:|---:|---:|
| Distillate | 351.63 K (78.48°C) | 101325 Pa | ≈0.06 kg/s |
| Bottoms | 372.09 K (98.94°C) | 101325 Pa | ≈0.22 kg/s |

The feed and product flow rates close approximately to the overall feed flow.

## 7.2 Column duties

| Duty | Value |
|---|---:|
| Condenser duty | ≈175.44 kW heat rejected |
| Reboiler duty | ≈268.98 kW heat required |

The signs shown by DWSIM depend on its energy stream convention. In this project, duties are discussed using their physical meaning:

- **Condenser:** approximately 175.44 kW of heat is rejected.
- **Reboiler:** approximately 268.98 kW of heat must be supplied.

Small differences in the last decimal places can occur when DWSIM recalculates the flowsheet. The final baseline used for the Python calculations should therefore be frozen after the DWSIM case is finalized.

---

# 8. Baseline Energy Balance

The baseline column has two important energy demands:

### Condenser

The overhead vapor must be condensed, releasing approximately:

**175.44 kW**

### Reboiler

The column requires approximately:

**268.98 kW**

of heat at the reboiler.

Therefore, the available condenser heat is smaller than the reboiler requirement:

\[
268.98-175.44=93.54\;kW
\]

More importantly, the condenser heat is at a lower temperature than the reboiler requires.

This temperature mismatch is the reason direct heat recovery is not sufficient.

---

# 9. Heat Integration / Pinch Analysis

The baseline process can be simplified into two main thermal streams:

### Hot stream

Distillation condenser:

**78.48°C**

Available heat:

**≈175.44 kW**

### Cold stream

Distillation reboiler:

**98.94°C**

Required heat:

**≈268.98 kW**

The temperature difference is:

\[
98.94-78.48=20.46\;K
\]

Therefore, the condenser heat cannot directly drive the reboiler while maintaining a positive temperature driving force.

A heat pump is introduced to overcome this temperature mismatch.

The Python pinch analysis represents these streams and illustrates the temperature gap.

---

# 10. Heat Pump Concept

The heat pump is modelled as a closed mechanical vapor compression cycle.

The cycle consists of:

1. Evaporator
2. Compressor
3. Condenser
4. Expansion valve

The refrigerant circulates continuously inside the heat pump.

The process heat and refrigerant are not mixed.

Only heat is transferred between the two systems.

## Energy flow

```text 
DISTILLATION CONDENSER
        │
        │ Low temperature heat
        ▼
HEAT PUMP EVAPORATOR
        │
        ▼
COMPRESSOR
        │
        │ Temperature and pressure increased
        ▼
HEAT PUMP CONDENSER
        │
        │ High temperature heat
        ▼
DISTILLATION REBOILER
```

---

# 11. Heat Pump Thermodynamic Package

The heat pump was modelled separately from the distillation column.

| Parameter | Setting |
|---|---|
| Software | DWSIM |
| Property package | CoolProp |
| Refrigerant | R1233zd(E) |
| Cycle | Vapor compression |
| Compressor process | Adiabatic |
| Compressor efficiency | 75% |

The distillation system uses **NRTL**, while the heat pump uses **CoolProp**.

This separation is intentional because the two systems have different thermodynamic requirements.

---

# 12. Heat Pump Temperature Assumptions

The heat pump temperatures were selected from the temperatures calculated by the baseline distillation model.

## 12.1 Evaporator temperature

The distillation condenser operates at approximately:

**78.48°C**

A refrigerant evaporation temperature of:

**70°C**

was selected.

Therefore:

\[
\Delta T_{evap}=78.48-70
\]

\[
\Delta T_{evap}=8.48\;K
\]

This temperature difference represents the assumed driving force between the distillation condenser heat source and the heat pump evaporator.

---

## 12.2 Condensing temperature

The distillation reboiler operates at approximately:

**98.94°C**

A heat pump condensing temperature of:

**103.94°C**

was selected.

Therefore:

$$
\Delta T_{cond}=103.94-98.94
$$

$$
\Delta T_{cond}=5.00\;K
$$

This provides the temperature driving force required to transfer heat from the heat pump condenser to the reboiler.

---

# 13. Heat Pump Pressure Levels

The selected refrigerant temperatures correspond to approximately:

| State | Temperature | Pressure |
|---|---:|---:|
| Evaporator / compressor inlet | 70°C | 511.96 kPa |
| Compressor outlet / condenser inlet | ≈103.94°C | 1136.57 kPa |
| Condenser outlet | ≈103.94°C | 1136.57 kPa |
| Expansion valve outlet | 70°C | 511.96 kPa |

The pressure ratio of the compressor is approximately:

$$
\frac{1136.57}{511.96}\approx2.22
$$

Pressure losses in the heat exchangers, piping and fittings are neglected in this conceptual model.

---

# 14. Compressor Model

The compressor is configured as an **adiabatic compressor**.

### Main settings

| Parameter | Value |
|---|---:|
| Calculation type | Outlet pressure |
| Outlet pressure | 1.13657 MPa |
| Pressure increase | ≈624.61 kPa |
| Pressure ratio | ≈2.22 |
| Adiabatic efficiency | 75% |
| Rotation speed shown in DWSIM | 1500 rpm |

The 75% compressor efficiency is an engineering assumption for this preliminary study. It is not a vendor value.

DWSIM calculates the compressor power from the selected pressure ratio, refrigerant properties and efficiency.

The calculated compressor power is approximately:

**28.97 kW**

---

# 15. How the Refrigerant Mass Flow Was Determined

The refrigerant mass flow was **not selected arbitrarily**.

The available heat from the distillation condenser was used as the target evaporator duty.

The calculation follows:

$$
Q_{evap}=
\dot m_{ref}(h_{out}-h_{in})
$$

Therefore:

$$
\dot m_{ref} =
\frac{Q_{evap}}
{h_{out}-h_{in}}
$$

In DWSIM, the refrigerant mass flow was adjusted iteratively until the heat absorbed by the evaporator approximately matched the available condenser heat.

The resulting refrigerant flow was approximately:

**1.4707 kg/s**

This gives an evaporator duty of approximately:

**175.44 kW**

The flow rate is therefore a **calculated/iteratively adjusted design result**, not a primary assumption.

---

# 16. Heat Pump Energy Connection in DWSIM

The distillation condenser duty was represented by an energy stream:

**Q_Distillation_Condenser**

This energy stream was connected to the heat pump evaporator.

Therefore the model contains an actual thermal connection between the baseline distillation process and the heat pump rather than simply copying a number from one calculation into another.

The heat pump absorbs heat from the distillation condenser and releases upgraded heat at its condenser.

---

# 17. Heat Pump Condenser

The heat pump condenser operates at approximately:

**103.94°C**

and releases approximately:

**204.42 kW**

of heat.

This heat is intended to supply part of the distillation reboiler duty.

The energy stream is named:

**Q_HP_Condenser**

The heat pump condenser is therefore the high temperature heat source for the reboiler.

---

# 18. Why the Heat Pump Does Not Supply 100% of the Reboiler

The baseline reboiler requires approximately:

$$
Q_{reboiler}=268.98\;kW
$$

The heat pump supplies approximately:

$$
Q_{HP}=204.42\;kW
$$

Therefore the remaining duty is:

$$
Q_{aux}=268.98-204.42
$$

$$
Q_{aux}\approx64.56\;kW
$$

The heat pump coverage is:

$$
Coverage=
\frac{204.42}{268.98}\times100
$$

$$
Coverage\approx76\%
$$

Thus the conceptual retrofit is a **hybrid heating system**:

- approximately 76% of the reboiler duty comes from the heat pump
- approximately 24% remains supplied by the existing auxiliary heating system

This is not a modelling failure. It results from the fact that the available condenser heat is limited.

---

# 19. Heating COP

The heating coefficient of performance is calculated as:

$$
COP_{heating}=
\frac{Q_{cond}}{W_{comp}}
$$

Using the DWSIM results:

$$
COP_{heating}=
\frac{204.42}{28.97}
$$

$$
COP_{heating}\approx7.06
$$

The COP is a calculated result of the conceptual heat pump model.

For comparison, the ideal Carnot heating COP between the selected temperature levels is:

$$
COP_{Carnot}=
\frac{T_{cond}}
{T_{cond}-T_{evap}}
$$

using absolute temperature in kelvin.

The calculated heat pump COP is below this theoretical maximum, as expected.

---

# 20. Heat Pump Assumptions

The main assumptions used in the current conceptual model are:

| Assumption | Value / treatment |
|---|---|
| Refrigerant | R1233zd(E) |
| Heat pump property package | CoolProp |
| Evaporation temperature | 70°C |
| Condensation temperature | 103.94°C |
| Evaporator approach | 8.48 K |
| Condenser approach | 5 K |
| Compressor efficiency | 75% |
| Pressure drops | Neglected |
| Refrigerant heat exchanger model | Idealized Heater/Cooler blocks |
| Compressor process | Adiabatic |
| Refrigerant loop | Closed |
| Refrigerant leakage | Not considered |
| Mechanical/electrical motor losses | Not separately modelled |
| Detailed exchanger area | Not calculated |
| Detailed compressor sizing | Not calculated |

---

# 21. Important Limitation: Heater/Cooler Blocks

The current DWSIM heat pump model uses idealized **Heater/Cooler type blocks** to represent the evaporator and condenser.

This is appropriate for the current learning objective because it allows the thermodynamic energy balance and temperature levels to be investigated.

However, these blocks do **not** represent a final physical heat exchanger design.

The current model does not calculate:

- heat transfer coefficient
- overall heat transfer coefficient
- heat exchanger area
- tube dimensions
- number of tubes
- flow arrangement
- pressure drop
- fouling
- detailed exchanger cost

Therefore, the current heat pump result demonstrates **conceptual thermodynamic feasibility**, not final equipment design.

Detailed heat exchanger sizing is planned as future work.

---

# 22. Baseline vs Assumed vs Calculated Values

Keeping these categories separate is important for interpreting the project.

## Baseline DWSIM results

These come from the independently solved distillation model:

- Distillate temperature ≈ 351.63 K
- Bottoms temperature ≈ 372.09 K
- Condenser duty ≈ 175.44 kW
- Reboiler duty ≈ 268.98 kW

## Engineering assumptions

These were selected by the project author:

- Evaporator temperature = 70°C
- Condensing temperature = 103.94°C
- Evaporator approach = 8.48 K
- Condenser approach = 5 K
- Compressor efficiency = 75%
- 8000 operating hours/year
- 88% existing boiler efficiency
- Energy price assumptions
- CAPEX assumptions

## Calculated heat pump results

These result from the DWSIM heat pump model:

- Evaporator pressure ≈ 511.96 kPa
- Condenser pressure ≈ 1136.57 kPa
- Refrigerant flow ≈ 1.4707 kg/s
- Compressor power ≈ 28.97 kW
- Heat pump condenser duty ≈ 204.42 kW
- Heating COP ≈ 7.06
- Reboiler coverage ≈ 76%
- Auxiliary heating requirement ≈ 64.56 kW

---

# 23. Techno Economic Analysis

The DWSIM results are passed to Python for preliminary economic analysis.

The analysis considers:

- annual operating hours
- natural gas consumption
- electricity consumption
- energy cost
- CO₂ emissions
- heat pump CAPEX
- simple payback
- NPV
- sensitivity to energy prices and CAPEX

The main Python files are:

- `techno_economic.py`
- `capex_payback.py`
- `sensitivity_analysis.py`

---

# 24. Operating Assumptions

The current economic model uses:

| Parameter | Assumption |
|---|---:|
| Operating hours | 8000 h/year |
| Existing boiler efficiency | 88% |
| Natural gas price | 7.0 ct/kWh |
| Electricity price | 17.2 ct/kWh |
| Natural gas CO₂ factor | 201 g CO₂/kWh |
| Grid electricity CO₂ factor | 344 g CO₂/kWh |

These are preliminary economic assumptions and should not be interpreted as project specific commercial quotations.

---

# 25. Energy Cost Results

The conceptual comparison is:

| Metric | Baseline | Heat pump retrofit |
|---|---:|---:|
| Annual gas consumption | ≈2445 MWh/year | ≈587 MWh/year |
| Annual electricity consumption | 0 | ≈232 MWh/year |
| Annual energy cost | ≈€171,169/year | ≈€80,946/year |
| Annual energy cost reduction | — | ≈€90,223/year |
| Cost reduction | — | ≈52.7% |

The retrofit does not eliminate gas consumption because approximately 24% of the reboiler duty remains as auxiliary heat.

The heat pump requires electricity, but the high COP means that one unit of electricity produces several units of useful heating.

---

# 26. CO₂ Results

The preliminary comparison gives:

| Metric | Baseline | Retrofit |
|---|---:|---:|
| Annual CO₂ emissions | ≈491 t/year | ≈198 t/year |
| CO₂ reduction | — | ≈294 t/year |
| Relative reduction | — | ≈59.8% |

The result includes emissions associated with electricity consumption using the assumed grid emission factor.

Therefore, the retrofit does not automatically represent zero carbon operation. Its environmental benefit depends partly on the electricity source.

---

# 27. CAPEX and Payback

Because vendor quotations are not available, the heat pump CAPEX is treated as an estimate rather than a quotation.

The current Python model evaluates three cases:

| Case | Specific cost | Installation factor | Installed CAPEX | Payback |
|---|---:|---:|---:|---:|
| Low | 300 €/kWth | 2.0× | ≈€122,652 | ≈1.4 years |
| Base | 500 €/kWth | 2.5× | ≈€255,525 | ≈2.8 years |
| High | 900 €/kWth | 3.0× | ≈€551,934 | ≈6.1 years |

The base case is used as the main economic reference.

The analysis also calculates NPV over a 15 year period using an 8% discount rate.

These figures should be interpreted as **preliminary screening estimates**, not a bankable investment study.

---

# 28. Sensitivity Analysis

The sensitivity analysis varies important uncertain inputs individually.

The current analysis considers:

- natural gas price
- electricity price
- CAPEX

The purpose is to determine which assumptions have the greatest influence on project payback.

The current results indicate that gas price and CAPEX have a stronger influence on payback than electricity price within the selected sensitivity ranges.

This is useful because energy prices and equipment costs are major uncertainties in an early stage heat pump project.

---

# 29. Overall Energy Concept

The complete concept can be summarized as:

```text
                    DISTILLATION COLUMN
                           │
              ┌────────────┴────────────┐
              │                         │
         OVERHEAD                    BOTTOMS
              │                         │
              ▼                         ▲
       DISTILLATION                 REBOILER
         CONDENSER                      │
              │                         │
              │ Heat                    │ Heat
              ▼                         │
        HP EVAPORATOR                   │
              │                         │
              ▼                         │
         COMPRESSOR                     │
              │                         │
              ▼                         │
         HP CONDENSER ──────────────────┘
              │
              │
        Heat pump upgrades
        low temperature heat
        to a useful temperature
```

The heat pump therefore acts as a **thermal bridge** between the distillation condenser and reboiler.

---

# 30. Current Project Status

At this stage, the project has demonstrated a complete conceptual workflow:

**Baseline process → heat integration analysis → heat pump simulation → energy savings → CO₂ analysis → CAPEX/payback → sensitivity analysis**

The DWSIM flowsheet contains:

- ethanol water distillation
- condenser and reboiler
- heat pump evaporator
- compressor
- heat pump condenser
- expansion valve
- refrigerant loop
- energy connection between the distillation condenser and heat pump
- energy connection between the heat pump condenser and the reboiler concept

The current model is suitable for demonstrating the **thermodynamic concept and preliminary economic potential**.

---

# 31. What Has Not Yet Been Modelled

The following items are intentionally outside the current conceptual model:

### Detailed heat exchanger design

Future work can replace the idealized Heater/Cooler blocks with actual heat exchanger models and calculate:

- UA
- heat transfer area
- heat transfer coefficients
- pressure drops
- exchanger configuration

### Full electrification

A separate scenario can investigate supplying the remaining approximately 64.56 kW auxiliary duty using electricity rather than gas.

This should be evaluated economically and environmentally rather than assuming that electricity is automatically the best option.

### More realistic heat pump cycle

Future refinement could include:

- compressor inlet superheat
- condenser outlet subcooling
- heat exchanger pressure drops
- compressor motor efficiency
- mechanical losses
- realistic compressor performance curves

### Equipment level design

Vendor data would eventually be required for:

- compressor selection
- heat exchanger selection
- controls
- pumps and auxiliaries
- installation cost
- maintenance cost

---

# 32. Final Interpretation

The conceptual study shows that the distillation condenser rejects useful heat at a temperature below the temperature required by the reboiler.

Direct heat recovery is therefore not sufficient.

A heat pump can upgrade this heat to a higher temperature.

For the current design case:

- approximately **175 kW** is available from the distillation condenser
- approximately **204 kW** is delivered by the heat pump condenser
- approximately **29 kW** of compressor electricity is required
- the calculated heating COP is approximately **7.06**
- approximately **76%** of the reboiler duty can be covered
- approximately **24%** remains as auxiliary heating

The project therefore demonstrates the principle of using a heat pump as a temperature upgrading device for distillation heat integration.

The next engineering step is not to keep changing the conceptual cycle indefinitely. The baseline should be frozen and the project should move toward **realistic heat exchanger sizing, improved heat pump assumptions, and validation of the economic assumptions**.
