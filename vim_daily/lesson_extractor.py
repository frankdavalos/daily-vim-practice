"""Module for extracting lessons from vimtutor."""

import os
import subprocess
import re
import tempfile
from pathlib import Path

class LessonExtractor:
    """Extracts individual lessons from vimtutor."""
    
    def __init__(self):
        """Initialize the lesson extractor."""
        self.vimtutor_content = self._get_vimtutor_content()
        self.lessons = self._identify_lessons()
    
    def _get_vimtutor_content(self):
        """Get the content of vimtutor from the static file."""
        static_file = Path("data/vimtutor.txt")
        
        try:
            with open(static_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
                return content
        except Exception as e:
            print(f"Error reading vimtutor.txt file: {e}")
            print(f"Please ensure {static_file.absolute()} exists and is readable")
            return "ERROR: Could not read vimtutor content from the static file."
    
    def _identify_lessons(self):
        """Identify all lessons in vimtutor content."""
        # This regex looks for lesson headers like "Lesson 1.1", "Lesson 2.3", etc.
        lesson_pattern = re.compile(r'(?:^|\n)\s*(?:Lesson|LESSON)\s+(\d+\.\d+)', re.IGNORECASE)
        matches = lesson_pattern.finditer(self.vimtutor_content)
        
        lessons = []
        for match in matches:
            lesson_id = match.group(1)
            if lesson_id not in lessons:  # Avoid duplicates
                lessons.append(lesson_id)
        
        return sorted(lessons, key=lambda x: float(x))
    
    def extract_lesson(self, lesson_id):
        """Extract a specific lesson from vimtutor."""
        if not self.lessons:
            return "No lessons found in vimtutor content."
        
        # Find the index of the requested lesson
        try:
            index = self.lessons.index(lesson_id)
        except ValueError:
            return f"Lesson {lesson_id} not found"
        
        # Determine the start pattern for this lesson
        start_pattern = re.compile(f'(?:^|\n)\s*(?:Lesson|LESSON)\s+{re.escape(lesson_id)}', re.IGNORECASE)
        
        # Determine the end pattern (next lesson or end of file)
        if index < len(self.lessons) - 1:
            next_lesson = self.lessons[index + 1]
            end_pattern = re.compile(f'(?:^|\n)\s*(?:Lesson|LESSON)\s+{re.escape(next_lesson)}', re.IGNORECASE)
        else:
            end_pattern = None
        
        # Find the start position
        start_match = start_pattern.search(self.vimtutor_content)
        if not start_match:
            return f"Lesson {lesson_id} not found in content"
        
        start_pos = start_match.start()
        
        # Find the end position
        if end_pattern:
            end_match = end_pattern.search(self.vimtutor_content)
            end_pos = end_match.start() if end_match else len(self.vimtutor_content)
        else:
            end_pos = len(self.vimtutor_content)
        
        # Extract the lesson content
        lesson_content = self.vimtutor_content[start_pos:end_pos]
        
        # Add a header with lesson information
        header = f"# Vim Daily - Lesson {lesson_id}\n\n"
        return header + lesson_content
    
    def get_available_lessons(self):
        """Return all available lesson IDs."""
        return self.lessons