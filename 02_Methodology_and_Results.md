# Heat-Pump-Assisted Solvent Recovery Distillation
## Methodology and Results

---

## 1. Methodology Overview

| Stage | Status |
|---|---|
| 1. Define the case study | Complete |
| 2. Baseline distillation model (DWSIM) | Complete |
| 3. Pinch / heat integration analysis (Python) | Complete |
| 4. Heat pump design and simulation (DWSIM) | Complete |
| 5. Techno-economic analysis - OPEX & CO2 (Python) | Complete |
| 5b. Techno-economic analysis - CAPEX & payback (Python) | Not yet completed |

---

## 2. Baseline Distillation Model

**Tool:** DWSIM 10.2.3.0, NRTL property package (ethanol–water is a strongly non-ideal, minimum-boiling-azeotrope system), Naphtali-Sandholm (simultaneous correction) column solver.

**Feed:** 1000 kg/h (0.278 kg/s), 20 wt% ethanol / 80 wt% water, 298.15 K, 1.013 bar.

**Column configuration:** 12 theoretical stages, feed at stage 8, total condenser, kettle reboiler, atmospheric pressure, no pressure drop assumed.

**Specifications:** distillate and bottoms compositions specified directly (90 wt% and ≤1 wt% ethanol respectively), letting DWSIM solve for the required reflux ratio and reboiler duty.

### Results

| Stream | Temperature | Flow | Composition |
|---|---|---|---|
| Distillate | 351.63 K (78.48°C) | ≈216 kg/h | 90.1 wt% ethanol |
| Bottoms | 372.09 K (98.94°C) | ≈792 kg/h | 1.02 wt% ethanol |

| Duty | Value |
|---|---|
| Condenser duty (heat rejected) | 175.44 kW |
| Reboiler duty (heat required) | 268.98 kW |

**Validation performed:** mass balance closure (distillate + bottoms ≈ feed), energy balance closure around the column (H_feed + Q_reboiler = H_distillate + H_bottoms + Q_condenser, confirmed to within <0.01% ), and an independent hand calculation of condenser duty via vapor boilup rate × latent heat (~172 kW estimated vs. 175.3 kW simulated, ~2% agreement).

---

## 3. Pinch / Heat Integration Analysis

**Tool:** Python (pandas, matplotlib) - see `pinch_analysis.py`.

The column reduces to a two-stream heat integration problem: a hot stream (condenser, 175.44 kW available at 78.48°C) and a cold stream (reboiler, 268.98 kW required at 98.94°C), both isothermal phase changes.

**Key finding:** the hot stream is at a *lower* temperature (78.48°C) than the cold stream requires (98.94°C) - a 20.5 K gap. Since heat cannot flow against a temperature gradient, **direct heat recovery is thermodynamically impossible**, which is the formal justification for the heat pump concept.

**Baseline utility targets (no heat pump):** minimum hot utility = 268.98 kW (full reboiler duty from an external source), minimum cold utility = 175.44 kW (full condenser duty rejected to cooling water).

See `composite_curves.png` for the visual composite curve, including the heat pump's evaporator/condenser levels overlaid to show how the 33.9 K lift bridges the gap.

---

## 4. Heat Pump Design

**Tool:** DWSIM, CoolProp property package, R1233zd(E) refrigerant (a low-GWP fluid suited to this temperature range, with commercially available high-temperature heat pump hardware).

**Cycle:** Evaporator → Compressor → Condenser → Expansion valve → Evaporator (standard mechanical vapor-compression cycle).

### Assumed design choices 

| Parameter | Value | Basis |
|---|---|---|
| Evaporator temperature | 70°C (343.15 K) | 8.48 K approach below condenser source temp (78.48°C) |
| Condensing temperature | 103.94°C (377.09 K) | 5 K approach above reboiler temp (98.94°C) |
| Compressor adiabatic efficiency | 75% | Realistic first-pass assumption for a mid-size compressor |

### Calculated results

| Parameter | Value |
|---|---|
| Evaporator pressure | 511.96 kPa |
| Condensing pressure | 1136.57 kPa |
| Refrigerant mass flow | 1.4707 kg/s (solved so evaporator duty matches available waste heat) |
| Compressor power | 28.97 kW |
| Heat pump condenser duty (delivered to reboiler) | 204.42 kW |
| **Heating COP** | **≈7.05–7.06** |
| **Reboiler coverage by heat pump** | **76.0%** |
| Residual auxiliary heat still required (existing gas/steam) | 64.56 kW |

**Sanity check:** COP is compared against the Carnot limit (COP_Carnot = T_cond / (T_cond − T_evap) ≈ 11.1 in absolute temperature terms); the real COP sits at ~63% of Carnot, consistent with realistic vapor-compression performance at this lift.

**Known limitation carried into future work:** the compressor outlet in the current model sits very close to the refrigerant's saturation line (minimal superheat). Adding a small deliberate superheat margin (3–5 K) at the compressor inlet is planned as a refinement for realism and to avoid liquid-carryover risk in a real design.

---

## 5. Techno-Economic Analysis - Energy Cost and CO2 (OPEX)

**Tool:** Python - see `techno_economic.py`.

### Operating and pricing assumptions (explicitly stated, sourced)

| Assumption | Value | Source / basis |
|---|---|---|
| Operating hours | 8000 h/yr | Continuous industrial process assumption |
| Existing boiler efficiency | 88% | Typical for an existing industrial gas/steam system |
| Industrial gas price | 7.0 ct/kWh | Representative large-volume (RLM) industrial gas contract, Germany 2026 |
| Industrial electricity price | 17.2 ct/kWh | BDEW 2026 average, small/medium industrial delivery contracts |
| Natural gas CO2 factor | 201 g CO2/kWh | Standard combustion emission factor |
| German grid electricity CO2 factor | 344 g CO2/kWh | Umweltbundesamt (UBA), official 2025 figure |

### Results: baseline (100% gas) vs. retrofit (heat pump + gas top-up)

| Metric | Baseline | Retrofit | Change |
|---|---|---|---|
| Annual gas consumption | 2445 MWh/yr | 587 MWh/yr | −76% |
| Annual electricity consumption | 0 MWh/yr | 232 MWh/yr | + |
| **Annual energy cost** | **€171,169/yr** | **€80,946/yr** | **−€90,223/yr (−52.7%)** |
| **Annual CO2 emissions** | **491 t/yr** | **198 t/yr** | **−294 t/yr (−59.8%)** |

**Notable finding:** cost savings (52.7%) exceed the heat pump's coverage of reboiler duty (76%, in energy terms - note this is *not* directly comparable to the cost % without accounting for COP). This is because, per unit of *delivered heat*, the heat pump is substantially cheaper than gas: electricity at 17.2 ct/kWh delivered through a COP of ~7.06 costs approximately 2.4 ct per kWh of heat, versus gas at 7.0 ct/kWh through an 88% efficient boiler costing approximately 8.0 ct per kWh of heat - roughly a 3x cost advantage per unit of heat delivered.

---
## 6. Techno-Economic Analysis - CAPEX and Payback
 
**Tool:** Python - see `capex_payback.py`.
 
Vendor quotes were not available, so CAPEX is estimated from published industrial high-temperature heat pump cost literature and presented as a **Low/Base/High range**, not a single number - the literature itself reports specific investment costs varying by roughly 5x depending on scale, temperature, and scope (200–1500 EUR/kW across all HTHP technologies; 300–900 EUR/kW_thermal bare equipment specifically for heat delivery up to 160°C, per Blue Terra 2008 as reviewed by energy.nl). An installation factor (2.0–3.0x bare equipment cost) is applied to account for labor, piping, controls, and engineering, consistent with the literature noting installed cost runs "several times" bare equipment cost.
 
| Case | Specific cost | Installation factor | Total installed CAPEX | Simple payback | NPV (8%, 15 yr) |
|---|---|---|---|---|---|
| Low | 300 EUR/kWth | 2.0x | €122,652 | 1.4 years | €649,610 |
| **Base** | **500 EUR/kWth** | **2.5x** | **€255,525** | **2.8 years** | **€516,737** |
| High | 900 EUR/kWth | 3.0x | €551,934 | 6.1 years | €220,328 |
 
**Conclusion:** even in the pessimistic (High) cost case, payback (6.1 years) sits close to a typical 5-year industrial investment hurdle, and the base case (2.8 years) is comfortably attractive. NPV is positive in all three cases over a 15-year service life at an 8% discount rate - the retrofit is a defensible investment across the full range of realistic cost uncertainty, not just in an optimistic scenario.
 
## 7. Not Yet Completed
 
- **Sensitivity analysis**: electricity price, gas price, and CAPEX uncertainty ranges, plus a DWSIM-based sensitivity sweep on compressor efficiency and condensing temperature vs. COP.
- **Full-electrification comparison scenario**: cost/CO2 case if the residual 64.56 kW were supplied by direct electric resistance heating instead of gas.
- **Detailed heat exchanger sizing**: UA/area for the evaporator and condenser (currently modeled as ideal Heater/Cooler blocks).
- **Final PFD** (before/after) and written technical report.
- **GitHub packaging** of all DWSIM files, Python scripts, plots, and documentation.
---
 
## 8. Files Produced So Far
 
| File | Description |
|---|---|
| `Heat-Pump-Assisted_Solvent_Recovery_Distillation.dwxmz` | DWSIM flowsheet (distillation column + heat pump cycle) |
| `pinch_analysis.py`, `pinch_summary.csv`, `composite_curves.png` | Pinch / heat integration analysis |
| `techno_economic.py`, `techno_economic_baseline_vs_retrofit.csv`, `baseline_vs_retrofit.png` | OPEX and CO2 techno-economic comparison |
| `capex_payback.py`, `capex_payback.csv`, `capex_payback.png` | CAPEX and payback (Low/Base/High literature-cost range), with NPV |

