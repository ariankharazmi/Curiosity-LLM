import json, math, pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent

def load_json(name):
    with open(BASE / name) as f:
        return json.load(f)

# Look for LM-Eval terms like acc_norm
def get_metric(d, metric):
    return d.get(f"{metric},none") or d.get(metric)

def ci95(mean, se):
    half = 1.96 * se
    return mean - half, mean + half

c16 = load_json("HellaSwag_C16.json")
gpt2 = load_json("HellaSwag_GPT-2M.json")

c_block = c16.get("results", {}).get("hellaswag")
g_block = gpt2.get("results", {}).get("hellaswag")

if c_block is None:
    c_block = list(c16.get("results", {}).values())[0]
if g_block is None:
    g_block = list(gpt2.get("results", {}).values())[0]

metrics = ["acc", "acc_norm"]
rows = []
for m in metrics:
    # Accuracy metrics (Raw & Normalized, per model)
    c_acc = get_metric(c_block, m)
    g_acc = get_metric(g_block, m)

    # Standard Error
    c_se = get_metric(c_block, m + "_stderr")
    g_se = get_metric(g_block, m + "_stderr")

    # Per-model Confidence Intervals
    c_low, c_high = ci95(c_acc, c_se)
    g_low, g_high = ci95(g_acc, g_se)

    # Deltas and Delta CI's
    delta = c_acc - g_acc
    delta_se = math.sqrt(c_se**2 + g_se**2)
    d_low, d_high = ci95(delta, delta_se)
    rows.append({
        "metric": m,
        "gpt2M_acc": g_acc,
        "gpt2M_ci_low": g_low,
        "gpt2M_ci_high": g_high,
        "c16_acc": c_acc,
        "c16_ci_low": c_low,
        "c16_ci_high": c_high,
        "delta": delta,
        "delta_ci_low": d_low,
        "delta_ci_high": d_high
    })

df = pd.DataFrame(rows)
out = BASE / "HellaSwag_Full_CIs.csv"
df.to_csv(out, index=False)

print("Retrieved", out)
print(df.to_string(index=False))
