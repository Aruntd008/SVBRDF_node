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

