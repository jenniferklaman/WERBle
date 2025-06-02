import argparse
import json
from werble.scorer import load_lines, compute_wer_batch, plot_errors

def main():
    parser = argparse.ArgumentParser(description="Calculate WER from reference and hypothesis files.")
    parser.add_argument("--ref", required=True, help="Reference transcript file")
    parser.add_argument("--hyp", required=True, help="Hypothesis transcript file")
    parser.add_argument("--case-sensitive", action="store_true", help="Preserve case (default is lowercase)")
    parser.add_argument("--keep-punctuation", action="store_true", help="Keep punctuation (default strips it)")
    parser.add_argument("--csv", action="store_true", help="Export WER results to CSV")
    parser.add_argument("--verbose", action="store_true", help="Print per-line WER and alignments")
    parser.add_argument("--plot", action="store_true", help="Show error type bar plot")
    parser.add_argument("--json", action="store_true", help="Export WER results to werble_output.json")
    parser.add_argument("--plot-out", type=str, help="Save the plot to a file instead of displaying it")


    args = parser.parse_args()

    refs = load_lines(args.ref, args.case_sensitive, args.keep_punctuation)
    hyps = load_lines(args.hyp, args.case_sensitive, args.keep_punctuation)

    if len(refs) != len(hyps):
        print(f"[ERROR] Line count mismatch: {len(refs)} refs vs {len(hyps)} hyps")
        return

    result = compute_wer_batch(refs, hyps, verbose=args.verbose)

    print(f"\n===================")
    print(f"Overall WER: {result['overall_wer']:.2f}%")
    print(f"Insertions: {result['total_ins']}  Deletions: {result['total_dels']}  Substitutions: {result['total_subs']}")

    if args.csv:
        result["df"].to_csv("werble_output.csv", index=False)
        print("[✓] Saved results to werble_output.csv")

    if args.json:
        json_data = {
            "overall_wer": round(result["overall_wer"], 2),
            "insertions": result["total_ins"],
            "deletions": result["total_dels"],
            "substitutions": result["total_subs"],
            "lines": result["df"].to_dict(orient="records"),
        }
        with open("werble_output.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)
        print("[✓] Saved results to werble_output.json")

    if args.plot:
        plot_errors(
            result["total_ins"],
            result["total_dels"],
            result["total_subs"],
            save_path=args.plot_out
        )

if __name__ == "__main__":
    print("CLI script running...")
    main()
