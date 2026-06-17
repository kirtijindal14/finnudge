import os
import subprocess
import csv

screenshots_dir = "data/screenshots"
output_file = "data/labelled.csv"

files = sorted([f for f in os.listdir(screenshots_dir) if f.endswith(".jpeg")])

pattern_map = {
    "0": "CLEAN", "1": "FOMO", "2": "LOSS", "3": "ANCHOR",
    "4": "SCARCITY", "5": "GAMIFY", "6": "DEFAULT"
}
bias_map = {
    "FOMO": "social_proof", "LOSS": "loss_aversion", "ANCHOR": "anchoring",
    "SCARCITY": "scarcity", "GAMIFY": "variable_reward",
    "DEFAULT": "default_bias", "CLEAN": "none"
}
screen_map = {
    "h": "home", "f": "fund", "o": "onboarding", "p": "portfolio",
    "n": "notification", "s": "stock", "e": "explore"
}

# Check how many already labelled
already_done = set()
if os.path.exists(output_file):
    with open(output_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            already_done.add(row["filename"])

print(f"=== FinNudge Labelling Tool ===")
print(f"Already labelled: {len(already_done)}/81")
print("\nPATTERN: 0=CLEAN | 1=FOMO | 2=LOSS | 3=ANCHOR | 4=SCARCITY | 5=GAMIFY | 6=DEFAULT")
print("SCREEN:  h=home | f=fund | o=onboarding | p=portfolio | n=notification | s=stock | e=explore")
print("SEVERITY: 1=subtle | 2=moderate | 3=aggressive")
print("Type 'skip' to skip\n")

# Open CSV in append mode
with open(output_file, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "filename", "app", "screen_type", "pattern_label",
        "bias_exploited", "severity", "notes"
    ])
    
    # Write header only if file is empty
    if len(already_done) == 0:
        writer.writeheader()

    for i, fname in enumerate(files):
        # Skip already labelled
        if fname in already_done:
            print(f"[{i+1}/81] {fname} — already done, skipping")
            continue

        path = os.path.join(screenshots_dir, fname)
        app = fname.split("_")[0]
        subprocess.Popen(["open", "-a", "Preview", path])

        print(f"\n[{i+1}/81] {fname} (app: {app})")

        while True:
            pattern_key = input("  Pattern (0-6): ").strip()
            if pattern_key == "skip":
                break
            if pattern_key in pattern_map:
                pattern = pattern_map[pattern_key]
                break
            print("  ⚠ Type a single number 0-6")

        if pattern_key == "skip":
            print("  Skipped")
            continue

        while True:
            screen_key = input("  Screen (h/f/o/p/n/s/e): ").strip()
            if screen_key in screen_map:
                screen = screen_map[screen_key]
                break
            print("  ⚠ Type one letter")

        if pattern != "CLEAN":
            while True:
                severity = input("  Severity (1/2/3): ").strip()
                if severity in ["1", "2", "3"]:
                    break
                print("  ⚠ Type 1, 2 or 3")
            notes = input("  Notes: ").strip()
        else:
            severity = "0"
            notes = "clean UI"

        row = {
            "filename": fname, "app": app, "screen_type": screen,
            "pattern_label": pattern, "bias_exploited": bias_map[pattern],
            "severity": severity, "notes": notes
        }
        writer.writerow(row)
        f.flush()  # saves immediately to disk

        print(f"  ✓ Saved: {pattern} | {screen} | severity {severity}")

print(f"\nDone! Check data/labelled.csv")
