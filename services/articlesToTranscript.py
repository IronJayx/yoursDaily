import os
from clients.llmClient import llmClient
from loguru import logger

SystemPrompts = {
    "0": (
        "You are: yoursDaily, a podcast channel delivering a personalised recap of recent news to your auditors. "
        "Your job is to write the podcast transcript. "
        "You will be given articles that have been cherry picked because they are relevant to the auditor interests."
        "You should base he podcatst on the articles provided."
        "Additionaly follow the following guidelines:"
        "- ADAPT your writing style for news podcast format, pay attention to key elements like: hooks, rhythm, diction, choice of words."
        "Start the podacast with an original hook of one sentence related to a news."
        "After this first hook, remind the name of the podcast directly addressing the listener with something like: Welcome to yoursDaily, your daily podcast covering yesterday's news, let's dive in ..."
        "Be creative in how you introduce each news, include adjectives and vary sentence structures. A/an/the {adjective} {event} in/from/.. {place mentionned/celebrity...} {author name} and the {journal name} brings to us an astonishing story about ...."
        "After the introduction, when you introduce each piece of news follow a structure similar to this: "
        "Choose your wording to match the intonation of a podcaster. "
        "DON'T include titles or bullet points in your summary. "
        "DON'T include anything else other than the podcast transcript. "
        "DONT repeat information, IF several news talk about the same topic mention them together and feel free to discard redundant news articles."
    )
}

class TranscriptWriter:
    hard_token_limit = 12000

    def __init__(self, prompt_version="0", top_k: int = 3):
        self.outbound_dir = "data/transcripts"

        self.system_prompt = SystemPrompts.get(prompt_version)
        self.version = prompt_version
        self.top_k = top_k

        self.llm_client = llmClient()

        if not os.path.exists(self.outbound_dir):
            os.makedirs(self.outbound_dir)


    def write_transcript(self, articles: list, preferences: str, length: int):
        self.llm_client.add_message(self.system_prompt)
        message_text = f"You are writing a podcast transcript for someone interested in {preferences}.\n Here is some piece of news he/she might be interested in: "
        
        for i, article in enumerate(articles):
            source = article.get('source', 'Unknown source')
            author = article.get('author', 'Unknown source')
            title = article.get('title', 'Unknown source')
            text = article.get('text', '')
            message_text += f"Here is the an article from {source} by {author}: {title} - {text}\n"
        
        self.llm_client.add_message(message_text[:self.hard_token_limit], role="user")
        
        # Send the message list to the LLM client
        response = self.llm_client.answer(max_length=length)
        return response


    def run(self, articles: list, user_preferences: str, length=int):        

        if len(articles) == 0:
            return logger.error('No match found')

        transcript = self.write_transcript(
            articles=articles,
            preferences=user_preferences,
            length=length
        ).replace('\n', ' ')

        return transcript
