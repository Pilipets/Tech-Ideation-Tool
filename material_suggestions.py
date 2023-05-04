import arxiv
import requests
from dateutil.parser import parse
import openai
from transformers import pipeline
from gnews import GNews
import os


openai.api_key = open(os.path.join('keys', 'open_ai.key')).read()
MAX_RESULTS = 5


def arxiv_sample(query='quantum'):
	print('arxiv_sample')
	search = arxiv.Search(
		query = query,
		max_results = MAX_RESULTS,
		sort_by = arxiv.SortCriterion.SubmittedDate
	)

	ret = []
	for result in search.results():
		ret.append({'title':result.title, 'published':result.published, 'link':result.entry_id, 'summary':result.summary})
	return ret


def patents_view_sample(query='electric car'):
	print('patents_view_sample')
	url = "https://api.patentsview.org/patents/query"

	# Set the parameters for the API request
	params = {
		"q": '{"_text_any":{"patent_abstract":"%s"}}' % query,
		"f": '["patent_title", "patent_date", "patent_abstract", "patent_number"]',
		"o": '{"per_page": %d}' % MAX_RESULTS,
		"s": '[{"patent_date":"desc"}]', 
	}

	response = requests.get(url, params=params)

	if response.status_code == 200:
		data = response.json()
		results = data.get('patents', [])

		ret = []
		for patent in results:
			ret.append({
				'title':patent.get('patent_title', 'Not Found'),
				'date':patent.get('patent_date', 'Not Found'),
				'number':patent.get('patent_number', 'Not Found'),
				'summary':patent.get('patent_abstract', 'Not Found')
			})
		return ret
	else:
		raise f"Error fetching data from PatentsView API: {response.status_code}"


def arxiv_explorer_sample(query = 'trying something unusual'):
	print('arxiv_explorer_sample')
	url = 'https://us-west1-semanticxplorer.cloudfunctions.net/semantic-xplorer-db'

	resp = requests.get(url, params={'query': query})

	elems = []
	for el in resp.json():
		url = 'https://arxiv.org/abs/' + el['id']
		el = el['metadata']
		elems.append({'title': el['title'], 'date': parse(el['date']), 'url': url, 'abstract': el['abstract']})

	elems.sort(key=lambda el: el['date'], reverse=True)

	elems = elems[:MAX_RESULTS]
	return elems


def chatgpt_sample(query='trying something unusual'):
	print('chatgpt_sample')

	def generate_ideas(prompt):
		prompts = [prompt for _ in range(MAX_RESULTS)]
		response = openai.Completion.create(
			engine="text-davinci-003",
			prompt=prompts,
			max_tokens=500,
			stop=None,
			temperature=0.5,
		)

		ideas = [choice.text.strip() for choice in response.choices]
		return ideas

	prompt = "Generate idea or fact or insight related to '%s' that can be useful for tech-startup" % (query)
	ret = generate_ideas(prompt)
	return ret


def hugging_face_sample(query = 'climate change'):
	print('hugging_face_sample')

	generator = pipeline('text-generation', model = 'gpt2')
	results = generator("New idea/fact/insight related to the %s is" % query, max_length = 200, num_return_sequences=MAX_RESULTS)

	ideas = [r['generated_text'].replace('\n\n', '\n') for r in results]
	return ideas


def google_news_sample(query = 'distributed databases'):
	print('google_news_sample')
	google_news = GNews()

	google_news.max_results = MAX_RESULTS

	news = google_news.get_news(query)
	ret = []

	for new in news:
		ret.append({
			'title':new['title'], 'date':new['published date'],
			'description':new['description'], 'url':new['url']}
		)
	return ret


def main():
	print(arxiv_sample())
	print(arxiv_explorer_sample())
	print(patents_view_sample())
	print(chatgpt_sample())
	print(hugging_face_sample())
	print(google_news_sample())


if __name__ == '__main__':
	main()