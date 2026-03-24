import os

# Updated path based on the new folder structure
base_path = 'dataset/images'
categories = ['safe', 'phishing']

for cat in categories:
    path = os.path.join(base_path, cat)
    if not os.path.exists(path):
        print(f"Error: {path} not found! Did you put the folders inside dataset/images/?")
        continue
        
    files = [f for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    print(f"Found {len(files)} valid images in {cat}.")
    
    for i, filename in enumerate(files):
        ext = os.path.splitext(filename)[1].lower()
        old_file = os.path.join(path, filename)
        new_file = os.path.join(path, f"cleaned_{cat}_{i}{ext}")
        try:
            os.rename(old_file, new_file)
        except FileExistsError:
            continue

print("Dataset fixed. Run train_vision.py next.")