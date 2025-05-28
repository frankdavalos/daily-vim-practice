"""Module for managing lessons and tracking history."""

import os
import json
import random
import shutil
from datetime import datetime
from pathlib import Path

class LessonManager:
    """Manages lesson selection, history, and file operations."""
    
    def __init__(self):
        """Initialize the lesson manager."""
        self.data_dir = Path("data")
        self.lessons_dir = Path("lessons")
        self.rounds_dir = Path("rounds")
        
        self._ensure_directories_exist()
        
        self.history_file = self.data_dir / "history.json"
        # Removed current_round_file attribute
        
        self._load_history()
    
    def _ensure_directories_exist(self):
        """Ensure all required directories exist."""
        for directory in [self.data_dir, self.lessons_dir, self.rounds_dir]:
            directory.mkdir(exist_ok=True)
    
    def _load_history(self):
        """Load lesson history from file."""
        if not self.history_file.exists() or self.history_file.stat().st_size == 0:
            self.history = {"completed": [], "current_round": 1}
            self._save_history()
        else:
            try:
                with open(self.history_file, "r") as f:
                    self.history = json.load(f)
            except json.JSONDecodeError:
                # If the file exists but has invalid JSON, reset with defaults
                self.history = {"completed": [], "current_round": 1}
                self._save_history()
        
        # Removed current_round_file check and creation
    
    def _save_history(self):
        """Save lesson history to file."""
        with open(self.history_file, "w") as f:
            json.dump(self.history, f, indent=2)
        
        # Removed current_round_file update
    
    def get_next_lesson(self, available_lessons):
        """Get the next random lesson that hasn't been completed in this round."""
        if not available_lessons:
            return None
        
        # Filter out lessons that have already been completed in this round
        remaining_lessons = [
            lesson for lesson in available_lessons
            if lesson not in self.history["completed"]
        ]
        
        # If all lessons have been completed, start a new round
        if not remaining_lessons:
            self._start_new_round()
            remaining_lessons = available_lessons
        
        # Select a random lesson from remaining lessons
        if remaining_lessons:
            selected_lesson = random.choice(remaining_lessons)
            self.history["completed"].append(selected_lesson)
            self._save_history()
            return selected_lesson
        
        return None
    
    def _start_new_round(self):
        """Start a new round of lessons."""
        # Move completed lessons to a round directory
        round_number = self.history["current_round"]
        round_dir = self.rounds_dir / f"round_{round_number:02d}"
        round_dir.mkdir(exist_ok=True)
        
        # Move all lessons to the round directory
        for lesson_file in self.lessons_dir.glob("lesson_*.txt"):
            shutil.move(str(lesson_file), str(round_dir / lesson_file.name))
        
        # Update history for new round
        self.history["current_round"] += 1
        self.history["completed"] = []
        self._save_history()
   
    def save_lesson(self, lesson_id, content, is_practice=False):
        """Save a lesson to a file.
        
        Args:
            lesson_id: The lesson identifier
            content: The lesson content
            is_practice: Whether this is a practice session (doesn't affect progress)
            
        Returns:
            The path to the saved lesson file
        """
        # Create a clean lesson identifier for the filename
        clean_id = lesson_id.replace(".", "_")
        
        # For practice sessions, use a different prefix to distinguish them
        if is_practice:
            filename = f"practice_lesson_{clean_id}.txt"
        else:
            filename = f"lesson_{clean_id}.txt"
            
        filepath = self.lessons_dir / filename
        
        with open(filepath, "w") as f:
            f.write(content)
        
        return filepath

    def reset_history(self):
        """Reset the lesson history."""
        self.history = {"completed": [], "current_round": 1}
        self._save_history()
        
        # Clean up lessons directory
        for lesson_file in self.lessons_dir.glob("lesson_*.txt"):
            lesson_file.unlink(missing_ok=True)

    def full_reset(self):
        """Reset history completely and remove all round directories."""
        self.reset_history()  # First do normal reset
        
        # Then remove all round directories
        for round_dir in self.rounds_dir.glob("round_*"):
            if round_dir.is_dir():
                shutil.rmtree(round_dir)
            
    def get_current_round(self):
        """Return the current round number."""
        return self.history["current_round"]