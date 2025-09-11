#!/bin/bash
#SBATCH --job-name=form3-one
#SBATCH --output=logs/form3-one-%j.out
#SBATCH --time=00:05:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=your_email@stanford.edu

cd ~/yens-onboarding-2025/exercises
source venv/bin/activate

python scripts/extract_form_3_one_file.py
