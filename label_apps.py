import os
import subprocess

screenshots_dir = "data/screenshots"
files = sorted([f for f in os.listdir(screenshots_dir) if f.endswith(".jpeg")])

app_map = {
    "g": "groww",
    "z": "zerodha", 
    "u": "upstox",
    "i": "indmoney",
    "a": "angelone"
}

print("Keys: g=Groww | z=Zerodha | u=Upstox | i=INDmoney | a=AngelOne | s=skip")
print(f"Total: {len(files)} screenshots\n")

results = []
for i, fname in enumerate(files):
    path = os.path.join(screenshots_dir, fname)
    
    # Opens image in Mac preview
    subprocess.Popen(["open", path])
    
    key = input(f"[{i+1}/{len(files)}] {fname} → app? ").strip().lower()
    
    if key == "s":
        continue
    
    app = app_map.get(key, None)
    if app:
        results.append((fname, app))
        print(f"  ✓ Tagged as {app}")
    else:
        print("  ✗ Invalid key, skipping")

# Save results
with open("data/app_tags.txt", "w") as f:
    for fname, app in results:
        f.write(f"{fname},{app}\n")

print(f"\nDone! Tagged {len(results)} screenshots. Saved to data/app_tags.txt")
