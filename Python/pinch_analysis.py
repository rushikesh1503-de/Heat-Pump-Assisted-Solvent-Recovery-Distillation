"""
Pinch / Heat Integration Analysis
Heat-Pump-Assisted Solvent Recovery Distillation Project

Two process streams, both isothermal phase changes:
  - HOT stream:  distillation condenser (source of waste heat, needs cooling)
  - COLD stream: distillation reboiler (heat sink, needs heating)

This script:
  1. Builds composite curves for the two streams
  2. Shows why direct heat exchange is infeasible (hot stream is colder
     than the cold stream's requirement -> negative/zero driving force)
  3. Reports minimum hot/cold utility targets (baseline, no heat pump)
  4. Overlays the heat pump's evaporator/condenser temperatures to show
     how it bridges the gap
  5. Exports a results table (CSV) and a composite curve plot (PNG)
"""

import matplotlib.pyplot as plt
import pandas as pd
import os

# Folder where this Python script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Output files
CSV_FILE = os.path.join(SCRIPT_DIR, "pinch_summary.csv")
PNG_FILE = os.path.join(SCRIPT_DIR, "composite_curves.png")

# ---------------------------------------------------------------------
# 1. Stream data (from converged DWSIM baseline distillation model)
# ---------------------------------------------------------------------

# Hot stream: distillation condenser (releases heat, needs cooling)
T_hot_C = 78.48          # deg C  (351.63 K)
Q_hot_kW = 175.44         # kW available

# Cold stream: distillation reboiler (absorbs heat, needs heating)
T_cold_C = 98.94          # deg C  (372.09 K)
Q_cold_kW = 268.98         # kW required

# Heat pump design points (from DWSIM heat pump model)
T_evap_C = 70.0            # deg C - refrigerant evaporating temperature
T_cond_C = 103.94          # deg C - refrigerant condensing temperature
Q_evap_kW = 175.44          # kW - matches available condenser waste heat
Q_cond_kW = 204.42          # kW - delivered to reboiler
W_comp_kW = 28.97           # kW - compressor electrical work
COP = Q_cond_kW / W_comp_kW

dT_approach_evap = T_hot_C - T_evap_C     # heat source side approach
dT_approach_cond = T_cond_C - T_cold_C    # heat sink side approach

Q_aux_kW = Q_cold_kW - Q_cond_kW          # residual heat still needed
coverage_pct = 100 * Q_cond_kW / Q_cold_kW

# ---------------------------------------------------------------------
# 2. Utility targets WITHOUT heat pump (classical pinch result)
# ---------------------------------------------------------------------
# Because the hot stream (78.48C) is at a LOWER temperature than the cold
# stream needs (98.94C), heat cannot flow directly between them
# (2nd law - no negative-temperature-difference heat transfer).
# => Minimum hot utility = full reboiler duty
# => Minimum cold utility = full condenser duty
# (i.e. with zero process-to-process heat recovery in the baseline case)

Q_hot_utility_min_kW = Q_cold_kW   # steam/gas needed at the reboiler
Q_cold_utility_min_kW = Q_hot_kW   # cooling water needed at the condenser

# ---------------------------------------------------------------------
# 3. Print a clean summary table
# ---------------------------------------------------------------------
summary = pd.DataFrame([
    ["Hot stream (condenser) temperature", f"{T_hot_C:.2f} C"],
    ["Hot stream (condenser) duty", f"{Q_hot_kW:.2f} kW"],
    ["Cold stream (reboiler) temperature", f"{T_cold_C:.2f} C"],
    ["Cold stream (reboiler) duty", f"{Q_cold_kW:.2f} kW"],
    ["", ""],
    ["Baseline min. hot utility (no HP)", f"{Q_hot_utility_min_kW:.2f} kW"],
    ["Baseline min. cold utility (no HP)", f"{Q_cold_utility_min_kW:.2f} kW"],
    ["", ""],
    ["Heat pump evaporator temperature", f"{T_evap_C:.2f} C"],
    ["Heat pump condenser temperature", f"{T_cond_C:.2f} C"],
    ["Approach temp. (evaporator side)", f"{dT_approach_evap:.2f} K"],
    ["Approach temp. (condenser side)", f"{dT_approach_cond:.2f} K"],
    ["Heat pump evaporator duty", f"{Q_evap_kW:.2f} kW"],
    ["Heat pump condenser duty", f"{Q_cond_kW:.2f} kW"],
    ["Compressor work", f"{W_comp_kW:.2f} kW"],
    ["Heating COP", f"{COP:.2f}"],
    ["Reboiler coverage by heat pump", f"{coverage_pct:.1f} %"],
    ["Residual (auxiliary) heating needed", f"{Q_aux_kW:.2f} kW"],
], columns=["Parameter", "Value"])

print(summary.to_string(index=False))
summary.to_csv(CSV_FILE, index=False)

# ---------------------------------------------------------------------
# 4. Composite curve plot
# ---------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 6))

# Hot composite curve: horizontal segment at T_hot_C, from 0 to Q_hot_kW
ax.plot([0, Q_hot_kW], [T_hot_C, T_hot_C], color="firebrick", lw=3,
        label=f"Hot stream: distillation condenser ({Q_hot_kW:.0f} kW @ {T_hot_C:.1f} C)")

# Cold composite curve: horizontal segment at T_cold_C, from 0 to Q_cold_kW
ax.plot([0, Q_cold_kW], [T_cold_C, T_cold_C], color="steelblue", lw=3,
        label=f"Cold stream: distillation reboiler ({Q_cold_kW:.0f} kW @ {T_cold_C:.1f} C)")

# Shade the temperature gap that makes direct exchange infeasible
ax.fill_between([0, min(Q_hot_kW, Q_cold_kW)], T_hot_C, T_cold_C,
                 color="gray", alpha=0.15,
                 label=f"Infeasible gap ({T_cold_C - T_hot_C:.1f} K) \u2014 heat pump lift required")

# Heat pump evaporator / condenser levels
ax.plot([0, Q_evap_kW], [T_evap_C, T_evap_C], color="darkorange", lw=2, ls="--",
        label=f"Heat pump evaporator ({Q_evap_kW:.0f} kW @ {T_evap_C:.1f} C)")
ax.plot([0, Q_cond_kW], [T_cond_C, T_cond_C], color="seagreen", lw=2, ls="--",
        label=f"Heat pump condenser ({Q_cond_kW:.0f} kW @ {T_cond_C:.1f} C)")

# Annotate the lift
ax.annotate("", xy=(Q_evap_kW * 0.5, T_cond_C), xytext=(Q_evap_kW * 0.5, T_evap_C),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
ax.text(Q_evap_kW * 0.52, (T_evap_C + T_cond_C) / 2,
        f"Heat pump lift\n{T_cond_C - T_evap_C:.1f} K", va="center", fontsize=9)

ax.set_xlabel("Cumulative Heat Duty (kW)")
ax.set_ylabel("Temperature (\u00b0C)")
ax.set_title("Composite Curves \u2014 Ethanol Distillation Waste Heat vs. Reboiler Demand")
ax.legend(loc="upper left", fontsize=8, framealpha=0.9)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(PNG_FILE, dpi=150)
print("\nSaved: pinch_summary.csv, composite_curves.png")
