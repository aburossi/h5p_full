from youtube_transcript_api import YouTubeTranscriptApi
import logging

logger = logging.getLogger(__name__)

class YouTubeTranscriber:
    def __init__(self):
        # Configure phrases you wish to remove from the transcript
        self.youtube_transcriber_config = {
            'remove_phrases': ['[music]']
        }
    
    def extract_video_id(self, url: str) -> str:
        if "v=" in url:
            return url.split("v=")[-1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[-1].split("?")[0]
        else:
            return None
    
    def extract_transcript(self, url: str) -> str:
        """
        Extracts and cleans the transcript from the given YouTube URL.
        It first attempts to fetch a manually created transcript (original language).
        If unavailable, it falls back to the auto-generated transcript.
        """
        try:
            video_id = self.extract_video_id(url)
            if not video_id:
                raise ValueError("Invalid YouTube URL format.")
            
            # List all available transcripts for the video
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Attempt to get a manually created transcript (usually in the original language)
            transcript = None
            for t in transcript_list:
                if not t.is_generated:
                    transcript = t.fetch()
                    break
            
            # If no manually created transcript is available, fetch an auto-generated one
            if transcript is None:
                # Build a list of available language codes from the transcript list
                language_codes = [t.language_code for t in transcript_list]
                transcript = transcript_list.find_generated_transcript(language_codes).fetch()
            
            # Clean the transcript by removing any unwanted phrases
            cleaned_transcript = " ".join([
                entry['text']
                for entry in transcript
                if entry['text'].lower() not in [phrase.lower() for phrase in self.youtube_transcriber_config['remove_phrases']]
            ])
            return cleaned_transcript
        except Exception as e:
            logger.error(f"Error extracting YouTube transcript: {str(e)}")
            raise
