from flask import Flask, render_template, request, jsonify
import material_suggestions
import json

app = Flask(__name__)
results = []


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the selected sources
        query = request.form['query']
        sources = request.form.getlist('sources')

        # Perform the searches and update the output
        output = []
        results = []
        if "arxiv" in sources:
            # Get Arxiv articles for the query
            articles = material_suggestions.arxiv_sample(query)

            results.extend([elem for elem in articles])
            output.extend([('ARXIV', elem['title']) for elem in articles])

        return jsonify({"results": output})

    return render_template('flask_web.html')

@app.route('/row/<int:index>', methods=['GET'])
def row_details(index):
    elem = results[index]

    return jsonify({"row": json.dumps(elem, indent=4, sort_keys=True, default=str)})

if __name__ == '__main__':
    app.run(debug=True)
