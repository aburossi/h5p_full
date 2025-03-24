from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
import logging

logger = logging.getLogger(__name__)

class YouTubeTranscriber:
    def __init__(self):
        # Configure phrases to remove (case-insensitive)
        self.youtube_transcriber_config = {
            'remove_phrases': ['[music]']
        }
        # Initialize the YouTubeTranscriptApi with Webshare proxy credentials
        self.ytt_api = YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
                proxy_username="qxgfpukp",
                proxy_password="jm9du9nupv3x"
            )
        )
    
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
        It first attempts to fetch a manually created transcript (usually in the original language).
        If unavailable, it falls back to an auto-generated transcript.
        """
        try:
            video_id = self.extract_video_id(url)
            if not video_id:
                raise ValueError("Invalid YouTube URL format.")
            
            # List all available transcripts for the video using the proxy-configured API
            transcript_list = self.ytt_api.list_transcripts(video_id)
            
            # Attempt to get a manually created transcript (original language)
            transcript = None
            for t in transcript_list:
                if not t.is_generated:
                    transcript = t.fetch()
                    break
            
            # If no manually created transcript is available, fetch an auto-generated one
            if transcript is None:
                # Get a list of all available language codes and fetch the generated transcript
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

if __name__ == "__main__":
    # For testing purposes
    sample_url = "https://www.youtube.com/watch?v=BO1bjSmN8rM"
    transcriber = YouTubeTranscriber()
    try:
        transcript = transcriber.extract_transcript(sample_url)
        print("Transcript fetched successfully:")
        print(transcript[:500] + "..." if len(transcript) > 500 else transcript)
    except Exception as e:
        print(f"An error occurred: {e}")
