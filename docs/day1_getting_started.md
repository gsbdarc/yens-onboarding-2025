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

## Learning goals

By the end of today you will be able to:

- Connect to the Yens via SSH and JupyterHub.
- Navigate the file system using basic shell commands.
- Create and activate Python virtual environments.
- Install and link Jupyter kernels to your custom environment.
- Run code via Python scripts and Jupyter notebooks on the Yens.
- Use environment variables securely (e.g., for API keys).
- Explore paths and reproducibility on shared systems.

---

A legend we will use:

💻: means “use terminal on the Yens”

✏️ : means “we will white board this”

🐍: means "Python script"

❓: question for class. Feel free to shout out the answer

🟩/🟥: means “put up the colored sticky once you finish the exercise / ask for help”


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

🟩/🟥

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


## Access the Yens on the web 
To access JupyterHub, choose any of the following:

- <a href="https://yen1.stanford.edu" target="_blank">`yen1` https://yen1.stanford.edu</a>
- <a href="https://yen2.stanford.edu" target="_blank">`yen2` https://yen2.stanford.edu</a>
- <a href="https://yen3.stanford.edu" target="_blank">`yen3` https://yen3.stanford.edu</a>
- <a href="https://yen4.stanford.edu" target="_blank">`yen4` https://yen4.stanford.edu</a>
- <a href="https://yen5.stanford.edu" target="_blank">`yen5` https://yen5.stanford.edu</a>

Let's navigate by double clicking on folders to find an image we copied from our local machine. 

> You can double click on it to view it natively in JupyterHub.
{: .tip }




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

  1. You should have a terminal connected to the Yens open or terminal in JupyteHub.

  2. You should be in the `~/yens-onboarding-2025/exercises` directory

  3. Now that we looked at the python script, let's look at the `requirements.txt` file:

  ```
  cat requirements.txt
  ```

❓ What is requirements.txt file?

❓ Why is it useful?



## 💻 Create a python virtual environment
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


## Securely Using Environment Variables
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


## Summary
You're now ready to:

- Connect and move around the Yens

- Create and use virtual environments

- Run code from both notebooks and the terminal

- Manage packages and secrets in a reproducible way


