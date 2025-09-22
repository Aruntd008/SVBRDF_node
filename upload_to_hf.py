from huggingface_hub import HfApi
import os

# Repository details
repo_id = "aruntd008/svbrdf-model"  # Replace with your repo ID
folder_path = "./pretrained_checkpoints"

# Initialize Hugging Face API
api = HfApi()

# Upload all files in the folder
for root, _, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        # Upload each file to the repository
        api.upload_file(
            path_or_fileobj=file_path,
            path_in_repo=file_path.replace("./", ""),  # Preserve folder structure
            repo_id=repo_id,
            repo_type="model",  # Or "dataset" if you chose a dataset repo
            commit_message=f"Upload {file} to pretrained_checkpoints"
        )
        print(f"Uploaded {file}")