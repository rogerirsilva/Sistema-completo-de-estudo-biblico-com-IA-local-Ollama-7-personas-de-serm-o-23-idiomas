"""
Biblia em 23 Idiomas - Bible Study Tool with AI Assistance
Main Flask Application
"""
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from bible_data import (
    get_verse, get_chapter, get_available_languages, 
    get_available_books, BIBLE_DATA
)
from ollama_integration import OllamaAI

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")

ollama = OllamaAI()


@app.route('/')
def index():
    """Main page."""
    languages = get_available_languages()
    books = get_available_books()
    ollama_status = ollama.is_available()
    return render_template('index.html', 
                         languages=languages, 
                         books=books,
                         ollama_available=ollama_status)


@app.route('/api/verse', methods=['GET'])
def api_get_verse():
    """API endpoint to get a specific verse."""
    book = request.args.get('book', 'genesis')
    chapter = request.args.get('chapter', '1')
    verse = request.args.get('verse', '1')
    language = request.args.get('language', 'pt')
    
    verse_text = get_verse(book, chapter, verse, language)
    
    if verse_text:
        return jsonify({
            'success': True,
            'book': book,
            'chapter': chapter,
            'verse': verse,
            'language': language,
            'text': verse_text
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Verse not found'
        }), 404


@app.route('/api/chapter', methods=['GET'])
def api_get_chapter():
    """API endpoint to get all verses from a chapter."""
    book = request.args.get('book', 'genesis')
    chapter = request.args.get('chapter', '1')
    language = request.args.get('language', 'pt')
    
    verses = get_chapter(book, chapter, language)
    
    if verses:
        return jsonify({
            'success': True,
            'book': book,
            'chapter': chapter,
            'language': language,
            'verses': verses
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Chapter not found'
        }), 404


@app.route('/api/ai/analyze', methods=['POST'])
def api_ai_analyze():
    """API endpoint for AI verse analysis."""
    data = request.json
    verse_text = data.get('verse_text', '')
    language = data.get('language', 'pt')
    context = data.get('context', '')
    
    if not verse_text:
        return jsonify({
            'success': False,
            'error': 'Verse text is required'
        }), 400
    
    result = ollama.analyze_verse(verse_text, language, context)
    return jsonify(result)


@app.route('/api/ai/question', methods=['POST'])
def api_ai_question():
    """API endpoint for AI question answering."""
    data = request.json
    question = data.get('question', '')
    verse_text = data.get('verse_text', '')
    language = data.get('language', 'pt')
    
    if not question:
        return jsonify({
            'success': False,
            'error': 'Question is required'
        }), 400
    
    result = ollama.answer_question(question, verse_text, language)
    return jsonify(result)


@app.route('/api/languages', methods=['GET'])
def api_get_languages():
    """API endpoint to get available languages."""
    return jsonify({
        'success': True,
        'languages': get_available_languages()
    })


@app.route('/api/books', methods=['GET'])
def api_get_books():
    """API endpoint to get available books."""
    return jsonify({
        'success': True,
        'books': get_available_books()
    })


@app.route('/api/ollama/status', methods=['GET'])
def api_ollama_status():
    """API endpoint to check Ollama availability."""
    available = ollama.is_available()
    return jsonify({
        'available': available,
        'host': ollama.host,
        'model': ollama.model
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)
