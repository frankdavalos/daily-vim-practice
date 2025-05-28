"""Utility functions for Vim Daily."""

import os
import subprocess
from pathlib import Path

def check_vim_installed():
    """Check if Vim is installed."""
    try:
        subprocess.run(["vim", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def check_neovim_installed():
    """Check if Neovim is installed."""
    try:
        subprocess.run(["nvim", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def get_vim_version():
    """Get the installed Vim version."""
    try:
        result = subprocess.run(
            ["vim", "--version"], 
            capture_output=True, 
            text=True,
            check=True
        )
        version_line = result.stdout.splitlines()[0]
        return version_line
    except (subprocess.SubprocessError, FileNotFoundError):
        return "Vim not found"

def get_vim_runtime_path():
    """Try to find the Vim runtime path."""
    try:
        result = subprocess.run(
            ["vim", "-e", "-T", "dumb", "-c", "echom $VIMRUNTIME", "-c", "quit"],
            capture_output=True,
            text=True,
            check=True
        )
        # Parse the output to find the path
        for line in result.stderr.splitlines():
            if line and not line.startswith(":"):
                return line.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    return None