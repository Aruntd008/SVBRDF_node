"""
SVBRDF Node for ComfyUI
========================

This package provides a ComfyUI node for Single-Image SVBRDF (Spatially Varying Bidirectional Reflectance Distribution Function) capture.
The node takes an input image and generates material maps including normals, diffuse, roughness, and specular components.

Author: Based on the DeepMaterials implementation
"""

import os
import subprocess
import sys
import importlib.util
import platform
import urllib.request
import tempfile
import shutil

def find_conda_executable():
    """Find the conda executable in common locations."""
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

def check_conda_installed():
    """Check if conda is installed and accessible."""
    try:
        conda_exe = find_conda_executable()
        if not conda_exe:
            return False, "Conda not found in PATH or common locations"

        result = subprocess.run([conda_exe, '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            return True, f"Conda found at {conda_exe}: {result.stdout.strip()}"
        else:
            return False, "Conda command failed"
    except FileNotFoundError:
        return False, "Conda not found in PATH"
    except Exception as e:
        return False, f"Error checking conda: {str(e)}"

def install_miniconda():
    """Automatically install Miniconda if conda is not found."""
    print("Conda not found. Installing Miniconda...")
    
    try:
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        # Determine the appropriate Miniconda installer
        if system == "windows":
            if "64" in machine or "amd64" in machine:
                installer_url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
                installer_name = "Miniconda3-latest-Windows-x86_64.exe"
            else:
                installer_url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86.exe"
                installer_name = "Miniconda3-latest-Windows-x86.exe"
        elif system == "linux":
            if "64" in machine:
                installer_url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
            else:
                installer_url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86.sh"
            installer_name = "Miniconda3-latest-Linux.sh"
        else:
            raise RuntimeError(f"Unsupported operating system: {system}. Only Windows and Linux are supported.")
        
        # Download installer
        with tempfile.TemporaryDirectory() as temp_dir:
            installer_path = os.path.join(temp_dir, installer_name)
            print(f"Downloading Miniconda from {installer_url}...")
            
            urllib.request.urlretrieve(installer_url, installer_path)
            print("Download completed.")
            
            # Install Miniconda
            if system == "windows":
                # Windows installer
                print("Running Miniconda installer...")
                print("NOTE: Please follow the installer prompts and restart ComfyUI after installation.")
                
                # Run installer with silent install options
                result = subprocess.run([
                    installer_path, 
                    "/InstallationType=JustMe", 
                    "/AddToPath=1", 
                    "/RegisterPython=0", 
                    "/S"  # Silent install
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    print("Silent installation failed. Running interactive installer...")
                    subprocess.run([installer_path])
                
            else:
                # Linux installer
                print("Installing Miniconda...")
                os.chmod(installer_path, 0o755)
                
                # Try silent installation first
                result = subprocess.run([
                    "bash", installer_path, "-b", "-p", 
                    os.path.expanduser("~/miniconda3")
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    # Add conda to PATH for current session
                    conda_path = os.path.expanduser("~/miniconda3/bin")
                    current_path = os.environ.get("PATH", "")
                    os.environ["PATH"] = f"{conda_path}:{current_path}"
                    print("Miniconda installed successfully!")
                else:
                    raise RuntimeError(f"Miniconda installation failed: {result.stderr}")
        
        # Verify installation
        is_installed, message = check_conda_installed()
        if is_installed:
            print("Conda installation successful!")
            return True
        else:
            print(f"Conda installation verification failed: {message}")
            return False
            
    except Exception as e:
        print(f"Failed to install Miniconda: {str(e)}")
        print("\nPlease install conda manually:")
        print("1. Download Miniconda from: https://docs.conda.io/en/latest/miniconda.html")
        print("2. Install it following the instructions for your operating system")
        print("3. Restart ComfyUI after installation")
        return False

def check_conda_environment():
    """Check if the svbrdf conda environment exists and has required packages."""
    try:
        conda_exe = find_conda_executable()
        if not conda_exe:
            return False, "Conda not found"

        # Check if svbrdf environment exists
        result = subprocess.run([conda_exe, 'env', 'list'], capture_output=True, text=True)
        if result.returncode != 0:
            return False, "Conda not found"

        if 'svbrdf' not in result.stdout:
            return False, "Environment 'svbrdf' not found"

        # Check if tensorflow is installed in the environment
        check_tf = subprocess.run([conda_exe, 'run', '-n', 'svbrdf', 'python', '-c', 'import tensorflow; print(tensorflow.__version__)'],
                                capture_output=True, text=True)
        if check_tf.returncode != 0:
            return False, "TensorFlow not found in svbrdf environment"

        return True, "Environment ready"
    except Exception as e:
        return False, f"Error checking environment: {str(e)}"

def setup_conda_environment():
    """Automatically set up the svbrdf conda environment with required dependencies."""
    print("Setting up SVBRDF conda environment automatically...")

    try:
        conda_exe = find_conda_executable()
        if not conda_exe:
            raise RuntimeError("Conda executable not found")

        # Accept conda Terms of Service for Anaconda channels (required in newer conda versions)
        print("Accepting conda Terms of Service...")
        tos_channels = [
            'https://repo.anaconda.com/pkgs/main',
            'https://repo.anaconda.com/pkgs/r'
        ]
        for channel in tos_channels:
            subprocess.run([conda_exe, 'tos', 'accept', '--override-channels', '--channel', channel],
                         capture_output=True, text=True)

        # Create conda environment using conda-forge channel (doesn't require TOS)
        print("Creating conda environment 'svbrdf' with Python 3.8...")
        result = subprocess.run([
            conda_exe, 'create', '-n', 'svbrdf', 'python=3.8', '-y',
            '-c', 'conda-forge'
        ], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to create conda environment: {result.stderr}")

        # Install dependencies
        print("Installing dependencies...")
        packages = [
            'numpy', 'imageio', 'opencv-python', 'pillow',
            'matplotlib', 'tqdm', 'lxml', 'scipy', 'huggingface_hub'
        ]

        for package in packages:
            print(f"Installing {package}...")
            result = subprocess.run([conda_exe, 'run', '-n', 'svbrdf', 'pip', 'install', package],
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Warning: Failed to install {package}: {result.stderr}")

        # Install TensorFlow 2.12.0
        print("Installing TensorFlow 2.12.0...")
        result = subprocess.run([conda_exe, 'run', '-n', 'svbrdf', 'pip', 'install', 'tensorflow==2.12.0'],
                              capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to install TensorFlow: {result.stderr}")

        print("SVBRDF environment setup complete!")
        return True

    except Exception as e:
        print(f"Failed to set up environment: {str(e)}")
        print("Please run the setup script manually:")
        if os.name == 'nt':  # Windows
            print("  setup_environment.bat")
        else:  # Linux/Mac
            print("  ./setup_environment.sh")
        return False

def check_model_checkpoints():
    """Check if the required model checkpoints exist."""
    current_dir = os.path.dirname(os.path.realpath(__file__))
    checkpoint_dir = os.path.join(current_dir, 'pretrained_checkpoints')
    
    # Required checkpoint files
    required_files = [
        'checkpoint',
        'model-deepMaterials.data-00000-of-00001',
        'model-deepMaterials.index',
        'model-deepMaterials.meta',
        'options.json'
    ]
    
    if not os.path.exists(checkpoint_dir):
        return False, "Checkpoint directory not found"
    
    missing_files = []
    for file in required_files:
        file_path = os.path.join(checkpoint_dir, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
    
    if missing_files:
        return False, f"Missing checkpoint files: {', '.join(missing_files)}"
    
    return True, "All checkpoint files present"

def download_model_checkpoints():
    """Download model checkpoints from Hugging Face."""
    print("Downloading model checkpoints from Hugging Face...")

    try:
        conda_exe = find_conda_executable()
        if not conda_exe:
            raise RuntimeError("Conda executable not found")

        current_dir = os.path.dirname(os.path.realpath(__file__))
        checkpoint_dir = os.path.join(current_dir, 'pretrained_checkpoints')

        # Use huggingface-cli download command
        cmd = [
            conda_exe, 'run', '-n', 'svbrdf',
            'huggingface-cli', 'download',
            'aruntd008/svbrdf-model',
            '--local-dir', checkpoint_dir,
            '--repo-type', 'model'
        ]

        print("Running: huggingface-cli download aruntd008/svbrdf-model...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            # Fallback: try using Python API
            print("CLI download failed, trying Python API...")
            return download_model_checkpoints_python()

        print("Model checkpoints downloaded successfully!")
        return True

    except Exception as e:
        print(f"Failed to download checkpoints: {str(e)}")
        return download_model_checkpoints_python()

def download_model_checkpoints_python():
    """Download model checkpoints using Python huggingface_hub API."""
    try:
        conda_exe = find_conda_executable()
        if not conda_exe:
            raise RuntimeError("Conda executable not found")

        # Import huggingface_hub in the svbrdf environment
        result = subprocess.run([
            conda_exe, 'run', '-n', 'svbrdf', 'python', '-c',
            '''
from huggingface_hub import snapshot_download
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
checkpoint_dir = os.path.join(current_dir, "pretrained_checkpoints")

print("Downloading model using Python API...")
snapshot_download(
    repo_id="aruntd008/svbrdf-model",
    repo_type="model",
    local_dir=checkpoint_dir,
    local_dir_use_symlinks=False
)
print("Download completed!")
'''
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.realpath(__file__)))
        
        if result.returncode == 0:
            print("Model checkpoints downloaded successfully using Python API!")
            return True
        else:
            print(f"Python API download failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Failed to download using Python API: {str(e)}")
        print("\nPlease download the model manually:")
        print("huggingface-cli download aruntd008/svbrdf-model --local-dir pretrained_checkpoints --repo-type model")
        return False

def ensure_environment():
    """Ensure conda is installed, the svbrdf environment is set up, and model checkpoints are available."""
    # First check if conda is installed
    conda_installed, conda_message = check_conda_installed()
    
    if not conda_installed:
        print(f"Conda check: {conda_message}")
        print("Attempting to install Miniconda automatically...")
        
        if not install_miniconda():
            print("Automatic conda installation failed.")
            print("Please install conda manually and restart ComfyUI.")
            print("Download from: https://docs.conda.io/en/latest/miniconda.html")
            return False
    else:
        print(f"Conda check: {conda_message}")
    
    # Now check the svbrdf environment
    is_ready, message = check_conda_environment()
    
    if not is_ready:
        print(f"SVBRDF environment check: {message}")
        print("Attempting automatic environment setup...")
        
        if not setup_conda_environment():
            print("Automatic environment setup failed. The MaterialNetNode may not work properly.")
            print("Please run the manual setup script or check your conda installation.")
            return False
    else:
        print("SVBRDF environment is ready!")
    
    # Check model checkpoints
    checkpoints_ready, checkpoint_message = check_model_checkpoints()
    
    if not checkpoints_ready:
        print(f"Model checkpoint check: {checkpoint_message}")
        print("Attempting to download model checkpoints from Hugging Face...")
        
        if not download_model_checkpoints():
            print("Automatic checkpoint download failed. The MaterialNetNode may not work properly.")
            print("Please download manually using:")
            print("huggingface-cli download aruntd008/svbrdf-model --local-dir pretrained_checkpoints --repo-type model")
            return False
    else:
        print(f"Model checkpoints: {checkpoint_message}")
    
    return True

# Automatically check and setup environment when the module is imported
print("Checking SVBRDF environment...")
ensure_environment()

from .svbrdf_node import MaterialNetNode

# Export the node class mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "MaterialNetNode": MaterialNetNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MaterialNetNode": "Material Net Node"
}

# Module metadata
__version__ = "1.0.0"
__author__ = "SVBRDF Node Implementation"
__description__ = "ComfyUI node for single-image SVBRDF material capture"

# Export everything that ComfyUI needs
__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "MaterialNetNode"
]

# Export the node class mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "MaterialNetNode": MaterialNetNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MaterialNetNode": "Material Net Node"
}

# Module metadata
__version__ = "1.0.0"
__author__ = "SVBRDF Node Implementation"
__description__ = "ComfyUI node for single-image SVBRDF material capture"

# Export everything that ComfyUI needs
__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "MaterialNetNode"
]