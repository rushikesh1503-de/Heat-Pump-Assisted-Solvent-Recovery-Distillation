"""
Techno-Economic Analysis (Part 2): CAPEX and Payback
Heat-Pump-Assisted Solvent Recovery Distillation Project

CAPEX for industrial high-temperature heat pumps is genuinely uncertain
without vendor quotes -- published literature reports specific investment
costs (bare equipment) in the range of roughly 300-900 EUR/kW_thermal for
heat delivery up to ~160 degC, with total INSTALLED cost (labour, piping,
controls, engineering) reported as "several times" the bare equipment cost.

Sources (see project report for full citations):
  - Blue Terra (2008), cited via energy.nl industrial HTHP review:
    100-250 EUR/kWth (bare, up to 85 degC) and 300-900 EUR/kWth
    (bare, up to 160 degC)
  - IEA HPT Annex 58 / ScienceDirect review: 200-1500 EUR/kW across all
    HTHP technologies, with >100 K lift costing at least 600 EUR/kW
    (our lift is 34 K, well below that threshold, so the low-to-mid range
    is the more relevant comparison)

Because of this spread, results are reported as a range (low / base / high),
not a single number.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Folder where this Python script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Output files
CSV_FILE = os.path.join(SCRIPT_DIR, "Capex payback.csv")
PNG_FILE = os.path.join(SCRIPT_DIR, "Capex payback.png")

# ---------------------------------------------------------------------
# 1. Inputs (from prior stages -- not assumptions)
# ---------------------------------------------------------------------
Q_HP_kW = 204.42                    # heat pump condenser duty (useful heat output)
annual_savings_EUR = 90223          # from techno_economic.py (OPEX savings)

# ---------------------------------------------------------------------
# 2. CAPEX assumptions -- explicit range 
# ---------------------------------------------------------------------
cases = {
    "Low":  {"specific_cost_EUR_kWth": 300, "install_factor": 2.0},
    "Base": {"specific_cost_EUR_kWth": 500, "install_factor": 2.5},
    "High": {"specific_cost_EUR_kWth": 900, "install_factor": 3.0},
}

# ---------------------------------------------------------------------
# 3. Calculate CAPEX and simple payback for each case
# ---------------------------------------------------------------------
rows = []
for label, params in cases.items():
    bare_equipment_EUR = Q_HP_kW * params["specific_cost_EUR_kWth"]
    total_installed_EUR = bare_equipment_EUR * params["install_factor"]
    payback_years = total_installed_EUR / annual_savings_EUR
    rows.append({
        "Case": label,
        "Specific cost (EUR/kWth)": params["specific_cost_EUR_kWth"],
        "Installation factor": params["install_factor"],
        "Bare equipment CAPEX (EUR)": bare_equipment_EUR,
        "Total installed CAPEX (EUR)": total_installed_EUR,
        "Simple payback (years)": payback_years,
    })

capex_df = pd.DataFrame(rows)
print(capex_df.to_string(index=False))
capex_df.to_csv(CSV_FILE, index=False)

# ---------------------------------------------------------------------
# 4. NPV over the heat pump's typical service life (bonus metric)
# ---------------------------------------------------------------------
discount_rate = 0.08     # typical industrial hurdle rate, Germany
project_life_years = 15  # typical industrial heat pump service life

def npv(capex, annual_savings, rate, years):
    return -capex + sum(annual_savings / (1 + rate) ** t for t in range(1, years + 1))

capex_df["NPV @ 8%, 15 yr (EUR)"] = capex_df["Total installed CAPEX (EUR)"].apply(
    lambda c: npv(c, annual_savings_EUR, discount_rate, project_life_years)
)
print("\nWith NPV:")
print(capex_df[["Case", "Total installed CAPEX (EUR)", "Simple payback (years)",
                 "NPV @ 8%, 15 yr (EUR)"]].to_string(index=False))
capex_df.to_csv(CSV_FILE, index=False)

# ---------------------------------------------------------------------
# 5. Chart: CAPEX range and payback range
# ---------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11, 5))

colors = ["seagreen", "steelblue", "firebrick"]
axes[0].bar(capex_df["Case"], capex_df["Total installed CAPEX (EUR)"], color=colors)
axes[0].set_ylabel("Total installed CAPEX (EUR)")
axes[0].set_title("CAPEX range")
for i, v in enumerate(capex_df["Total installed CAPEX (EUR)"]):
    axes[0].text(i, v + 8000, f"{v:,.0f} EUR", ha="center")

axes[1].bar(capex_df["Case"], capex_df["Simple payback (years)"], color=colors)
axes[1].set_ylabel("Simple payback (years)")
axes[1].set_title("Payback range")
axes[1].axhline(5, color="black", ls="--", lw=1, label="Typical 5-yr industrial hurdle")
axes[1].legend(fontsize=8)
for i, v in enumerate(capex_df["Simple payback (years)"]):
    axes[1].text(i, v + 0.1, f"{v:.1f} yr", ha="center")

plt.suptitle("Heat Pump Retrofit \u2014 CAPEX and Payback (Low / Base / High literature-cost cases)")
plt.tight_layout()
plt.savefig(PNG_FILE, dpi=150)
print("\nSaved: " + CSV_FILE + ", " + PNG_FILE)
