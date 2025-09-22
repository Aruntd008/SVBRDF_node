import torch
import numpy as np
import os
import tempfile
import subprocess
from PIL import Image

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
            
            # Run material_net.py in the svbrdf conda environment
            # Using cmd.exe on Windows to activate conda environment

            #python material_net.py --input_dir inputExamples/ --mode eval --output_dir examples_outputs --checkpoint ./pretrained_checkpoints/ --imageFormat png --scale_size 256 --batch_size 1 --correctGamma      
            activate_cmd = "conda activate svbrdf"
            python_cmd = f"python {script_path} --mode eval --input_dir {input_path} --output_dir {output_dir} --checkpoint {checkpoint_dir} --imageFormat png --scale_size 256 --batch_size 1 --correctGamma"
            
            # Combine conda activation and python command
            full_cmd = f"{activate_cmd} && {python_cmd}"
            
            # Run the command using cmd.exe shell with correct working directory
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, cwd=dir_path)
            
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