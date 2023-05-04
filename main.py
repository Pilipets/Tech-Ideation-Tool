from flask import Flask, request, jsonify
from flask_cors import CORS

import material_suggestions, text_suggestions
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

@app.route('/search')
def search():
    query = request.args.get('q')
    arxiv = request.args.get('arxiv')
    news = request.args.get('news')
    patents = request.args.get('patents')
    openai = request.args.get('openai')
    ai_free = request.args.get('ai_free')

    results_num = 100

    if query is None:
        query = 'no code development'

    results = []
    if arxiv == 'true':
        try:
            ret = material_suggestions.arxiv_sample(query)

            for r in ret:
                main_info = r.pop('title')
                results.append({'type':'ARXIV', 'main_info':main_info, 'details':r})
        except Exception as ex:
            logging.warning('Error getting arxiv: {}'.format(ex))

    if arxiv == 'true':
        try:
            ret = material_suggestions.arxiv_explorer_sample(query)

            for r in ret:
                main_info = r.pop('title')
                results.append({'type':'ARXIV', 'main_info':main_info, 'details':r})
        except Exception as ex:
            logging.warning('Error getting arxiv_explorer: {}'.format(ex))

    if news == 'true':
        try:
            ret = material_suggestions.google_news_sample(query)

            for r in ret:
                main_info = r.pop('title')
                results.append({'type':'NEWS', 'main_info':main_info, 'details':r})
        except Exception as ex:
            logging.warning('Error getting google_news: {}'.format(ex))

    if patents == 'true':
        try:
            ret = material_suggestions.patents_view_sample(query)

            for r in ret:
                main_info = r.pop('title')
                results.append({'type':'PATENTS', 'main_info':main_info, 'details':r})
        except Exception as ex:
            logging.warning('Error getting google_news: {}'.format(ex))

    if openai == 'true':
        try:
            ret = material_suggestions.chatgpt_sample(query)

            for r in ret:
                results.append({'type':'OpenAI', 'main_info':r})
        except Exception as ex:
            logging.warning('Error getting chatgpt: {}'.format(ex))

    if ai_free == 'true':
        try:
            ret = material_suggestions.hugging_face_sample(query)

            for r in ret:
                results.append({'type':'AI-free', 'main_info':r})
        except Exception as ex:
            logging.warning('Error getting hugging_face: {}'.format(ex))

    return jsonify({"results": results})

if __name__ == '__main__':
    app.run()
