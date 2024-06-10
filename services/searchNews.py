import os
import re
from exa_py import Exa
from dotenv import load_dotenv


load_dotenv()


class SearchNews:
    def __init__(self) -> None:
        self.exa = Exa(api_key=os.environ.get('EXA_API_KEY'))


    def parse_source(self, url: str):
        # Regular expression to extract the website name between "www." and the next "/"
        match = re.search(r'www\.(.*?)\.', url)
        if match:
            return match.group(1)
        else:
            return None

    def clean_response(self, search_results: list):
        results = []

        for res in search_results:
            if len(res.text) < 100:
                print(f'Skipped {res.url} with text \n {res.text}')
                continue
            
            results.append({
                'title': res.title,
                'url': res.url,
                'source': self.parse_source(res.url),
                'author': res.author,
                'score': res.score,
                'text': res.text
            })

        return results
    
    def run(self, query: str, date_cutoff: str, num_results: int):
        search_response = self.exa.search_and_contents(
          query,
          use_autoprompt=True,
          num_results=num_results,
          start_published_date=date_cutoff
        )

        results = self.clean_response(search_response.results)

        return results