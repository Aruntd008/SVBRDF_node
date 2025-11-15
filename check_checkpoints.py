#!/usr/bin/env python3
"""
Diagnostic script to check and download SVBRDF model checkpoints.
"""

import os
import sys

def check_checkpoints():
    """Check if model checkpoints exist and list what's in the directory."""
    current_dir = os.path.dirname(os.path.realpath(__file__))
    checkpoint_dir = os.path.join(current_dir, 'pretrained_checkpoints')
    
    print("=" * 60)
    print("SVBRDF Model Checkpoint Diagnostic")
    print("=" * 60)
    print(f"\nCheckpoint directory: {checkpoint_dir}")
    print(f"Directory exists: {os.path.exists(checkpoint_dir)}")
    
    if os.path.exists(checkpoint_dir):
        print("\nContents of checkpoint directory:")
        print("-" * 60)
        
        all_files = []
        for root, dirs, files in os.walk(checkpoint_dir):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), checkpoint_dir)
                file_size = os.path.getsize(os.path.join(root, file))
                all_files.append((rel_path, file_size))
                print(f"  {rel_path} ({file_size:,} bytes)")
        
        if not all_files:
            print("  (empty directory)")
        
        print("\n" + "-" * 60)
        print("\nRequired files:")
        required_files = [
            'checkpoint',
            'model-deepMaterials.data-00000-of-00001',
            'model-deepMaterials.index',
            'model-deepMaterials.meta',
            'options.json'
        ]
        
        missing = []
        for req_file in required_files:
            file_path = os.path.join(checkpoint_dir, req_file)
            exists = os.path.exists(file_path)
            status = "✓ FOUND" if exists else "✗ MISSING"
            print(f"  {status}: {req_file}")
            if not exists:
                missing.append(req_file)
        
        print("\n" + "=" * 60)
        if missing:
            print(f"Status: INCOMPLETE - Missing {len(missing)} file(s)")

            # Check if files have backslashes in names (Windows path issue)
            backslash_files = [f for f in all_files if '\\' in f[0]]
            if backslash_files:
                print("\n⚠️  ISSUE DETECTED: Files have backslash characters in names!")
                print("   This happens when Hugging Face repos have Windows-style paths.")
                print("\n   Files with backslashes:")
                for f, _ in backslash_files[:5]:  # Show first 5
                    print(f"     - {f}")
                if len(backslash_files) > 5:
                    print(f"     ... and {len(backslash_files) - 5} more")
                print("\nTo fix this, run:")
                print("  python fix_backslash_filenames.py")
                return False

            # Check if files are in a nested directory
            nested_dir = os.path.join(checkpoint_dir, 'pretrained_checkpoints')
            if os.path.exists(nested_dir) and os.path.isdir(nested_dir):
                print("\n⚠️  ISSUE DETECTED: Files are in a nested directory!")
                print(f"   Files are in: {nested_dir}")
                print(f"   Should be in: {checkpoint_dir}")
                print("\nTo fix this, run:")
                print("  python fix_checkpoint_location.py")
                return False

            print("\nTo download the model checkpoints, run:")
            print("  python download_checkpoints.py")
            return False
        else:
            print("Status: COMPLETE - All required files present")
            return True
    else:
        print("\nStatus: NOT FOUND - Checkpoint directory doesn't exist")
        print("\nTo download the model checkpoints, run:")
        print("  python download_checkpoints.py")
        return False

if __name__ == "__main__":
    success = check_checkpoints()
    sys.exit(0 if success else 1)

