import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from rocketcea.cea_obj import CEA_Obj

# Define constant engine conditions
PC_PSI = 1000.0  # Chamber Pressure (psi)
EPSILON = 40.0  # Nozzle Area Expansion Ratio (Ae/At)

# Define propellant pairs: (Oxidizer, Fuel, MR_range, Label)
propellants = [
    ("LOX", "RP1", np.linspace(1.5, 3.5, 25), "LOX / RP-1 (Kerosene)"),
    ("LOX", "CH4", np.linspace(2.0, 4.5, 25), "LOX / Methane (CH4)"),
    ("LOX", "LH2", np.linspace(3.0, 8.0, 25), "LOX / Liquid Hydrogen (LH2)"),
]

# Run CEA calculations and store results
results = {}

for ox, fuel, mr_range, label in propellants:
    cea = CEA_Obj(oxName=ox, fuelName=fuel)
    isp_values = []

    for mr in mr_range:
        # Calculate vacuum specific impulse (Isp) in seconds
        isp = cea.get_Isp(Pc=PC_PSI, MR=mr, eps=EPSILON)
        isp_values.append(isp)

    results[label] = {
        "mr": mr_range,
        "isp": isp_values,
        "max_isp": max(isp_values),
        "optimal_mr": mr_range[np.argmax(isp_values)],
    }

# Plotting Isp vs. Mixture Ratio
plt.figure(figsize=(10, 6))

colors = ["tab:blue", "tab:orange", "tab:green"]
for i, (label, data) in enumerate(results.items()):
    plt.plot(
        data["mr"],
        data["isp"],
        label=f"{label} (Peak $I_{{sp}}$ = {data['max_isp']:.1f}s at MR = {data['optimal_mr']:.2f})",
        color=colors[i],
        linewidth=2.5,
    )

plt.xlabel("Mixture Ratio (Oxidizer/Fuel Mass Ratio)", fontweight="bold")
plt.ylabel("Vacuum Specific Impulse $I_{sp}$ (seconds)", fontweight="bold")
plt.title(
    r"NASA CEA Trade Study: Propellant Performance vs. Mixture Ratio ($P_c = 1000$ psi, $\epsilon = 40$)",
    pad=15,
)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(fontsize=10)
plt.tight_layout()

plt.savefig("nasa_cea_propellant_trade_study.png", dpi=300)
plt.show()

# Print summary table
summary_data = []
for label, data in results.items():
    summary_data.append(
        {
            "Propellant Pair": label,
            "Peak Isp (s)": round(data["max_isp"], 1),
            "Optimal O/F Ratio": round(data["optimal_mr"], 2),
        }
    )

df_summary = pd.DataFrame(summary_data)
print("\n--- PERFORMANCE SUMMARY ---")
print(df_summary.to_string(index=False))
