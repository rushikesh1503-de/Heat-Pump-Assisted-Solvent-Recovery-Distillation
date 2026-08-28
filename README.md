# Heat-Pump-Assisted Solvent Recovery Distillation

Process simulation and techno-economic feasibility study of retrofitting an ethanol-water solvent recovery distillation column with a high-temperature industrial heat pump, recovering the column's own condenser waste heat to partially replace steam heating at the reboiler.

Built as a portfolio project demonstrating end-to-end chemical process engineering: process simulation, heat integration, equipment design, and techno-economic analysis, using tools and methods directly relevant to current industrial decarbonization work in Germany and beyond.

---

## Key Results

| Metric | Result |
|---|---|
| Distillation reboiler duty | 268.98 kW |
| Distillation condenser waste heat available | 175.44 kW |
| Heat pump refrigerant | R1233zd(E) |
| Heating COP | 7.06 |
| Reboiler duty covered by heat pump | 76% |
| Annual energy cost savings | EUR 90,223/yr (52.7%) |
| Annual CO2 savings | 294 t/yr (59.8%) |
| Simple payback (base case) | 2.8 years |
| Payback range (literature CAPEX uncertainty) | 1.4 - 6.1 years |

![Retrofit png](docs/HP_Distillation.png)

---

## Why This Project

Industrial process heat decarbonization is one of the most active investment areas in German industry right now. High-temperature heat pumps have matured to commercial readiness in exactly the 100-160 degC range this project targets, and rising EU ETS carbon prices keep strengthening the economic case. Solvent recovery distillation is a generic unit operation found across specialty chemicals, pharma, coatings, and food processing, so the approach here generalizes well beyond a single sector.

Full motivation and scope: [`docs/01_Project_Overview.md`](docs/01_Project_Overview.md)

---

## Method

1. **Baseline distillation model** (DWSIM, NRTL) - converged mass and energy balance for the ethanol-water column.
2. **Pinch analysis** (Python) - showed the 20.5 K temperature gap that makes direct heat recovery impossible, justifying the heat pump.
3. **Heat pump design** (DWSIM, CoolProp, R1233zd(E)) - full vapor-compression cycle, solved for the refrigerant flow rate that matches available waste heat.
4. **Techno-economic analysis** (Python) - OPEX, CO2, CAPEX (literature-based range), payback, NPV, and sensitivity analysis.

Full methodology and all intermediate results: [`docs/02_Methodology_and_Results.md`](docs/02_Methodology_and_Results.md)

---

## Tools

- **DWSIM** (open-source process simulator) - flowsheet simulation, NRTL and CoolProp thermodynamics
- **Python** (pandas, matplotlib) - pinch analysis, techno-economic modeling, sensitivity analysis, PFD generation

## Assumptions and Limitations

All economic and design assumptions (temperature approaches, compressor efficiency, energy prices, CO2 factors, CAPEX basis) are explicitly stated and sourced in [`docs/02_Methodology_and_Results.md`](docs/02_Methodology_and_Results.md). Known limitations: heat exchangers modeled as ideal duty blocks rather than sized equipment; CAPEX is a literature-based range rather than a vendor quote.

---