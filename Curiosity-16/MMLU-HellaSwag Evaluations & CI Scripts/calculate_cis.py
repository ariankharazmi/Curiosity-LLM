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

# Load your JSONs
c16 = load_json("MMLU-C16-Results.json")
gpt2  = load_json("MMLU-GPT2Medium-Results.json")

rows = []
for k in sorted(set(c16["results"]) & set(gpt2["results"])):
    c = c16["results"][k]
    g = gpt2["results"][k]

# Get Standard Errors and Normalized Accuracies
    acc_c = get_metric(c, "acc_norm") or get_metric(c, "acc")
    se_c  = get_metric(c, "acc_norm_stderr") or get_metric(c, "acc_stderr")
    acc_g = get_metric(g, "acc_norm") or get_metric(g, "acc")
    se_g  = get_metric(g, "acc_norm_stderr") or get_metric(g, "acc_stderr")
# Per model Confidence Intervals
    c_low, c_high = ci95(acc_c, se_c)
    g_low, g_high = ci95(acc_g, se_g)
# Deltas and Delta CI's
    delta = acc_c - acc_g
    se_delta = math.sqrt(se_c**2 + se_g**2)
    d_low, d_high = ci95(delta, se_delta)
    rows.append({
        "subject": k,
        "gpt2M_acc": acc_g,
        "gpt2M_se": se_g,
        "gpt2M_ci_low": g_low,
        "gpt2M_ci_high": g_high,
        "c16_acc": acc_c,
        "c16_se": se_c,
        "c16_ci_low": c_low,
        "c16_ci_high": c_high,
        "delta": delta,
        "delta_se": se_delta,
        "delta_ci_low": d_low,
        "delta_ci_high": d_high,
    })

out_path = BASE / "MMLU_CIs_and_Deltas.csv"
pd.DataFrame(rows).to_csv(out_path, index=False)
print("Retrieved:", out_path)
