import re
import pandas as pd
from typing import List, Tuple


def normalize(text: str, case_sensitive: bool = False, keep_punctuation: bool = False) -> List[str]:
    if not case_sensitive:
        text = text.lower()
    if not keep_punctuation:
        text = re.sub(r"[^\w\s]", "", text)
    return text.strip().split()


def load_lines(path: str, case_sensitive: bool = False, keep_punctuation: bool = False) -> List[List[str]]:
    with open(path, "r", encoding="utf-8") as f:
        return [normalize(line, case_sensitive, keep_punctuation) for line in f]


def compute_wer(ref: List[str], hyp: List[str]) -> Tuple[float, int, int, int, List[str]]:
    r, h = len(ref), len(hyp)
    dp = [[0] * (h + 1) for _ in range(r + 1)]

    for i in range(r + 1):
        dp[i][0] = i
    for j in range(h + 1):
        dp[0][j] = j

    for i in range(1, r + 1):
        for j in range(1, h + 1):
            if ref[i - 1] == hyp[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j - 1] + 1,  # substitution
                    dp[i][j - 1] + 1,      # insertion
                    dp[i - 1][j] + 1       # deletion
                )

    i, j = r, h
    subs = ins = dels = 0
    align = []

    while i > 0 and j > 0:
        if ref[i - 1] == hyp[j - 1]:
            align.append(f"  {ref[i - 1]}")
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j - 1] + 1:
            subs += 1
            align.append(f"S {ref[i - 1]}->{hyp[j - 1]}")
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i][j - 1] + 1:
            ins += 1
            align.append(f"I {hyp[j - 1]}")
            j -= 1
        else:
            dels += 1
            align.append(f"D {ref[i - 1]}")
            i -= 1

    while j > 0:
        ins += 1
        align.append(f"I {hyp[j - 1]}")
        j -= 1
    while i > 0:
        dels += 1
        align.append(f"D {ref[i - 1]}")
        i -= 1

    wer_score = 100 * (subs + ins + dels) / max(len(ref), 1)
    return wer_score, ins, dels, subs, align[::-1]


def compute_wer_batch(
    refs: List[List[str]],
    hyps: List[List[str]],
    verbose: bool = False
) -> dict:
    total_words = total_ins = total_dels = total_subs = total_wer = 0
    per_line_data = []

    for i, (ref_line, hyp_line) in enumerate(zip(refs, hyps)):
        wer_score, ins, dels, subs, align = compute_wer(ref_line, hyp_line)
        total_words += len(ref_line)
        total_ins += ins
        total_dels += dels
        total_subs += subs
        total_wer += wer_score * len(ref_line)
        per_line_data.append({
            "Line": i + 1,
            "WER": wer_score,
            "Insertions": ins,
            "Deletions": dels,
            "Substitutions": subs,
            "Alignment": " ".join(align)
        })

        if verbose:
            print(f"\n[Line {i + 1}] WER: {wer_score:.2f}%")
            print("Alignment:", " ".join(align))

    overall_wer = total_wer / total_words if total_words > 0 else 0

    return {
        "overall_wer": overall_wer,
        "total_ins": total_ins,
        "total_dels": total_dels,
        "total_subs": total_subs,
        "df": pd.DataFrame(per_line_data)
    }


# def plot_errors(ins: int, dels: int, subs: int):
#     import matplotlib.pyplot as plt

#     labels = ["Insertions", "Deletions", "Substitutions"]
#     values = [ins, dels, subs]

#     plt.bar(labels, values)
#     plt.title("WER Error Breakdown")
#     plt.ylabel("Count")
#     plt.tight_layout()
#     plt.show()

# saving file instead
def plot_errors(ins: int, dels: int, subs: int, save_path: str = None):
    import matplotlib.pyplot as plt

    labels = ["Insertions", "Deletions", "Substitutions"]
    values = [ins, dels, subs]

    plt.figure()
    plt.bar(labels, values)
    plt.title("WER Error Breakdown")
    plt.ylabel("Count")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"[✓] Saved plot to {save_path}")
    else:
        plt.show()
