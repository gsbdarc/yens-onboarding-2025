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

Login to the Yens.

Take a note of which interactive yen (yen[1-5]) you are on. Then, open a new terminal (or second tab if using Jupyter), and connect to the **same** yen. 

Now you should have two terminals, both conneted to the same interactive yen. 

In one of the terminals, run a mystery script four times:

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

   This line is called a "shebang." It tells the system to run the script using the Bash shell interpreter (`/bin/bash`). This ensures consistent behavior for shell commands like `cd`, `source`, and environment variables — regardless of the user's default shell.

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

   The `--output=my-first-job.out` flag tells Slurm to save all job outputs (printed to screen) in a text file named `my-first-job.out` in the same directory (`~/yens-onboarding-2025/exercises/slurm`).

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

The `123456` is a job ID which is unique for every job on the cluster. 

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
Let’s now run a real script using Slurm — and discuss paths, resource requests, and how to organize logs.

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

- Save output to `~/yens-onboarding-2025/exercises/slurm/my-first-job.out` (because of `--output=my-first-job.out`) 



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
Let’s write a new Slurm script that runs the Python script `scripts/mystery_script.py`.

As we know, this script uses multiple CPU cores, so we’ll request **10 cores**.

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

#### About the `logs/` folder
The line `#SBATCH --output=logs/mystery-%j.out` tells Slurm to write all job output (stdout and stderr) to a file inside the `logs/` folder. The `%j` gets replaced by the Slurm job ID, so each job has its own unique log file.

Before submitting the job, we must create the `logs` directory:

```
cd ~/yens-onboarding-2025/exercises/slurm
mkdir logs
```

We also do the following in the slurm script:

```
# Move into the correct working directory
cd ~/yens-onboarding-2025/exercises

# Activate your Python environment
source venv/bin/activate
```

This activates your python virtual environment. It makes sure you are running the python script using the virtual environment we created earlier.

```
python scripts/mystery_script.py
```

This runs the actual Python script. It assumes you're inside the `exercises/` directory and that the `scripts/` subfolder is there.

> If you don't `cd` into the correct working directory, relative paths like `scripts/mystery_script.py` will fail.
{: .tip }

Save and exit the file.

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

### Step 4: Monitor the job
To check the status of your job:

```
squeue -u $USER
```

You’ll see a table with columns like JOBID, NAME, STATE, TIME, and NODELIST.
Your job may show up as `PD` (pending), `R` (running), or disappear when it’s finished.

### Step 5: View the output log
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

✅ **Recap**:

You’ve now:

- Written a Slurm script to run a Python job using multiple CPU cores

- Activated a virtual environment in a Slurm context

- Used job output logs to track success or failure

- Submitted, monitored, and inspected a real cluster job

**Next up**: handling jobs that fail, scaling your jobs, adding fault tolerance, and running many jobs at once using arrays.


### 💻 Exercise: debugging cluster jobs
In this exercise, you'll run a series of broken Slurm scripts that simulate **common mistakes** researchers make when working on a cluster.

Each one will fail for a different reason — your job is to figure out why by inspecting the logs and **fixing the script**.

❓ What happens if your job crashes?

- It may disappear from `squeue` without printing output
- You may get an email from Slurm about the failure
- Your `.out` file might contain Python errors or clues


❓ What information is in the Slurm log files?
- Anything printed by your script (`stdout`)
- Python tracebacks (`stderr`)
- Resource usage (sometimes)
- Error messages if Slurm kills the job (memory/time)

❓ How do you rerun failed jobs?
- Open the `.slurm` script
- Fix the error
- Resubmit it using `sbatch`



---

### 🔧 Try These Broken Scripts
1. Navigate to your `slurm/` directory: 
  
   ```
   cd ~/yens-onboarding-2025/exercises/slurm   
   ```

2. Submit each broken script:

   ```
   sbatch fix_me.slurm
   sbatch fix_me_2.slurm
   sbatch fix_me_3.slurm
   ```

3. Check the logs:

   ```
   cd logs
   cat fix-me-<jobid>.out
   ```

4. Identify the issue and fix it. Use the Jupyter Text Editor.

5. Resubmit once fixed:

   ```
   sbatch fix_me.slurm
   ```

6. 🟩 / 🟥 when complete

### 💡 Bonus Challenge

Try to debug this longer but broken script:

```
sbatch extract_form_3_one_file_broken.slurm
```

- 🟩 / 🟥

### ✅ Fixes for Each Broken Script

Below are common fixes for the broken job scripts you've submitted. These mimic common real-world mistakes with paths and environments.


### 🔧 `fix_me.slurm`

**Problem:**
- Missing `cd` to the correct working directory
- Missing environment activation
- Assumes `scripts/extract_form_3_one_file.py` is in the current folder (it isn't)


### 🔧 `fix_me_2.slurm`
**Problem:**
- Doesn’t `cd` into the right `~/yens-onboarding-2025/exercises` project folder, so `venv` folder is not found
- Script calls `python extract_form_3_one_file.py`, assuming the 🐍 file is in the current directory


### 🔧 `fix_me_3.slurm`

**Problem:**
- Uses a relative path for `cd yens-onboarding-2025/exercises`

**Fix:**
```bash
cd ~/yens-onboarding-2025/exercises
source venv/bin/activate
python scripts/extract_form_3_one_file.py
```

> Always double-check:
- Your working directory (`cd`)
- That your script paths are correct
- That your virtual environment is activated
{: .tip }

## 💥 What Happens When Jobs Fail?

Sometimes your Slurm job script will **run**, but still **fail before finishing**. Two common reasons for this are:

- Not requesting **enough memory**
- Not requesting **enough time**

Let’s simulate both types of failure with two example jobs.


### Failure Case 1: Not Enough RAM

Let’s write a script that tries to allocate too much memory.

1. Create the file:

   ```bash
   touch slurm/fail_not_enough_memory.slurm
   ```

2. Add the following:

   ```
   #!/bin/bash
   #SBATCH --job-name=fail-mem
   #SBATCH --output=logs/fail-mem-%j.out
   #SBATCH --time=00:05:00
   #SBATCH --mem=100M        # Too little!
   #SBATCH --cpus-per-task=1
   #SBATCH --mail-type=END,FAIL
   #SBATCH --mail-user=your_email@stanford.edu
   
   cd ~/yens-onboarding-2025/exercises
   source venv/bin/activate
   
   python scripts/memory_hog.py
   ```

3. Save the file.

   The script `memory_hog.py` should allocate a large list or array that uses more than 100 MB of RAM.
   You can modify it to simulate memory use like this:

   ```python
   # memory_hog.py
   big_list = [0] * int(1e8)  # ~800MB if using 8-byte ints
   print("Allocated a big list")
   ```


4. Submit:
 
   ```
   sbatch slurm/fail_not_enough_memory.slurm
   ```

🟩 / 🟥

### Failure Case 2: Not Enough Time

1. Create the file:

   ```
   touch slurm/fail_not_enough_time.slurm
   ```

2. Add this script:
  
   ```
   #!/bin/bash
   #SBATCH --job-name=fail-time
   #SBATCH --output=logs/fail-time-%j.out
   #SBATCH --time=00:00:05       # Just 5 seconds!
   #SBATCH --mem=1G
   #SBATCH --cpus-per-task=1
   #SBATCH --mail-type=END,FAIL
   #SBATCH --mail-user=your_email@stanford.edu
   
   cd ~/yens-onboarding-2025/exercises
   source venv/bin/activate
   
   python scripts/sleep_longer.py
   ```

3. Add the Python script:

   ```
   # scripts/sleep_longer.py
   import time
   time.sleep(30)
   print("Finished sleeping.")
   ```

4. Submit:

   ```
   sbatch slurm/fail_not_enough_time.slurm
   ```

🟩 / 🟥

### 🔍 Inspecting Failed Jobs

After either job fails:

1. Go to the `logs/` folder.

2. Run:

   ```
   cat fail-mem-<jobid>.out
   ```
  
   or

   ```
   cat fail-time-<jobid>.out
   ```

   You may see errors like:

   - `Killed` (from the memory-limited job)
   - `DUE TO TIME LIMIT` (in the time-limited job)

> Read Slurm emails after the job fails for memory utilization and hints on why it failed.
{: .tip }


### 🛠️ How to Fix It
- If a job ran out of memory, increase `#SBATCH --mem=...` to a realistic number (e.g., 2G, 4G, etc.).

- If it ran out of time, increase `#SBATCH --time=...` based on how long your script actually needs (remember to use `time` interactively to measure).

- Fix it and resubmit.

🟩 / 🟥
---


## Submitting Form 3 Extraction Job
Now that you've seen how to submit a Slurm job, let’s process a real SEC Form 3 filing using OpenAI and a structured output model with Pydantic.

### 🐍 View the script

Let’s inspect the single-file processing script:

```bash
cat scripts/extract_form_3_one_file.py
```

You should see code that:

- Loads a filing from disk
- Defines a `Form3Filing` Pydantic model
- Uses OpenAI to extract structured information from the text
- Prints the extracted result as a Python dictionary

### View the Slurm job script
This Slurm script runs the code above:

```
cat slurm/extract_form_3_one_file.slurm
```

You should see:

```
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
```

### ✅ Submit it!

From the `exercises/` directory, run:

```
sbatch slurm/extract_form_3_one_file.slurm
```

After submission:

- Monitor the job with `squeue -u $USER`
- Check the output in `logs/` once it finishes

🟩 / 🟥

## Scaling Up to Process Many Files
Now let’s move from a single example to 100 filings. 

We already have a file named `form_3_100.csv` in `data` directory containing 100 rows, each with a path to an SEC Form 3 filing on the Yens.

Let’s take a look:

```
cd exercises
head form_3_100.csv
```

You should see a column called `filepath` with full paths to `.txt` filings.

### 🐍 View the batch-processing script

```
cat scripts/extract_form_3_batch.py
```

This version of the script:

- Reads `form_3_100.csv` using pandas
- Loops over all file paths
- Sends each filing to OpenAI sequentially
- Collects all structured results in a list
- Saves them into one file: `results/form3_batch_results.json`

This is still a single-core, sequential job good for testing and small data processing runs.

### View the batch Slurm script

```
cat slurm/extract_form_3_batch.slurm
```

It should look like:

```
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
```

### ✅ Submit the batch job

Edit the slurm file to include your email.

Then submit from `slurm` directory:
```
cd exercises/slurm
sbatch slurm/extract_form_3_batch.slurm
```

Track it as usual:
```
squeue -u $USER
```

Check the logs once the job completes:

```
cat logs/form3-batch-<jobid>.out
```

🟩 / 🟥

❓ What do you see in the log file? 

❓ What do you see in the `results` folder? 

❓ How can we improve upon this? 

## 🛠 Fault Tolerance: Why We Need to Track Progress

Let’s talk about what happens when things go wrong in real-world file processing.


### 🔍 Step 1: Run the batch job

We ran the `extract_form_3_batch.py` script on our `form_3_100.csv` file.

> This CSV intentionally contains a broken file path around the 8th entry so that the job will fail.  
{: .important }

**What happened?**
You’ll see that the script:

- Processed the first ~8 files successfully
- Then crashed when it hit a bad path
- Lost all progress — the earlier results were stored in memory only and never written to disk

> In a long sequential job, one bad file can ruin **hours of compute** if you only save results at the end.
{: .note }


### ⚠️  What We're Doing Now

In our current approach, if a long batch job fails, we:

- Have to start **from scratch**
- Waste compute time and API calls (a.k.a. 💸 money)
- Face many possible **failure modes**:
  - Malformatted paths
  - Corrupted input files
  - API timeouts or rate limits
  - Running out of Slurm time or memory
- Manually figure out where the failure happened
- Fix or remove the problematic file from the input list
- Re-run the **entire** job

That’s not scalable — especially when jobs take hours or days.


### ✅ What Can We Do Instead?

We can make our script **fault-tolerant** by:
1. **Saving results as we go** — so progress isn’t lost when something fails
2. **Logging failures** to a separate file for later review
3. **Skipping already-processed files** when resuming a job

This way:
- If the job fails after file #80, we still keep results for files #1–79
- A re-run processes *only* the remaining files
- We minimize wasted time, compute, and API costs

---

Up next: we’ll run a **checkpointed batch script** that does all of this automatically.


## ✅ Fault‑Tolerant Batch (Save As You Go & Resume) Script
We’re upgrading the batch job so it **keeps progress** even if it crashes mid‑run, then **skips already‑processed files** on the next run.

You’ll use this Python script:

```bash
cat scripts/extract_form_3_batch_checkpoint.py
```

It:

- Reads the file list from `/scratch/shared/yens-onboarding-2025/data/form_3_100.csv`

- Loads existing results from results/form3_batch.json (if present)

- Processes only the remaining files

- Appends in memory and writes to JSON after each file

### View the Slurm job

```
cat slurm/extract_form_3_batch_checkpoint.slurm
```

You should see:

```
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
```

### Submit, Monitor, Resume
From `slurm` directory:

```
cd ~/yens-onboarding-2025/exercises/slurm
sbatch extract_form_3_batch_checkpoint.slurm
```

Monitor:

```
squeue -u $USER
```

Inspect logs when done:

```
cat logs/form3-checkpoint-<jobid>.out
```

🟩 / 🟥

### 💻 Exercise: Fixing a Broken Path and Resubmitting

Our checkpointed batch job just failed!  

If you check the **log file** in `logs/`, you’ll see the traceback points to a missing `.txt` on file #9’s path.

**What happened?**  
- One of the file paths in our `form_3_100.csv` file is wrong.
- The Python script can’t open the file and stops at that point.
- Luckily, with checkpointing, everything before the failure is already saved.

1. In the most recent `.out` file, look for the last processed file — the one right before the crash.

2. The instructor will correct the broken path in the CSV file.

3. After they correct the input file, resubmit the job.


Because we’re using checkpointing, we don’t need to start from scratch —
the script will skip already processed files and pick up right after file #8.

```
sbatch extract_form_3_batch_checkpoint.slurm
```

Monitor the logs and verify the run completes:

```
squeue -u $USER
tail -f logs/form3-batch-<new_jobid>.out
```

When finished, check `results/form3_batch.json` to confirm all 100 results are there.

🟩/🟥



## ⚡️ Parallel Processing with Slurm Arrays (100 filings at once)
Sequential data processing is slow. Let’s parallelize and run **one filing per Slurm task** using an **array job**.

**Idea:** Give each task an index (`0..99`) and have the Python script process the file at that row in `form_3_100.csv`.

---

### Concept: Slurm array 


When you submit with `#SBATCH --array=0-99`, Slurm launches 100 tasks.  
Each task gets an environment variable:

```
SLURM_ARRAY_TASK_ID=0 # for the first task
SLURM_ARRAY_TASK_ID=1 # for the second
...
SLURM_ARRAY_TASK_ID=99 # for the last
```


We’ll pass that index as a command-line argument to Python to select the matching row in the CSV. We can use the index directly in Python to pick which file to process.

Our 🐍 script will process **one** row by index.

Let's look at the 🐍 script:

```
cat scripts/extract_form_3_one_from_csv.py
```




