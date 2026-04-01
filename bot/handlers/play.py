import asyncio
from youtube_search import YoutubeSearch
import re

class CommandHandler:
    def __init__(self):
        self.rate_limit = {}  # Dictionary to track command usage per chat
        self.queue = []  # Queue for managing search results

    async def play_command(self, chat_id, query):
        """Handle the /play command"""
        await self.check_rate_limit(chat_id)
        video_info = await self.search_youtube(query)
        if video_info:
            self.queue.append(video_info)
            return f"Added to queue: {video_info['title']}"
        return "No results found."

    async def vplay_command(self, chat_id, url):
        """Handle the /vplay command"""
        await self.check_rate_limit(chat_id)
        video_info = await self.parse_url(url)
        if video_info:
            self.queue.append(video_info)
            return f"Added to queue: {video_info['title']}"
        return "Invalid video URL."

    async def check_rate_limit(self, chat_id):
        """Check if command usage is within allowed limits"""
        if chat_id in self.rate_limit:
            if self.rate_limit[chat_id] >= 5:  # Limit to 5 commands per minute
                raise Exception("Rate limit exceeded. Try again later.")
            else:
                self.rate_limit[chat_id] += 1
        else:
            self.rate_limit[chat_id] = 1
        await asyncio.sleep(60)  # Reset rate limit after a minute

    async def search_youtube(self, query):
        """Perform a YouTube search and return video information"""
        results = await YoutubeSearch(query, max_results=1).next()
        return results[0] if results else None

    async def parse_url(self, url):
        """Validate and extract video information from a URL"""
        if re.match(r'https?://(www\.)?(youtube\.com|youtu\.?be)/.+', url):
            video_id = url.split('v=')[-1]
            return {'title': 'Sample Video', 'id': video_id}  # Placeholder
        return None


# Example of how to use CommandHandler
# handler = CommandHandler()
# result = await handler.play_command(chat_id='12345', query='example search')
# print(result)