#!/usr/bin/env python3
"""
Download SVBRDF model checkpoints from Hugging Face.
This script can be run standalone or will be called automatically by ComfyUI.
"""

import os
import sys
import subprocess

def find_conda_executable():
    """Find the conda executable."""
    import shutil
    
    # First try to find conda in PATH
    conda_exe = shutil.which('conda')
    if conda_exe:
        return conda_exe
    
    # Common conda installation paths
    possible_paths = [
        os.path.expanduser("~/miniconda3/bin/conda"),
        os.path.expanduser("~/anaconda3/bin/conda"),
        "/opt/conda/bin/conda",
        "/usr/local/miniconda3/bin/conda",
        "/usr/local/anaconda3/bin/conda",
    ]
    
    for path in possible_paths:
        if os.path.isfile(path):
            return path
    
    return None

def download_with_cli():
    """Download using huggingface-cli."""
    print("Attempting download with huggingface-cli...")
    
    conda_exe = find_conda_executable()
    if not conda_exe:
        print("ERROR: Conda not found. Please install conda first.")
        return False
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    checkpoint_dir = os.path.join(current_dir, 'pretrained_checkpoints')
    os.makedirs(checkpoint_dir, exist_ok=True)
    
    cmd = [
        conda_exe, 'run', '-n', 'svbrdf',
        'huggingface-cli', 'download',
        'aruntd008/svbrdf-model',
        '--local-dir', checkpoint_dir,
        '--repo-type', 'model'
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    return result.returncode == 0

def download_with_python():
    """Download using Python huggingface_hub API."""
    print("Attempting download with Python API...")
    
    conda_exe = find_conda_executable()
    if not conda_exe:
        print("ERROR: Conda not found. Please install conda first.")
        return False
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    checkpoint_dir = os.path.join(current_dir, 'pretrained_checkpoints')
    os.makedirs(checkpoint_dir, exist_ok=True)
    
    python_code = f'''
from huggingface_hub import snapshot_download
import os

checkpoint_dir = r"{checkpoint_dir}"
print(f"Downloading to: {{checkpoint_dir}}")

snapshot_download(
    repo_id="aruntd008/svbrdf-model",
    repo_type="model",
    local_dir=checkpoint_dir,
    local_dir_use_symlinks=False
)
print("Download completed!")
'''
    
    cmd = [conda_exe, 'run', '-n', 'svbrdf', 'python', '-c', python_code]
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    return result.returncode == 0

def main():
    print("=" * 60)
    print("SVBRDF Model Checkpoint Downloader")
    print("=" * 60)
    print()
    
    # Try CLI first
    if download_with_cli():
        print("\n✓ Download successful!")
        return 0
    
    print("\nCLI download failed, trying Python API...")
    
    # Try Python API
    if download_with_python():
        print("\n✓ Download successful!")
        return 0
    
    print("\n✗ Download failed!")
    print("\nPlease try manual download:")
    print("1. Visit: https://huggingface.co/aruntd008/svbrdf-model")
    print("2. Download all files to: pretrained_checkpoints/")
    return 1

if __name__ == "__main__":
    sys.exit(main())

