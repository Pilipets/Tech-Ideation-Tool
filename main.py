from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_caching import Cache

import material_suggestions, text_suggestions
import logging

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 60*5})
CORS(app)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def _query_append_results(results, fn, query, PORTION_SIZE, type, main_info_key):
    assert not main_info_key or (main_info_key and PORTION_SIZE == 1), ("Invalid params passed" + locals())
    try:
        ret = fn(query)

        for i in range(0, len(ret), PORTION_SIZE):
            items = ret[i:i+PORTION_SIZE]

            if len(items) == 1:
                elem = items[0]
                
                if main_info_key:
                    main_info = elem.pop(main_info_key)
                    results.append({'type':type, 'main_info':main_info, 'details': elem})
                else:
                    results.append({'type':type, 'main_info':elem})

            else:
                results.append({'type':type, 'main_info':items})

    except Exception as ex:
        logging.warning('Error getting {}: {}'.format(fn.__name__, ex))


@app.route('/search')
@cache.cached(timeout=60*5, query_string=True)
def search():
    query = request.args.get('q')
    arxiv = request.args.get('arxiv')
    news = request.args.get('news')
    patents = request.args.get('patents')
    openai = request.args.get('openai')
    ai_free = request.args.get('ai_free')
    trends = request.args.get('trends')
    num = request.args.get('num', type=int)

    material_suggestions.MAX_RESULTS = text_suggestions.MAX_RESULTS = num

    material_common_params = {'PORTION_SIZE':1, 'query':query, 'main_info_key':'title'}
    suggestion_common_params = {'PORTION_SIZE':10, 'query':query, 'main_info_key':None}

    results = []

    if trends == 'true':
        common_params = suggestion_common_params.copy()
        common_params['type'] = 'GTrends'
        
        _query_append_results(
            results,
            fn = text_suggestions.get_google_trends_suggestions,
            **common_params
        )
        _query_append_results(
            results,
            fn = text_suggestions.get_google_trends_related_queries,
            **common_params
        )
        _query_append_results(
            results,
            fn = text_suggestions.get_google_trends_related_topics,
            **common_params
        )

    if arxiv == 'true':
        _query_append_results(
            results,
            fn = material_suggestions.arxiv_sample,
            type='ARXIV',
            **material_common_params
        )

        _query_append_results(
            results,
            fn = material_suggestions.arxiv_explorer_sample,
            type='ARXIV',
            **material_common_params
        )

    if news == 'true':
        _query_append_results(
            results,
            fn = material_suggestions.google_news_sample,
            type='NEWS',
            **material_common_params
        )

    if patents == 'true':
        _query_append_results(
            results,
            fn = material_suggestions.patents_view_sample,
            type='PATENTS',
            **material_common_params
        )

    material_common_params = material_common_params
    material_common_params['main_info_key'] = None

    if openai == 'true':
        _query_append_results(
            results,
            fn = text_suggestions.get_chatgpt_ideas,
            type='OpenAI',
            **material_common_params
        )

        _query_append_results(
            results,
            fn = text_suggestions.get_chatgpt_phrases,
            type='OpenAI',
            **suggestion_common_params
        )

    if ai_free == 'true':
        _query_append_results(
            results,
            fn = text_suggestions.get_hugging_face_inference,
            type='AI-free',
            **material_common_params
        )

    return jsonify({"results": results})

if __name__ == '__main__':
    app.run()
