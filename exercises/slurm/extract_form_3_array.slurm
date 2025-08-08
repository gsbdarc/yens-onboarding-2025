#!/bin/bash
#SBATCH --job-name=form3-array
#SBATCH --output=logs/form3-array-%A_%a.out
#SBATCH --array=0-99
#SBATCH --time=02:00:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=your_email@stanford.edu

cd ~/yens-onboarding-2025/exercises
source venv/bin/activate

# Pass the array index as an argument to Python
python scripts/extract_form_3_one_from_csv.py $SLURM_ARRAY_TASK_ID
