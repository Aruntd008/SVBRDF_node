# SVBRDF Node Troubleshooting Guide

## Quick Diagnostics

### Check if checkpoints are properly installed:
```bash
python check_checkpoints.py
```

### Manually download checkpoints:
```bash
python download_checkpoints.py
```

---

## Common Issues

### 1. Missing Model Checkpoints

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: '.../pretrained_checkpoints/options.json'
```

**Solution:**

#### Option A: Automatic Download (Recommended)
```bash
conda activate svbrdf
python download_checkpoints.py
```

#### Option B: Manual Download
1. Visit: https://huggingface.co/aruntd008/svbrdf-model
2. Download all files to `pretrained_checkpoints/` directory
3. Required files:
   - `checkpoint`
   - `model-deepMaterials.data-00000-of-00001`
   - `model-deepMaterials.index`
   - `model-deepMaterials.meta`
   - `options.json`

#### Option C: Using huggingface-cli
```bash
conda activate svbrdf
huggingface-cli download aruntd008/svbrdf-model --local-dir pretrained_checkpoints --repo-type model
```

---

### 2. Conda Environment Not Found

**Error:**
```
EnvironmentLocationNotFound: Not a conda environment: /root/miniconda3/envs/svbrdf
```

**Solution:**
```bash
# Run the setup script
./setup_environment.sh   # Linux/Mac
# or
setup_environment.bat    # Windows
```

---

### 3. Conda Terms of Service Error

**Error:**
```
CondaToSNonInteractiveError: Terms of Service have not been accepted
```

**Solution:**
```bash
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
```

Then re-run the setup:
```bash
./setup_environment.sh
```

---

### 4. TensorFlow GPU Warnings

**Warning:**
```
Could not find cuda drivers on your machine, GPU will not be used.
```

**Note:** This is just a warning. The node will work on CPU, but will be slower. If you want GPU acceleration:

1. Install CUDA drivers for your GPU
2. Install TensorFlow with GPU support:
```bash
conda activate svbrdf
pip install tensorflow==2.12.0
```

---

## Verification Steps

After fixing any issues, verify the installation:

1. **Check conda environment:**
```bash
conda env list | grep svbrdf
```

2. **Check TensorFlow:**
```bash
conda activate svbrdf
python -c "import tensorflow; print(tensorflow.__version__)"
```

3. **Check checkpoints:**
```bash
python check_checkpoints.py
```

4. **Test the node in ComfyUI:**
   - Restart ComfyUI
   - Add the MaterialNet node to your workflow
   - Process a test image

---

## Getting Help

If you're still experiencing issues:

1. Run diagnostics:
```bash
python check_checkpoints.py
conda activate svbrdf
python -c "import tensorflow; print(tensorflow.__version__)"
```

2. Check the ComfyUI console for detailed error messages

3. Report the issue with:
   - Full error message
   - Output of diagnostic commands
   - Your operating system and environment (Docker/RunPod/local)

