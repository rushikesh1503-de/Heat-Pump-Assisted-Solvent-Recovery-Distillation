"""
Techno-Economic Analysis (Part 3): Sensitivity Analysis
Heat-Pump-Assisted Solvent Recovery Distillation Project

Tests how sensitive the payback period is to the key uncertain inputs:
  - electricity price
  - gas price
  - CAPEX (specific investment cost)

Each variable is swept individually, holding the others at the base case,
to build a tornado-style sensitivity chart. This shows which assumption
the result actually depends on most, rather than just presenting one
number as if it were certain.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Folder where this Python script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Output files
CSV_FILE = os.path.join(SCRIPT_DIR, "sensitivity_results.csv")
PNG_FILE = os.path.join(SCRIPT_DIR, "Sensitivity tornado.png")


# ---------------------------------------------------------------------
# 1. Base case inputs (from prior stages)
# ---------------------------------------------------------------------
Q_reboiler_kW = 268.98
Q_HP_kW = 204.42
Q_aux_kW = Q_reboiler_kW - Q_HP_kW
W_comp_kW = 28.97

operating_hours = 8000
boiler_efficiency = 0.88

base_price_gas = 0.070       # EUR/kWh
base_price_elec = 0.172      # EUR/kWh

base_capex_EUR = 255525      # base case from capex_payback.py

# ---------------------------------------------------------------------
# 2. Function: compute annual savings and payback for given inputs
# ---------------------------------------------------------------------
def compute_payback(price_gas, price_elec, capex):
    gas_input_kW_baseline = Q_reboiler_kW / boiler_efficiency
    gas_MWh_yr_baseline = gas_input_kW_baseline * operating_hours / 1000
    cost_baseline = gas_MWh_yr_baseline * 1000 * price_gas

    elec_MWh_yr = W_comp_kW * operating_hours / 1000
    gas_input_kW_aux = Q_aux_kW / boiler_efficiency
    gas_MWh_yr_retrofit = gas_input_kW_aux * operating_hours / 1000
    cost_retrofit = elec_MWh_yr * 1000 * price_elec + gas_MWh_yr_retrofit * 1000 * price_gas

    savings = cost_baseline - cost_retrofit
    payback = capex / savings
    return savings, payback

base_savings, base_payback = compute_payback(base_price_gas, base_price_elec, base_capex_EUR)
print(f"Base case: savings = {base_savings:,.0f} EUR/yr, payback = {base_payback:.2f} years\n")

# ---------------------------------------------------------------------
# 3. Sweep each variable individually, +/- 20% (CAPEX +/- 30%, wider
#    uncertainty since it is the least certain input, per literature spread)
# ---------------------------------------------------------------------
variables = {
    "Electricity price": {"base": base_price_elec, "range_pct": 0.20,
                           "setter": lambda v: compute_payback(base_price_gas, v, base_capex_EUR)},
    "Gas price":          {"base": base_price_gas,  "range_pct": 0.20,
                           "setter": lambda v: compute_payback(v, base_price_elec, base_capex_EUR)},
    "CAPEX":              {"base": base_capex_EUR,  "range_pct": 0.30,
                           "setter": lambda v: compute_payback(base_price_gas, base_price_elec, v)},
}

rows = []
for name, spec in variables.items():
    low_val = spec["base"] * (1 - spec["range_pct"])
    high_val = spec["base"] * (1 + spec["range_pct"])
    _, payback_low = spec["setter"](low_val)
    _, payback_high = spec["setter"](high_val)
    rows.append({
        "Variable": name,
        "Low input": low_val,
        "High input": high_val,
        "Payback at low input (yr)": payback_low,
        "Payback at high input (yr)": payback_high,
        "Payback swing (yr)": abs(payback_high - payback_low),
    })

sens_df = pd.DataFrame(rows).sort_values("Payback swing (yr)", ascending=True)
print(sens_df.to_string(index=False))
sens_df.to_csv(CSV_FILE, index=False)

# ---------------------------------------------------------------------
# 4. Tornado chart
# ---------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.5))

y_pos = range(len(sens_df))
for i, row in enumerate(sens_df.itertuples()):
    left = min(row._4, row._5)   # payback at low / high input
    width = abs(row._5 - row._4)
    ax.barh(i, width, left=left, color="steelblue", height=0.5)
    ax.text(row._4, i, f"{row._4:.1f}", va="center", ha="right", fontsize=9)
    ax.text(row._5, i, f"{row._5:.1f}", va="center", ha="left", fontsize=9)

ax.axvline(base_payback, color="black", ls="--", lw=1.2, label=f"Base case: {base_payback:.1f} yr")
ax.set_yticks(list(y_pos))
ax.set_yticklabels(sens_df["Variable"])
ax.set_xlabel("Payback period (years)")
ax.set_title("Sensitivity of Payback Period to Key Assumptions\n(each variable swept individually, others held at base case)")
ax.legend(loc="lower right", fontsize=8)
ax.grid(axis="x", alpha=0.3)
x_min = sens_df[["Payback at low input (yr)", "Payback at high input (yr)"]].min().min()
x_max = sens_df[["Payback at low input (yr)", "Payback at high input (yr)"]].max().max()
ax.set_xlim(x_min - 0.6, x_max + 0.4)

plt.tight_layout()
plt.savefig(PNG_FILE, dpi=150)
print("\nSaved: " + CSV_FILE + ", " + PNG_FILE)
