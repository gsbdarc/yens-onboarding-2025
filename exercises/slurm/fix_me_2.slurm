#!/bin/bash

#SBATCH --job-name=fix-me
#SBATCH --output=logs/fix-me-2-%j.out
#SBATCH --time=01:00:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=your_email@stanford.edu

source venv/bin/activate

# Run the python script
python extract_form_3_one_file.py 
