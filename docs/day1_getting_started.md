---
title: Day 1 — Getting Started on the Yens Cluster
layout: page
nav_order: 1
---

# {{ page.title }}

## Overview

This first session introduces you to Stanford GSB’s research computing cluster — the Yens. You’ll learn how to log in, navigate the file system, set up reproducible Python environments, and run code interactively on the cluster or through JupyterHub.

> 🔗 **Need help?** Visit [rcpedia.stanford.edu](https://rcpedia.stanford.edu/) or reach out via the [GSB DARC Slack](https://app.slack.com/client/E7SAV7LAD/C01JXJ6U4E5).

---

## Learning Goals

By the end of today you will be able to:

- Connect to the Yens via SSH and JupyterHub.
- Navigate the file system using basic shell commands.
- Create and activate Python virtual environments.
- Run code via Python scripts and Jupyter notebooks on the Yens.
- Use environment variables securely (e.g., for API keys).
- Install and link Jupyter kernels to your custom environment.

---

## Part 1: Connecting to the Yens
{: .important} If you are a Mac or Linux user, you can use the native terminal for these exercises.

{: .important} If you are a Windows user, you can use Git Bash to run these commands.


To SSH from your terminal (replace `<SUNetID>`):

```bash
ssh <SUNetID>@yen.stanford.edu
```
You’ll be prompted for Duo authentication.


### Command Line Basics

Explore your environment

```
pwd                   # Show your current directory
ls -lah               # List files, including hidden ones
cd /scratch/shared    # Change directories
cd                    # Go back to your home directory
mkdir new_dir         # Make a new folder
touch test.py         # Create a blank file
rm test.py            # Be careful! This deletes the file
```

Try uploading a file from your laptop to the cluster using scp (run from your local terminal):

```
scp path/to/file.txt <SUNetID>@yen.stanford.edu:~
```
You’ll be prompted for Duo authentication.

## Part 2: Web-based Computing 
To access JupyterHub, choose any of the following:

- <a href="https://yen1.stanford.edu" target="_blank">`yen1` https://yen1.stanford.edu</a>
- <a href="https://yen2.stanford.edu" target="_blank">`yen2` https://yen2.stanford.edu</a>
- <a href="https://yen3.stanford.edu" target="_blank">`yen3` https://yen3.stanford.edu</a>
- <a href="https://yen4.stanford.edu" target="_blank">`yen4` https://yen4.stanford.edu</a>
- <a href="https://yen5.stanford.edu" target="_blank">`yen5` https://yen5.stanford.edu</a>

## Part 3: Create a Python Virtual Environment
  1. Connect to the Yens either via a terminal in JupyterHub or via SSH.

  2. Clone the repo and change directories into it on the Yens:
    ```
    git clone https://github.com/gsbdarc/yens-onboarding-2025.git
    cd yens-onboarding-2025/exercises
    ``` 

  -❓ What is requirements.txt file?

  -❓ Why is it useful?

### Exercise 1: Create and activate a virtual environment
Let’s make a virtual environment from requirements.txt:
```
/usr/bin/python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Exercise 2: Run python script
Let’s look at the script called `extract_form_3_one_file.py` inside the `scripts` directory.

-❓: What is the script doing?

- Run it using the virtual env you just made

- ❓: What do you see?


