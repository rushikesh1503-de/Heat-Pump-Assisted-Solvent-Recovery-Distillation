"""
Techno-Economic Analysis (Part 1): Baseline vs. Heat Pump Retrofit
Heat-Pump-Assisted Solvent Recovery Distillation Project

Compares the annual energy cost and CO2 emissions of:
  (A) Baseline: reboiler fully fired by natural gas / steam
  (B) Retrofit: heat pump covers 76% of reboiler duty (electricity),
      remaining 24% still supplied by gas

All economic/emission factors below are explicit, sourced assumptions —
see comments. Adjust freely for your own sensitivity analysis.
"""

import pandas as pd
import os

# Folder where this Python script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Output files
CSV_FILE = os.path.join(SCRIPT_DIR, "techno_economic_baseline_vs_retrofit.csv")
PNG_FILE = os.path.join(SCRIPT_DIR, "baseline_vs_retrofit.png")

# ---------------------------------------------------------------------
# 1. Process results (from converged DWSIM models — not assumptions)
# ---------------------------------------------------------------------
Q_reboiler_kW = 268.98        # total reboiler duty required
Q_HP_kW = 204.42               # heat pump contribution
Q_aux_kW = Q_reboiler_kW - Q_HP_kW   # residual gas-fired top-up = 64.56 kW
W_comp_kW = 28.97               # heat pump compressor electrical power
COP = Q_HP_kW / W_comp_kW

# ---------------------------------------------------------------------
# 2. Operating assumptions 
# ---------------------------------------------------------------------
operating_hours = 8000          # h/yr - continuous process assumption
boiler_efficiency = 0.88        # existing gas-fired steam boiler, typical value

# German industrial energy prices, 2026 (see sources in accompanying text)
price_gas_EUR_kWh = 0.070       # large-volume industrial gas contract (BDEW-adjacent estimate)
price_elec_EUR_kWh = 0.172      # BDEW 2026 avg., small/medium industrial delivery contracts

# Emission factors
ef_gas_kgCO2_kWh = 0.201        # natural gas combustion, standard factor
ef_elec_kgCO2_kWh = 0.344       # German grid mix 2025 (UBA, official)

# ---------------------------------------------------------------------
# 3. Baseline case: 100% gas-fired reboiler
# ---------------------------------------------------------------------
gas_input_kW_baseline = Q_reboiler_kW / boiler_efficiency
gas_MWh_yr_baseline = gas_input_kW_baseline * operating_hours / 1000

cost_baseline_EUR_yr = gas_MWh_yr_baseline * 1000 * price_gas_EUR_kWh
co2_baseline_t_yr = gas_MWh_yr_baseline * 1000 * ef_gas_kgCO2_kWh / 1000

# ---------------------------------------------------------------------
# 4. Retrofit case: heat pump (electricity) + residual gas top-up
# ---------------------------------------------------------------------
elec_MWh_yr_retrofit = W_comp_kW * operating_hours / 1000
gas_input_kW_retrofit = Q_aux_kW / boiler_efficiency
gas_MWh_yr_retrofit = gas_input_kW_retrofit * operating_hours / 1000

cost_elec_EUR_yr = elec_MWh_yr_retrofit * 1000 * price_elec_EUR_kWh
cost_gas_EUR_yr_retrofit = gas_MWh_yr_retrofit * 1000 * price_gas_EUR_kWh
cost_retrofit_EUR_yr = cost_elec_EUR_yr + cost_gas_EUR_yr_retrofit

co2_elec_t_yr = elec_MWh_yr_retrofit * 1000 * ef_elec_kgCO2_kWh / 1000
co2_gas_t_yr_retrofit = gas_MWh_yr_retrofit * 1000 * ef_gas_kgCO2_kWh / 1000
co2_retrofit_t_yr = co2_elec_t_yr + co2_gas_t_yr_retrofit

# ---------------------------------------------------------------------
# 5. Savings
# ---------------------------------------------------------------------
cost_savings_EUR_yr = cost_baseline_EUR_yr - cost_retrofit_EUR_yr
cost_savings_pct = 100 * cost_savings_EUR_yr / cost_baseline_EUR_yr

co2_savings_t_yr = co2_baseline_t_yr - co2_retrofit_t_yr
co2_savings_pct = 100 * co2_savings_t_yr / co2_baseline_t_yr

# ---------------------------------------------------------------------
# 6. Results table
# ---------------------------------------------------------------------
results = pd.DataFrame([
    ["Heating COP", f"{COP:.2f}", ""],
    ["Reboiler coverage by heat pump", "76.0 %", ""],
    ["", "", ""],
    ["Annual gas consumption", f"{gas_MWh_yr_baseline:.0f} MWh/yr", f"{gas_MWh_yr_retrofit:.0f} MWh/yr"],
    ["Annual electricity consumption", "0 MWh/yr", f"{elec_MWh_yr_retrofit:.0f} MWh/yr"],
    ["Annual energy cost", f"{cost_baseline_EUR_yr:,.0f} EUR/yr", f"{cost_retrofit_EUR_yr:,.0f} EUR/yr"],
    ["Annual CO2 emissions", f"{co2_baseline_t_yr:.0f} t/yr", f"{co2_retrofit_t_yr:.0f} t/yr"],
], columns=["Parameter", "Baseline (100% gas)", "Retrofit (heat pump + gas top-up)"])

print(results.to_string(index=False))
print(f"\nAnnual cost savings: {cost_savings_EUR_yr:,.0f} EUR/yr ({cost_savings_pct:.1f}%)")
print(f"Annual CO2 savings:  {co2_savings_t_yr:.0f} t/yr ({co2_savings_pct:.1f}%)")

results.to_csv(CSV_FILE, index=False)

# ---------------------------------------------------------------------
# 7. Bar chart: cost and CO2, baseline vs. retrofit
# ---------------------------------------------------------------------
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(11, 5))

cases = ["Baseline\n(100% gas)", "Retrofit\n(heat pump + gas top-up)"]

axes[0].bar(cases, [cost_baseline_EUR_yr, cost_retrofit_EUR_yr], color=["firebrick", "seagreen"])
axes[0].set_ylabel("Annual energy cost (EUR/yr)")
axes[0].set_title(f"Cost: -{cost_savings_pct:.0f}%")
for i, v in enumerate([cost_baseline_EUR_yr, cost_retrofit_EUR_yr]):
    axes[0].text(i, v + max(cost_baseline_EUR_yr, cost_retrofit_EUR_yr) * 0.02,
                 f"{v:,.0f} EUR", ha="center")

axes[1].bar(cases, [co2_baseline_t_yr, co2_retrofit_t_yr], color=["firebrick", "seagreen"])
axes[1].set_ylabel("Annual CO2 emissions (t/yr)")
axes[1].set_title(f"CO2: -{co2_savings_pct:.0f}%")
for i, v in enumerate([co2_baseline_t_yr, co2_retrofit_t_yr]):
    axes[1].text(i, v + max(co2_baseline_t_yr, co2_retrofit_t_yr) * 0.02,
                 f"{v:.0f} t", ha="center")

plt.suptitle("Baseline vs. Heat Pump Retrofit — Annual Cost and CO2")
plt.tight_layout()
plt.savefig(PNG_FILE, dpi=150)
print("\nSaved: techno_economic_baseline_vs_retrofit.csv, baseline_vs_retrofit.png")
