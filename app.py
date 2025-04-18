from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import os
from analyzer import MenuAnalyzer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis_results = None
    url = None
    error = None
    
    if request.method == 'POST':
        url = request.form.get('menu_url')
        if not url:
            error = "Por favor, insira uma URL válida"
        else:
            try:
                analyzer = MenuAnalyzer(url)
                analysis_results = analyzer.analyze()
            except Exception as e:
                error = f"Erro ao analisar o menu: {str(e)}"
    
    return render_template('index.html', analysis_results=analysis_results, url=url, error=error)

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.json
    url = data.get('menu_url')
    
    if not url:
        return jsonify({"error": "URL não fornecida"}), 400
    
    try:
        analyzer = MenuAnalyzer(url)
        analysis_results = analyzer.analyze()
        return jsonify({"results": analysis_results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)