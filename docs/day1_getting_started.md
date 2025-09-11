---
title: Day 1 — Getting Started on the Yens Cluster
layout: page
nav_order: 1
---

# {{ page.title }}

## Overview

This first session introduces you to Stanford GSB’s research computing cluster — the Yens. You’ll learn how to log in, navigate the file system, set up reproducible Python environments, and run code interactively on the cluster or through JupyterHub. We’ll also take our first step into Slurm by submitting a simple batch job.

> 🔗 **Need help?** Visit [rcpedia.stanford.edu](https://rcpedia.stanford.edu/) or reach out via the [GSB DARC Slack](https://app.slack.com/client/E7SAV7LAD/C01JXJ6U4E5).

---

## Learning goals

By the end of today you will be able to:

- Connect to the Yens via SSH and JupyterHub.
- Navigate the file system using basic shell commands.
- Copy files and folders between your laptop and the cluster.
- Create and activate Python virtual environments.
- Install and link Jupyter kernels to your custom environment.
- Run code via Python scripts and Jupyter notebooks on the Yens.
- Use environment variables securely (e.g., for API keys).
- Explore paths and reproducibility on shared systems.
- Estimate appropriate resources (CPU, memory, time) of scripts interactively.
- Submit your first simple job with Slurm.

---


## Connecting to the Yens

> If you are a Mac or Linux user, you can use the native terminal for these exercises. 
{: .important }

> If you are a Windows user, you can use Git Bash to run these commands.
{: .important }

To SSH from your terminal (replace `<SUNetID>` with your SUNet ID; don't type the `<`, `>` symbols):

```bash
ssh <SUNetID>@yen.stanford.edu
```
You’ll be prompted for Duo authentication.

🟩 / 🟥

### 💻 Command line basics

When you `ssh` to the Yens, you are in your "home" directory. 

Let's explore your environment:

```
pwd                   # Show your current directory
ls -lah               # List files, including hidden ones
cd /scratch/shared    # Change directories
cd                    # Go back to your home directory
mkdir new_dir         # Make a new folder
touch test.py         # Create a blank file
rm test.py            # Be careful! This deletes the file
```


### Copying data to the Yens

Open a new terminal on your local machine (not connected to the Yens).

Make a new file in the text editor of your choice and save it where you can find it  (e.g., your Desktop). For example, name it `hello_yens.txt`. 

Then, we will upload this file from your laptop to the cluster using `scp` (run from your **local** terminal, not the Yens):

```bash
scp ~/Desktop/hello_yens.txt <SUNetID>@yen.stanford.edu:~
```
You’ll be prompted for Duo authentication. After logging in, check that the file was copied correctly by SSHing into the Yens and running `ls` in your home directory.
🟩/🟥

> To copy a folder, use a `-r` (recursive) flag with `scp`.
{: .tip }

Open a new terminal on your local machine (not connected to the Yens).

Make a new **folder** where you can find it  (e.g., your Desktop). For example, name it `test_folder_from_local`. 

Put a file in the folder (text, image, doc, etc). Let's take a screen shot of your screen and move it into this new folder. 

Then, we will upload this folder from your laptop to the cluster using `scp` (run from your **local** terminal, not the Yens):

```bash
scp -r ~/Desktop/test_folder_from_local <SUNetID>@yen.stanford.edu:~
```
You’ll be prompted for Duo authentication. After logging in, check that the folder was copied correctly by SSHing into the Yens and running `ls` in your home directory.
🟩/🟥



## Understanding paths and modules on the Yens
TODO

✏️ All this path and version stuff is important for reproducibility. Let’s take a beat to think through what reproducibility means in research.


## 💻 Copy a repo with exercises 

```
git clone https://github.com/gsbdarc/yens-onboarding-2025.git 
```

Navigate to the `exercises` directory:

```
cd yens-onboarding-2025/exercises
```
🟩/🟥

## Run scripts from the terminal

💻 Create a Python script:

```
touch test_script.py
```

Edit this file in Jupyter Text File Editor.

The content for `test_script.py`:

```python
print("Hello from the Yens!")
```

Save this 🐍 file. 

💻 Run the script:

```
python3 test_script.py
```

🟩/🟥


## How to run python scripts that import libraries
Let’s look at the script called `extract_form_3_one_file.py` inside the `scripts` directory.

```bash
cat scripts/extract_form_3_one_file.py
```

❓: What is the script doing?


Before we can run this script, every user needs to have packages that the script imports installed. This is true for other languages like R and Julia as well.

  1. You should have a terminal connected to the Yens open or terminal in JupyterHub.

  2. You should be in the `~/yens-onboarding-2025/exercises` directory

  3. Now that we looked at the python script, let's look at the `requirements.txt` file:

```
cat requirements.txt
```

❓ What is `requirements.txt` file?

❓ Why is it useful?


## Access the Yens on the web 
To access JupyterHub, choose any of the following:

- <a href="https://yen1.stanford.edu" target="_blank">`yen1` https://yen1.stanford.edu</a>
- <a href="https://yen2.stanford.edu" target="_blank">`yen2` https://yen2.stanford.edu</a>
- <a href="https://yen3.stanford.edu" target="_blank">`yen3` https://yen3.stanford.edu</a>
- <a href="https://yen4.stanford.edu" target="_blank">`yen4` https://yen4.stanford.edu</a>
- <a href="https://yen5.stanford.edu" target="_blank">`yen5` https://yen5.stanford.edu</a>

Let's navigate by double-clicking on folders to find an image we copied from our local machine. 

> You can double-click on it to view it natively in JupyterHub.
{: .tip }


#### What is a default workflow on the Yens cluster?
1. Perform Development and Testing on JupyterHub in a notebook
2. Generate a script that can be run on the terminal
3. Run the script on the terminal (interactive yen or batch job)


> **You can always type Shift+Enter to run a cell in Jupyter Notebook.**
{: .tip }

Let's start with a super quick demo of Jupyter Notebook.
1. In your home directory create a new notebook called `Test.ipynb`. (Right click to Rename your notebook)
2. Add a code cell with the following content: `import math` (What kernel are you using?)
3. Add a markdown cell with the following title `# Variable declaration `
4. Add a new code cell with the following content: `x = 16`
5. Add a new code cell with the following content: `math.sqrt(x)` 
6. Run the cells (Restart your kernel and run the cells in a different order)

🟩/🟥

## 💻 Create a python virtual environment

Virtual environments allow you to manage dependencies for different projects separately. This is important because different projects may require different versions of libraries, and using virtual environments helps avoid conflicts between them.

Quick demonstration of the need for virtual environments:

1. Open a terminal and ssh into the yens
2. Access JupyterHub and open a terminal there
3. Run the command `which python3` in both terminals. What do you notice?


🟩/🟥


Let’s make a virtual environment from the `requirements.txt` file:

Run the following commands in the `~/yens-onboarding-2025/exercises` directory:

```
/usr/bin/python3 -m venv venv
source venv/bin/activate
```
This runs a script that’s located in the `./venv/bin` directory called `activate`. The `bin` directory doesn’t mean like, a literal bin. It’s short for `bin`ary, things that can be executed as programs, as opposed to data or configuration files.

> You will know the activation was successful when you see `(venv)` at the beginning of your terminal prompt. This indicates that the virtual environment is active.
{: .tip}

Your environment is activated, so now you can install packages using `pip`. Let’s try it.
```
pip install -r requirements.txt
```

These libraries are now installed in *this* environment. You can load the packages while the environment is activated, but it’s not installed for anyone else. Test it out! Try importing `numpy` and `dotenv` in the Jupyter terminal with your virtual environment activated and deactivated. 

> 🐍 For new python users, type `python3` to start a python console then in the console type `import numpy`. What happens when you try to import a package with the virtual environment activated and deactivated?
{: .tip }

🟩/🟥

## 💻 Run python script using virtual environment

Run the `scripts/extract_form_3_one_file.py` script using the virtual env you just made:

```
python scripts/extract_form_3_one_file.py
``` 

❓: What do you see?

🟩/🟥


## 💻 Use your python environment in Jupyter

One of the packages we installed, the `ipykernel` package, provides the tools to connect your environment to Jupyter. We can create a new Jupyter kernel linked to your virtual environment. Replace `<kernel_name>` with a description name for your environment (e.g. `yens-onboarding-env`). Make sure you’re in your active venv when you run this command!

```
python -m ipykernel install --user --name=<kernel_name>
```

In the Jupyter interface, go to your `yens-onboarding-2025/exercises` folder, and start a new notebook. Name it `Test.ipynb`. Change the kernel to `yens-onboarding-env` or whatever your kernel is named.

You should be able to run:

```
import dotenv
```
You can now run code that uses packages from your environment. If you can’t, let’s get help!

🟩/🟥


## Securely using environment variables
Let’s load your OpenAI API key (or any secret) using `dotenv`.

1. 💻 We created a hidden file to store secrets. Let's look at it:

   ```
   cat /scratch/shared/yens-onboarding-2025/.env
   ```

2. 🐍 Load the variable in Python:

   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv('/scratch/shared/yens-onboarding-2025/.env')
   api_key = os.getenv("OPENAI_API_KEY")
   ```

This allows you to use secrets without hardcoding them into scripts. 

## Cluster Resources

![DARC Cluster Resources](assets/images/darc-sep-2024.jpg)

✏️ Interactive Yens

![Sharing is Caring](assets/images/sharing-is-caring.jpeg)

Lets take a look at one of the interactive nodes. There are 5 interactive nodes (yen1-yen5), each with a large number of cores and RAM.

- The Yens **Share** memory across all nodes on Yen Storage.
   That means whenever you save something to your home folder on Yen1, you can access it from Yen2, Yen3, Yen4, or Yen5. Project folders are also shared across all nodes.

! Can put image of yen1 here and progressively zoom out to show all 5 yens and then the whole cluster.

- The interactive Yens **Share** CPU and RAM across all users logged into that node.
   This means that if one user is running a resource-intensive job on an interactive Yen node, it can affect the performance of other users on the same node.

✏️ Yen-Slurm Cluster

The Yen-Slurm has its own set of nodes that are separate from the interactive yens. These nodes are used to run batch jobs that you submit using the Slurm workload manager.

Slurm is a method for managing and scheduling jobs on a cluster. It allows you to submit jobs that can run in the background, request specific resources (like CPU, memory, and time), and manage multiple jobs efficiently.

Everyone **Shares** Yen-Slurm nodes but when you submit a job, you are allocated your own resources for the duration of the job.

- If you ask for 50 CPUs and 200GB of RAM for 24 hours, those resources are yours
- If you ask for 512 CPU and 2TB of RAM for 24 hours, those resources are yours

What is the catch? 


In order to help you get the jobs you need done we offer a variety of slurm `partitions` (queues) that have different limits on resources and time.

- normal: 512 CPUs, 3,000 GB RAM, max 2 days per job (2 hours default)
- long: 50 CPUs, 3,000 GB RAM, max 7 days per job (2 hours default)
- dev: 2 CPUs,  46 GB RAM, max 2 hours per job (1 hour default)
- gpu: 64 CPUs,  250 GB RAM, max 1 day per job (2 hours default)


✏️ Kitchen demo!

I need some volunteers to help me cook a meal.


## 💻 Run a mystery python script

Login to the Yens.

Take a note of which interactive yen (yen[1-5]) you are on. Then, open a new terminal (or second tab if using Jupyter), and connect to the **same** yen.

Now you should have two terminals, both connected to the same interactive yen.

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

Let’s make your first slurm job script. You can do this in JupyterHub using Text Editor.

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


## Summary
You're now ready to:

- Connect and move around the Yens

- Copy data to/from the cluster

- Create and use virtual environments

- Run code from both notebooks and the terminal

- Manage packages and secrets in a reproducible way

- Measure CPU/RAM needs interactively

- Submit your first Slurm job
