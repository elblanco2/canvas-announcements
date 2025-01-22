import requests
from typing import List
from pathlib import Path
from datetime import datetime
import webbrowser

class CanvasAnnouncement:
   def __init__(self):
       self.base_url = None
       self.token = None 
       self.headers = None
       self.downloads_path = Path.home() / "Downloads"
       self.html_template = '''
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; color: #333;">
   <div style="background-color: #ffe5b4; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
       <h1 style="color: #1a365d; margin: 0 0 10px 0;">{title}</h1>
   </div>

   {video_section}

   {announcements_section}

   {notes_section}
</div>'''

       self.video_section_template = '''
   <div style="background: white; padding: 20px; margin-bottom: 20px; border: 1px solid #e1e1e1; border-radius: 8px;">
       <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin: 20px 0;">
           {video_content}
       </div>
   </div>'''

       self.announcements_section_template = '''
   <div style="background: white; padding: 20px; margin-bottom: 20px; border: 1px solid #e1e1e1; border-radius: 8px;">
       <h2 style="color: #2c5282; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">General Announcements</h2>
       <ul style="padding-left: 20px;">
           {announcements}
       </ul>
   </div>'''

       self.notes_section_template = '''
   <div style="background-color: #fffbeb; padding: 15px; border-radius: 8px; margin-top: 20px;">
       <h2 style="color: #2c5282; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">Important Notes</h2>
       <p>{notes}</p>
   </div>'''

   def setup(self):
       """Get Canvas URL and API token from user."""
       self.base_url = input("Enter Canvas URL (e.g., https://college.instructure.com): ").strip()
       if not self.base_url.startswith('http'):
           self.base_url = 'https://' + self.base_url
       self.base_url = f"{self.base_url.rstrip('/')}/api/v1"
       
       self.token = input("Enter your Canvas API token: ").strip()
       self.headers = {
           "Authorization": f"Bearer {self.token}",
           "Content-Type": "application/json"
       }

   def get_course_ids(self) -> List[str]:
       """Get course IDs from user."""
       courses = []
       while True:
           course_id = input("\nEnter course ID (or press Enter to finish): ").strip()
           if not course_id:
               break
           if course_id.isdigit():
               courses.append(course_id)
           else:
               print("Invalid course ID. Please enter a number.")
       return courses

   def get_announcement_content(self):
       """Get content for each section of the announcement."""
       print("\nEnter announcement details:")
       title = input("Announcement Title: ").strip()
       self.announcement_title = title  # Store title for later use
       
       # Video section
       print("\nFor video embed, enter the video URL (or 'none' to skip)")
       print("Example format: https://www.kanopy.com/en/mdc/video/313379")
       video_url = input("Video URL: ").strip()
       
       if video_url.lower() != 'none':
           video_embed = f"<iframe style='position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;' allow='encrypted-media;' src='{video_url.replace('/video/', '/embed/video/')}' frameborder='0' allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe>"
           video_section = self.video_section_template.format(video_content=video_embed)
       else:
           video_section = ''
       
       # Announcements section
       print("\nEnter general announcements (one per line, press Enter twice to finish):")
       announcements = []
       while True:
           line = input().strip()
           if not line:
               break
           announcements.append(f"<li style='margin-bottom: 8px;'>{line}</li>")
       announcements_section = self.announcements_section_template.format(
           announcements='\n            '.join(announcements)
       ) if announcements else ''
       
       # Notes section
       notes = input("\nEnter important notes (or 'none' to skip): ").strip()
       notes_section = self.notes_section_template.format(
           notes=notes
       ) if notes.lower() != 'none' else ''
       
       return self.html_template.format(
           title=title,
           video_section=video_section,
           announcements_section=announcements_section,
           notes_section=notes_section
       )

   def save_announcement(self, content: str) -> str:
       """Save announcement HTML to Downloads folder."""
       timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
       filename = f"{self.announcement_title}_{timestamp}.html"
       filepath = self.downloads_path / filename
       
       try:
           filepath.write_text(content, encoding='utf-8')
           return str(filepath)
       except Exception as e:
           print(f"Error saving file: {e}")
           return None

   def post_announcement(self, course_ids: List[str], content: str) -> None:
       """Post announcement to specified courses."""
       for course_id in course_ids:
           try:
               response = requests.post(
                   f"{self.base_url}/courses/{course_id}/discussion_topics",
                   headers=self.headers,
                   json={
                       "title": self.announcement_title,
                       "message": content,
                       "is_announcement": True,
                       "published": True
                   }
               )
               response.raise_for_status()
               print(f"Announcement posted successfully to course {course_id}")
               
           except requests.RequestException as e:
               print(f"Error posting to course {course_id}: {e}")

   def post_with_confirmation(self, course_ids: List[str], content: str) -> None:
       """Save announcement, preview it, and post after confirmation."""
       saved_path = self.save_announcement(content)
       if saved_path:
           print(f"\nAnnouncement saved to: {saved_path}")
           webbrowser.open(f"file://{saved_path}")
           
           confirm = input("\nWould you like to post this announcement? (y/n): ").lower()
           if confirm == 'y':
               self.post_announcement(course_ids, content)
           else:
               print("Announcement not posted. HTML file is still saved locally.")

def main():
   print("\n=== Canvas Announcement Poster ===\n")
   
   announcer = CanvasAnnouncement()
   announcer.setup()
   
   course_ids = announcer.get_course_ids()
   if not course_ids:
       print("No courses selected. Exiting.")
       return
   
   content = announcer.get_announcement_content()
   announcer.post_with_confirmation(course_ids, content)
   print("\nProcess complete!")

if __name__ == "__main__":
   try:
       main()
   except KeyboardInterrupt:
       print("\n\nProgram terminated by user.")
