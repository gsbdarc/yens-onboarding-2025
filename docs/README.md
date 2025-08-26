---
layout: home
title:  Yens Onboarding -- Fall 2025
nav_exclude: true
permalink: /:path/
seo:
  type: Course
  name: Yens Onboarding -- Fall 2025
updateDate: 2025-07-28
---
# {{ page.title }}

Welcome! This two-session onboarding will get you productive on Stanford GSB’s research computing cluster—the **Yens**—and ready to run real research workflows at scale.

---

## Course objectives
By the end of the course, you will be able to:
- Connect to the Yens via SSH and JupyterHub, navigate the filesystem, and move files to/from the cluster.
- Create and use a **reproducible Python environment**, install packages, and register a Jupyter kernel.
- Submit, monitor, and debug **Slurm** jobs; choose CPU/RAM/time resources; and read job logs.
- Scale workloads with **fault tolerance** (checkpoint/resume) and **Slurm arrays** for parallelism.

---

## Overview of topics

### Day 1 — Getting started (interactive use)
- SSH & JupyterHub access; basic shell; copying data with `scp`.
- Clone the course repo; run scripts from the terminal.
- Create/activate a **virtual environment**, install from `requirements.txt`, and expose your env to Jupyter.
- Securely use environment variables with `dotenv`.
- **Motivation exercise:** run a “mystery” Python script interactively, watch CPU/RAM/time with `htop`, `userload`, and `time`.
- **Your first Slurm job** (hello-world) to close Day 1.

### Day 2 — Running and scaling jobs
- Running real scripts with Slurm: working directories, logs, monitoring with `squeue`, canceling jobs.
- **Debugging lab:** fix common broken Slurm scripts and learn a systematic log-first workflow.
- Handling resource failures (out-of-memory, time limits) and how to size jobs.
- **Fault tolerance:** run a checkpointed batch job that saves progress and resumes after fixes.
- **Scaling up:** Slurm arrays to run many tasks in parallel; per-task outputs and follow-up consolidation.
- Sharing results off-cluster and communicating your workflow (README updates).

---

## Expectations

### What we assume
- You’ve done *some* programming (Python preferred). If not, tell us and we’ll get you unstuck.
- You can bring a laptop with Duo for Stanford login and a modern browser.

### What to do during class
- Work through each hands-on step in order; put up 🟩 when done, 🟥 for help (we’ll circulate).
- Ask questions out loud—especially when something fails. We’ll use failures to practice debugging.

### Setup you’ll complete in class
- SSH/JupyterHub access and file transfer.
- Local repo clone and a working **venv** linked to Jupyter.
- A first Slurm submission on Day 1; full Slurm workflow on Day 2.

---

## How the course is run
- **Format:** short demos → guided hands-on exercises → quick recaps.
- **Timing:** Two sessions of ~2:45 each (including breaks), with clearly scoped exercises and checkpoints aligned to the Day 1/Day 2 pages.
- **Materials:** All commands and scripts live in the course repo you’ll clone on Day 1.

---

## Support & resources
- Need help beyond class? Check **RCPedia** and reach us on Slack.

### Contact us
- Join the **#gsb-yen-users** Slack channel to ask/answer questions and see workshop announcements.  
  If the link fails, open Slack and search for **#gsb-yen-users**.
- Email: [gsb_darcresearch@stanford.edu](mailto:gsb_darcresearch@stanford.edu)

---

## The DARC Team
<div style="display: flex; justify-content: center; gap: 10px;">
  <img src="/assets/images/darc.jpg" alt="DARC Team September 2024" style="width:48%; border-radius:8px;" />
  <img src="/assets/images/yo-darc-team.jpg" alt="DARC Team at Art Museum" style="width:48%; border-radius:8px;" />
</div>
