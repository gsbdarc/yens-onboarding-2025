
---
title: Day 2 — Running and Scaling Jobs on the Yens
layout: page
nav_order: 2
---

# {{ page.title }}

## Overview

Today we move from interactive work on the Yens and Jupyter to **running scheduled jobs on the Yens cluster** using Slurm — cluster's job scheduler. You’ll learn how to submit jobs, monitor them, debug them, and scale them up for real research.

---

## Learning Goals

By the end of today you will be able to:

- Write and submit Slurm batch job scripts
- Estimate appropriate resources (CPU, memory, time)
- Monitor and cancel running jobs
- Handle failed or stuck jobs
- Organize code for cluster-based research workflows
- Scale up tasks using job arrays


## Cluster Resources
TODO
✏️ Interactive Yens
✏️ Yen-Slurm Cluster

## 💻 Run a mystery python script

Login to the Yens. Take a note of which interactive yen (yen[1-5]) you are on. Then, open a new terminal (or second tab if using Jupyter), and connect to the **same** yen. 

Now you should have two terminal both conneted to the same interactive yen. 

In one of the terminals, run my mystery script:

```
cd yens-onboarding-2025/exercises/scripts
python3 mystery_script.py
```

1. While the script is running, in a second terminal connected to the same yen, watch the script run while running `htop`.

2. While the script is running, in a second terminal connected to the same yen, watch the script run while running `htop -u $USER`.

3. While the script is running, in a second terminal connected to the same yen, watch the script run while running `watch userload`.

4. To time the script, run in one of the terminals:

```
time python3 mystery_script.py
```
Key things to watch:

- Peak RAM usage
- Number of cores used
- Runtime


Compare with your neighbor the time, cores and RAM usage for this script.

❓ What do you see?

🟩/🟥

Now we know how many resources the script needs, we can submit it as a batch job to the scheduler requesting the resources from it.

## Submitting your first Yen-Slurm job

Navigate to `~/yens-onboarding-2025/exercises/slurm` directory:

```
cd ~/yens-onboarding-2025/exercises/slurm
```

Let’s make your first slurm job script. You can do this in JupyterHub usign Text Editor.

  1. Make a new file in the `slurm` directory called `my_first_job.slurm`.

  2. Start the file with the bash shebang line:

   ```
   #!/bin/bash
   ```

  3. Add Slurm job configuration flags that request appropriate resources (replace `your_email` with your Stanford email):  

   ```
   #SBATCH --job-name=my-first-job
   #SBATCH --output=my-first-job.out
   #SBATCH --time=10:00
   #SBATCH --mem=4G
   #SBATCH --cpus-per-task=1
   #SBATCH --mail-type=ALL
   #SBATCH --mail-user=your_email@stanford.edu
   ```

  The `--output=my-first-job.out` flag tells Slurm to save all job output (printed to screen) in a file named `my-first-job.out` in the same directory (`~/yens-onboarding-2025/exercises/slurm`).

  4. Finally, add a line to print a message: 

  ```
  echo "Hello there!" 
  ```

  Save this file.

  🟩/🟥

### 💻 Let’s submit it:

Run:
```
sbatch my_first_job.slurm
```
You’ll see output like:

```
Submitted batch job 123456
```

The `123456` is a job ID which is unique for every cluster job. 

## Monitoring slurm jobs

View the job queue:

```
squeue 
```

Or filter to just your jobs:
```
squeue -u $USER
```

Cancel a job if needed:
```
scancel <job-id>
```

## Checking results
After the job completes:

Look at the `.out` file created:
```
cat my-first-job.out
```

You should see:

```
Hello there!
```

If you included your email in `--mail-user`, you’ll also receive an email from Slurm when the job starts and ends.

## Running a python script via slurm
Let’s now run a real script using Slurm — and discuss **paths**, **resource requests**, and how to organize logs.

---

### 📁 Step 1: Understand paths on the cluster

**Slurm job working directory behavior**:

A Slurm job runs in the **current working directory**, meaning the directory you were in when you ran `sbatch`.

This affects:

- Where the job output files (like `--output=...`) will be written unless an absolute path is given

- Any relative paths used in your Slurm script (e.g., `python scripts/myscript.py`)


So for example:
```
cd ~/yens-onboarding-2025/exercises/slurm
sbatch my_first_job.slurm
```
This job will:

- Run from the `~/yens-onboarding-2025/exercises/slurm` folder

- Save output to `~/yens-onboarding-2025/exercises/slurm/my-first-job.out (because of `--output=my-first-job.out`) 



Now consider this alternative way to run the same job:
```
cd ~/yens-onboarding-2025/exercises/
sbatch slurm/my_first_job.slurm
```

You’re submitting the same script, but from a different directory.

This time, the `.out` file will be written to `~/yens-onboarding-2025/exercises/my-first-job.out`.

Slurm always evaluates relative paths (for logs, scripts, etc.) from the directory where `sbatch` was executed — *not* where the `.slurm` file lives.


### Example: calling a python script from `scripts/`
If your slurm job script includes:

```
python scripts/mystery_script.py
```

That line will only work if the current working directory contains the `scripts/` folder.

- If you ran `sbatch` from `~/yens-onboarding-2025/exercises/`, it works.

- If you ran it from `slurm/`, it will fail unless you `cd ..` or change paths.

### 📝 Step 2: Create a slurm script to run `mystery_script.py`
Let’s write a new Slurm job script that runs the Python script `scripts/mystery_script.py`.

As we know, this script uses multiple CPU cores, so we’ll request **10 cores**.

---

  1. Navigate to the `slurm/` directory:
  
  ```bash
  cd ~/yens-onboarding-2025/exercises/slurm
  ```

  2. Create a new text file in JupyterHub Text Editor (make sure it's in the `slurm` directory) and paste the following (update the email line!):

  ```
  #!/bin/bash
  #SBATCH --job-name=mystery
  #SBATCH --output=logs/mystery-%j.out
  #SBATCH --time=00:05:00
  #SBATCH --mem=8G
  #SBATCH --cpus-per-task=10
  #SBATCH --mail-type=ALL
  #SBATCH --mail-user=your_email@stanford.edu
  
  # Move into the correct working directory
  cd ~/yens-onboarding-2025/exercises
  
  # Activate your Python environment
  source venv/bin/activate
  
  # Run the Python script
  python scripts/mystery_script.py
  ```
  
  3. Name the file `mystery_script.slurm`.

  #### About the `logs/` Folder
  The line `#SBATCH --output=logs/mystery-%j.out` tells Slurm to write all job output (stdout and stderr) to a file inside the `logs/` folder. The `%j` gets replaced by the Slurm job ID, so each job has its own unique log file.

  Before submitting the job, we must create the `logs` directory:

  ```
  cd ~/yens-onboarding-2025/exercises/slurm
  mkdir logs
  ```

  We also do the following in the slurm script:

  ```
  source venv/bin/activate
  ```

  This activates your python virtual environment. It makes sure you are running the python script using the virtual environment we created earlier.

  ```
  python scripts/mystery_script.py
  ```
  This runs the actual Python script. It assumes you're inside the `exercises/` directory and that the `scripts/` subfolder is there.

  > If you don't `cd` into the correct working directory, relative paths like `scripts/mystery_script.py` may fail.
  {: .tip }


🟩 / 🟥

### Step 3: Submit the job to run `mystery_script.py`

We’re now ready to submit a real python job to the Yen-Slurm cluster.

#### Before submission:
- You created `run_mystery_script.slurm` inside the `slurm/` folder
- You created a `logs/` folder to capture output

Make sure you're in the `slurm/` folder before submitting so that relative paths in the script work correctly:

```bash
cd ~/yens-onboarding-2025/exercises/slurm
sbatch mystery_script.slurm
```

### Step 4: Monitor the Job
To check the status of your job:

```
squeue -u $USER
```

You’ll see a table with columns like JOBID, NAME, STATE, TIME, and NODELIST.
Your job may show up as `PD` (pending), `R` (running), or disappear when it’s finished.

### Step 5: View the Output Log
Once the job finishes, go to your `logs/` folder and inspect the output:

```
cd logs
ls
```

You should see a file like:
```
mystery-456789.out
```

View it with:

```
cat mystery-456789.out
```

This file contains:

- Any printed output from the script

- Any errors or traceback messages

- Useful debug information

> This is your first file to check when things don’t work — start with the `.out` file.
{: .tip }


