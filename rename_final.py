import os

screenshots_dir = "data/screenshots"
tags_file = "data/app_tags.txt"

# Count per app to number them
app_counters = {}

with open(tags_file, "r") as f:
    lines = f.readlines()

for line in lines:
    fname, app = line.strip().split(",")
    
    # increment counter per app
    app_counters[app] = app_counters.get(app, 0) + 1
    count = app_counters[app]
    
    old_path = os.path.join(screenshots_dir, fname)
    new_name = f"{app}_{count:03d}.jpeg"
    new_path = os.path.join(screenshots_dir, new_name)
    
    os.rename(old_path, new_path)
    print(f"{fname} → {new_name}")

print("\nSummary:")
for app, count in sorted(app_counters.items()):
    print(f"  {app}: {count} screenshots")
