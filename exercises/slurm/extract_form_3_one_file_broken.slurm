#!/bin/bash

#SBATCH --job-name=extract-one-file
#SBATCH --output=logs/extract-one-file-%j.out
#SBATCH --time=01:00:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=your_email@stanford.edu

cd $HOME/yens-onboarding-2025/exercises

# Activate virtual environment
source venv/bin/activate

# Run the python script
python scripts/extract_form_3_one_file_broken.py 
