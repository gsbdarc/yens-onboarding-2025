#!/bin/bash

#SBATCH --job-name=fix-me
#SBATCH --output=logs/fix-me-3-%j.out
#SBATCH --time=01:00:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=your_email@stanford.edu

cd yens-onboarding-2025/exercises

source venv/bin/activate

# Run the python script
python scripts/extract_form_3_one_file.py
