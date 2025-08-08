#!/bin/bash
#SBATCH --job-name=form3-batch
#SBATCH --output=logs/form3-batch-%j.out
#SBATCH --time=02:00:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=1
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=your_email@stanford.edu

cd ~/yens-onboarding-2025/exercises
source venv/bin/activate

python scripts/extract_form_3_batch.py
