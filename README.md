# SVBRDF Node Setup Guide

This guide explains the SVBRDF Node, which **automatically sets up everything** including conda and its environment when first loaded.

## ✨ Fully Automatic Setup (Recommended)

The SVBRDF Node now **automatically handles ALL setup requirements** when first loaded in ComfyUI! 

### What happens automatically:

1. ✅ **Checks if conda is installed** - if not, automatically downloads and installs Miniconda
2. ✅ **Checks if the `svbrdf` conda environment exists** - creates it if missing
3. ✅ **Creates the environment with Python 3.8** if needed
4. ✅ **Installs all required dependencies** (TensorFlow 2.12.0, numpy, opencv, huggingface_hub, etc.)
5. ✅ **Downloads model checkpoints from Hugging Face** if missing
6. ✅ **Verifies the installation is working**

### First-time usage (Zero Setup Required)

1. Simply restart ComfyUI after installing this node
2. The node will automatically:
   - Install conda (Miniconda) if not present
   - Set up the complete environment on first load
3. You'll see setup progress messages in the console
4. Once complete, the MaterialNetNode will be ready to use!

**No manual downloads, no script running, no conda installation needed!**

## Manual Setup (Optional)

If you prefer manual control or the automatic setup fails, you can still run the setup scripts:

### Windows
```cmd
setup_environment.bat
```

### Linux
```bash
chmod +x setup_environment.sh
./setup_environment.sh
```

**Note: This node supports Windows and Linux. macOS is not currently supported.**

## Manual Environment Setup (Advanced)

If you need to manually recreate the environment:

1. **Create the conda environment:**
   ```bash
   conda create -n svbrdf python=3.8 -y
   conda activate svbrdf
   ```

2. **Install dependencies:**
   ```bash
   pip install numpy imageio opencv-python pillow matplotlib tqdm lxml imageio scipy
   pip install tensorflow==2.12.0
   ```

## How It Works

The MaterialNetNode automatically:
- Checks for the `svbrdf` conda environment on first import
- Creates and configures the environment if it doesn't exist
- Activates the environment before running `material_net.py`
- Uses the specific TensorFlow 2.12.0 installation in that environment
- Handles errors gracefully and provides clear feedback

## Environment Requirements

- **Python:** 3.8
- **TensorFlow:** 2.12.0
- **Dependencies:** numpy, imageio, opencv-python, pillow, matplotlib, tqdm, lxml, scipy, huggingface_hub
- **Conda:** Automatically installed if not present (Miniconda)
- **Model:** Automatically downloaded from [aruntd008/svbrdf-model](https://huggingface.co/aruntd008/svbrdf-model)

## Troubleshooting

1. **Automatic conda installation failed:**
   - Check your internet connection
   - Ensure you have sufficient disk space (at least 3GB)
   - Try restarting ComfyUI as administrator (Windows)
   - Manual fallback: Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) manually

2. **Model download failed:**
   - Check your internet connection
   - Ensure you have sufficient disk space (model is ~500MB)
   - Manual fallback: Run `huggingface-cli download aruntd008/svbrdf-model --local-dir pretrained_checkpoints --repo-type model`

3. **Automatic setup failed:**
   - Check the console output for specific error messages
   - Try running the manual setup scripts
   - Ensure you have sufficient disk space and internet connection

3. **TensorFlow errors:**
   - The automatic setup installs TensorFlow 2.12.0 specifically
   - Check GPU compatibility if using CUDA

4. **Path issues:**
   - The node automatically uses relative paths to find `material_net.py` and checkpoints
   - Ensure the `pretrained_checkpoints` folder is in the same directory as the node

5. **Permission issues (Windows):**
   - Try running ComfyUI as administrator for the first setup
   - Some antivirus software may block automatic downloads

## Usage in ComfyUI

The setup is now completely transparent:

1. **No manual setup required** - everything happens automatically!
2. The node automatically activates the `svbrdf` conda environment
3. Processes your input image using the trained model
4. Returns 5 outputs: input_image, normals, diffuse, roughness, specular

The environment handling is completely transparent to the user - just load ComfyUI and start using the node!