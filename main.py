from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/search')
def search():
    query = request.args.get('q')
    arxiv = request.args.get('arxiv')
    news = request.args.get('news')
    
    # perform search based on query, arxiv, and news
    
    results = [
        {
            "type": "Article",
            "main_info": "Quantum Computing 101",
            "details": {
                "author": "John Doe",
                "date": "2023-04-30",
                "source": "Arxiv",
                "url": "https://arxiv.org/abs/12345.6789",
                "abstract": "A brief introduction to quantum computing for beginners."
            }
        },
        {
            "type": "News",
            "main_info": "Google announces new quantum computer breakthrough",
            "details": {
                "author": "Jane Smith",
                "date": "2023-04-28",
                "source": "CNN",
                "url": "https://www.cnn.com/tech/article/google-quantum-computer-breakthrough",
                "abstract": "Google's latest quantum computer can perform calculations that were previously thought impossible."
            }
        }
    ]
    
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run()
