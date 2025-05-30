# Vim Daily

A Python tool to help practice Vim skills through daily lessons extracted from vimtutor.

## Overview

Vim Daily gives you a structured way to learn Vim commands by serving up one lesson from vimtutor with each run. It tracks your progress and ensures you don't see the same lesson twice until you've completed all lessons.

## Installation

Clone this repository and install the package:

```bash
git clone https://github.com/frankdavalos/daily-vim-practice.git
cd daily-vim-practice
# Optional: Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Install dependencies (if any)
pip install -r requirements.txt
```

## Usage

Run the main script to get a daily lesson:

```bash
python -m vim_daily.main
```

The program will:
1. Extract a random lesson from vimtutor
2. Save it to the lessons directory
3. Tell you which lesson to open and practice

### Reset Progress

To reset your lesson history and start a new round:

```bash
python -m vim_daily.main --reset
```

This resets your progress tracking but preserves your round history directories.

For a complete reset that also removes all round history:

```bash
python -m vim_daily.main --full-reset
```

### Track Your Progress

To see your current progress and which lessons you've completed:

```bash
python -m vim_daily.main --progress
```

This will show:
- Your current round number
- How many lessons you've completed
- Which specific lessons you've completed
- How many lessons remain

### List Available Lessons

To see all available lessons in the vimtutor:

```bash
python -m vim_daily.main --list
```

This will display all lessons organized by chapter, making it easy to see what content is available.

### Practice Specific Lessons

To practice a specific lesson without affecting your normal progression:

```bash
python -m vim_daily.main --specific 1.2
```

This allows you to revisit any lesson at any time for additional practice. Practice sessions won't count toward your lesson completion progress.

## Project Structure

- `vim_daily/`: Main package code
- `data/`: Stores history and tracking files
- `lessons/`: Contains current lesson files
- `rounds/`: Archives completed rounds of lessons

## How Rounds Work

1. Each time you run the program, you get a new lesson that you haven't seen in the current round
2. Once you've seen all lessons, a new round begins
3. Completed lessons from previous rounds are stored in the `rounds/` directory
