#!/bin/bash
#SBATCH --job-name=form3-checkpoint
#SBATCH --output=logs/form3-checkpoint-%j.out
#SBATCH --time=04:00:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=1
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=your_email@stanford.edu

# Project working directory 
cd ~/yens-onboarding-2025/exercises

# Activate your environment
source venv/bin/activate

# Run the checkpointed batch processor
python scripts/extract_form_3_batch_checkpoint.py
