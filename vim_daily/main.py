"""Main entry point for the Vim Daily application."""

import argparse
import re
from pathlib import Path
from vim_daily.lesson_manager import LessonManager
from vim_daily.lesson_extractor import LessonExtractor

def main():
    """Run the Vim Daily application."""
    parser = argparse.ArgumentParser(description="Get a daily Vim lesson.")
    parser.add_argument("--reset", action="store_true", help="Reset the lesson history")
    parser.add_argument("--full-reset", action="store_true", help="Reset history and remove all round directories")
    parser.add_argument("--cleanup", action="store_true", help="Remove all practice files")
    parser.add_argument("--progress", action="store_true", help="Show your current progress")
    parser.add_argument("--list", action="store_true", help="List all available lessons")
    parser.add_argument("--specific", help="Practice a specific lesson (e.g., '1.2') without affecting your progress")
    args = parser.parse_args()
    
    extractor = LessonExtractor()
    manager = LessonManager()
    
    if args.reset:
        manager.reset_history()
        print("Lesson history has been reset.")
        return

    if args.full_reset:
        manager.full_reset()  # Reset history and remove all round directories
        print("All history and round directories have been completely reset.")
        return

    if args.cleanup:
        cleanup_count = 0
        for practice_file in Path("lessons").glob("practice_lesson_*.txt"):
            practice_file.unlink()
            cleanup_count += 1
        print(f"Cleaned up {cleanup_count} practice files.")
        return
    
    if args.progress:
        show_progress(manager, extractor)
        return
    
    if args.list:
        list_lessons(extractor)
        return
    
    if args.specific:
        # Check if the requested lesson exists
        all_lessons = extractor.get_available_lessons()
        if args.specific in all_lessons:
            content = extractor.extract_lesson(args.specific)
            filepath = manager.save_lesson(args.specific, content, is_practice=True)
            
            print(f"Practice lesson {args.specific} is ready: {filepath}")
            print(f"Open it with: vim {filepath}")
            print(f"Note: This practice session won't affect your regular progress.")
            return
        else:
            print(f"Lesson {args.specific} not found. Use --list to see available lessons.")
            return
    
    # Get next lesson
    lesson = manager.get_next_lesson(extractor.get_available_lessons())
    if lesson:
        content = extractor.extract_lesson(lesson)
        filepath = manager.save_lesson(lesson, content)
        print(f"Your daily Vim lesson is ready: {filepath}")
        print(f"Open it with: vim {filepath}")
        print(f"This is lesson {lesson} in round {manager.get_current_round()}")
    else:
        print("No lessons available. All lessons may have been completed.")

def show_progress(manager, extractor):
    """Show the user's current progress."""
    all_lessons = extractor.get_available_lessons()
    completed = manager.history["completed"]
    remaining = [l for l in all_lessons if l not in completed]
    
    print(f"Current round: {manager.get_current_round()}")
    print(f"Lessons completed this round: {len(completed)}/{len(all_lessons)} ({len(completed)/len(all_lessons)*100:.1f}%)")
    print(f"Lessons remaining: {len(remaining)}")
    
    if completed:
        print("\nLessons completed this round:")
        for lesson in sorted(completed, key=lambda x: float(x)):
            print(f"  - Lesson {lesson}")

def list_lessons(extractor):
    """List all available lessons with their titles."""
    # Modified regex to capture both lesson number and title
    lesson_pattern = re.compile(r'(?:^|\n)\s*(?:Lesson|LESSON)\s+(\d+\.\d+):\s+(.*?)(?:\n|$)', re.IGNORECASE)
    matches = lesson_pattern.finditer(extractor.vimtutor_content)
    
    lessons_with_titles = {}
    for match in matches:
        lesson_id = match.group(1)
        title = match.group(2).strip()
        lessons_with_titles[lesson_id] = title
    
    print(f"Found {len(lessons_with_titles)} lessons in vimtutor:")
    
    # Group lessons by chapter
    chapters = {}
    for lesson_id in sorted(lessons_with_titles.keys(), key=lambda x: float(x)):
        chapter = lesson_id.split('.')[0]
        if chapter not in chapters:
            chapters[chapter] = []
        chapters[chapter].append(lesson_id)
    
    # Print lessons organized by chapter with titles
    for chapter in sorted(chapters.keys(), key=int):
        print(f"\nChapter {chapter}:")
        for lesson_id in sorted(chapters[chapter], key=lambda x: float(x)):
            title = lessons_with_titles.get(lesson_id, "")
            print(f"  - Lesson {lesson_id}: {title}")

if __name__ == "__main__":
    main()