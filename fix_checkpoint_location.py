#!/usr/bin/env python3
"""
Fix checkpoint file locations if they were downloaded to a nested directory.
This is a common issue with Hugging Face downloads.
"""

import os
import shutil

def fix_checkpoint_location():
    """Move checkpoint files from nested directory to correct location."""
    current_dir = os.path.dirname(os.path.realpath(__file__))
    checkpoint_dir = os.path.join(current_dir, 'pretrained_checkpoints')
    
    print("=" * 60)
    print("SVBRDF Checkpoint Location Fix")
    print("=" * 60)
    print(f"\nCheckpoint directory: {checkpoint_dir}")
    
    if not os.path.exists(checkpoint_dir):
        print("ERROR: Checkpoint directory doesn't exist!")
        return False
    
    # Check if files are already in the correct location
    if os.path.exists(os.path.join(checkpoint_dir, 'options.json')):
        print("✓ Files are already in the correct location!")
        return True
    
    # Check for nested directory
    nested_dir = os.path.join(checkpoint_dir, 'pretrained_checkpoints')
    if os.path.exists(nested_dir) and os.path.isdir(nested_dir):
        print(f"\n✓ Found nested directory: {nested_dir}")
        print("\nMoving files to correct location...")
        print("-" * 60)
        
        moved_count = 0
        for item in os.listdir(nested_dir):
            src = os.path.join(nested_dir, item)
            dst = os.path.join(checkpoint_dir, item)
            
            if os.path.isfile(src):
                # Don't overwrite existing files
                if os.path.exists(dst):
                    print(f"  SKIP (exists): {item}")
                else:
                    shutil.move(src, dst)
                    print(f"  MOVED: {item}")
                    moved_count += 1
            elif os.path.isdir(src):
                # Move directories recursively
                if os.path.exists(dst):
                    print(f"  SKIP (exists): {item}/")
                else:
                    shutil.move(src, dst)
                    print(f"  MOVED: {item}/")
                    moved_count += 1
        
        print("-" * 60)
        print(f"\nMoved {moved_count} items")
        
        # Remove the nested directory if it's empty
        try:
            if not os.listdir(nested_dir):
                os.rmdir(nested_dir)
                print("Removed empty nested directory")
        except:
            pass
        
        # Verify the fix worked
        if os.path.exists(os.path.join(checkpoint_dir, 'options.json')):
            print("\n✓ SUCCESS! Files are now in the correct location!")
            return True
        else:
            print("\n✗ WARNING: options.json still not found after moving files")
            return False
    else:
        print("\n✗ No nested directory found")
        print("\nCurrent directory contents:")
        for item in os.listdir(checkpoint_dir):
            item_path = os.path.join(checkpoint_dir, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                print(f"  FILE: {item} ({size:,} bytes)")
            else:
                print(f"  DIR:  {item}/")
        
        print("\nThe files may need to be re-downloaded.")
        print("Run: python download_checkpoints.py")
        return False

if __name__ == "__main__":
    import sys
    success = fix_checkpoint_location()
    sys.exit(0 if success else 1)

