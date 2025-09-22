#!/bin/bash

echo "Setting up SVBRDF conda environment..."

echo "Creating conda environment 'svbrdf' with Python 3.8..."
conda create -n svbrdf python=3.8 -y

echo "Activating svbrdf environment..."
source activate svbrdf

echo "Installing common dependencies..."
pip install numpy imageio opencv-python pillow matplotlib tqdm lxml imageio scipy

echo "Installing TensorFlow 2.12.0..."
pip install tensorflow==2.12.0

echo ""
echo "Setup complete! The 'svbrdf' conda environment is ready."
echo ""
echo "To manually activate this environment, run:"
echo "conda activate svbrdf"
echo ""
echo "The MaterialNetNode will automatically use this environment when processing images."