#!/usr/bin/env python3
"""
Fix checkpoint files that were downloaded with backslash characters in filenames.
This happens when Hugging Face repos have Windows-style paths in their structure.
"""

import os
import shutil

def fix_backslash_filenames():
    """Extract files from backslash-named files to proper locations."""
    current_dir = os.path.dirname(os.path.realpath(__file__))
    checkpoint_dir = os.path.join(current_dir, 'pretrained_checkpoints')
    
    print("=" * 60)
    print("SVBRDF Checkpoint Backslash Filename Fix")
    print("=" * 60)
    print(f"\nCheckpoint directory: {checkpoint_dir}")
    
    if not os.path.exists(checkpoint_dir):
        print("ERROR: Checkpoint directory doesn't exist!")
        return False
    
    # Check if files are already in the correct location
    if os.path.exists(os.path.join(checkpoint_dir, 'options.json')):
        print("✓ Files are already in the correct location!")
        return True
    
    print("\nScanning for files with backslashes in names...")
    print("-" * 60)
    
    fixed_count = 0
    for item in os.listdir(checkpoint_dir):
        item_path = os.path.join(checkpoint_dir, item)
        
        # Check if this is a file with backslashes in the name
        if os.path.isfile(item_path) and '\\' in item:
            # Extract the actual filename (part after the last backslash)
            actual_filename = item.split('\\')[-1]
            target_path = os.path.join(checkpoint_dir, actual_filename)
            
            print(f"Found: {item}")
            print(f"  -> Extracting to: {actual_filename}")
            
            # Copy the file to the correct location
            if os.path.exists(target_path):
                print(f"  -> SKIP (already exists)")
            else:
                shutil.copy2(item_path, target_path)
                print(f"  -> COPIED")
                fixed_count += 1
    
    print("-" * 60)
    print(f"\nExtracted {fixed_count} files")
    
    # Verify the fix worked
    required_files = [
        'checkpoint',
        'model-deepMaterials.data-00000-of-00001',
        'model-deepMaterials.index',
        'model-deepMaterials.meta',
        'options.json'
    ]
    
    print("\nVerifying required files:")
    all_present = True
    for req_file in required_files:
        file_path = os.path.join(checkpoint_dir, req_file)
        exists = os.path.exists(file_path)
        status = "✓" if exists else "✗"
        print(f"  {status} {req_file}")
        if not exists:
            all_present = False
    
    if all_present:
        print("\n✓ SUCCESS! All required files are now in the correct location!")
        
        # Optionally clean up the backslash-named files
        print("\nCleaning up backslash-named files...")
        for item in os.listdir(checkpoint_dir):
            item_path = os.path.join(checkpoint_dir, item)
            if os.path.isfile(item_path) and '\\' in item:
                os.remove(item_path)
                print(f"  Removed: {item}")
        
        return True
    else:
        print("\n✗ WARNING: Some required files are still missing")
        print("\nYou may need to re-download the checkpoints.")
        print("Run: python download_checkpoints.py")
        return False

if __name__ == "__main__":
    import sys
    success = fix_backslash_filenames()
    sys.exit(0 if success else 1)

