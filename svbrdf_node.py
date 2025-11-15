import torch
import numpy as np
import os
import tempfile
import subprocess
from PIL import Image
import shutil

class MaterialNetNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE", "IMAGE", "IMAGE", "IMAGE", "IMAGE",)
    RETURN_NAMES = ("input_image", "normals", "diffuse", "roughness", "specular",)
    FUNCTION = "run"
    CATEGORY = "image processing"

    def _find_conda_executable(self):
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

    def run(self, image):
        # Use absolute path to pretrained_checkpoints
        dir_path = os.path.dirname(os.path.realpath(__file__))
        checkpoint_dir = os.path.join(dir_path, 'pretrained_checkpoints')

        img_np = image[0].cpu().numpy()

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "input.png")
            pil_img = Image.fromarray((img_np * 255).astype(np.uint8))
            pil_img.save(input_path)

            output_dir = os.path.join(tmpdir, "output")

            script_path = os.path.join(dir_path, "material_net.py")

            # Find conda executable - check common locations
            conda_exe = self._find_conda_executable()
            if not conda_exe:
                raise RuntimeError("Conda executable not found. Please ensure conda is installed and in PATH.")

            # Run material_net.py in the svbrdf conda environment
            # Using 'conda run' which works in both interactive and non-interactive shells
            # This is compatible with Linux containers and doesn't require 'conda init'

            # Build the command using conda run with full path to conda
            cmd = [
                conda_exe, 'run', '-n', 'svbrdf', 'python', script_path,
                '--mode', 'eval',
                '--input_dir', input_path,
                '--output_dir', output_dir,
                '--checkpoint', checkpoint_dir,
                '--imageFormat', 'png',
                '--scale_size', '256',
                '--batch_size', '1',
                '--correctGamma'
            ]

            # Run the command with correct working directory
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=dir_path)
            
            # Check if the command was successful
            if result.returncode != 0:
                raise RuntimeError(f"Material net inference failed. Error: {result.stderr}")
            
            image_dir = os.path.join(output_dir, "images")
            
            input_saved = os.path.join(image_dir, "input-inputs.png")
            normals = os.path.join(image_dir, "input-outputs-0-.png")
            diffuse = os.path.join(image_dir, "input-outputs-1-.png")
            roughness = os.path.join(image_dir, "input-outputs-2-.png")
            specular = os.path.join(image_dir, "input-outputs-3-.png")
            
            def load_img(path):
                img = Image.open(path).convert("RGB")
                arr = np.array(img).astype(np.float32) / 255.0
                return torch.from_numpy(arr).unsqueeze(0)
            
            input_t = load_img(input_saved)
            normals_t = load_img(normals)
            diffuse_t = load_img(diffuse)
            roughness_t = load_img(roughness)
            specular_t = load_img(specular)
            
            return (input_t, normals_t, diffuse_t, roughness_t, specular_t,)