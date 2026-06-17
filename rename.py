import os

folder = "data/screenshots"
files = sorted([f for f in os.listdir(folder) if f.endswith(".jpeg")])

for i, old_name in enumerate(files):
    new_name = f"screenshot_{i+1:03d}.jpeg"
    os.rename(
        os.path.join(folder, old_name),
        os.path.join(folder, new_name)
    )
    print(f"{old_name} → {new_name}")

print(f"\nDone! Renamed {len(files)} files.")
