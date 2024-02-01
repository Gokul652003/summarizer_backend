from flask import Flask, render_template, request, jsonify
# import os
import json
import PyPDF2
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_sentences_from_pdf(pdf_file):
    sentences = []
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page_text = pdf_reader.pages[page_num].extract_text()
        sentences.extend(page_text.split('. '))
    return sentences

def summarize_text_documents(text_documents, sentenceCount):
    try:
        # Summarization logic for text documents
        parser = PlaintextParser.from_string('\n'.join(text_documents), Tokenizer('english'))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentenceCount)  # Summarize to 3 sentences
        return ' '.join(str(sentence) for sentence in summary)
    except Exception as e:
        print(f"Error in text summarization: {str(e)}")
        return ''

def summarize_pdf_file(pdf_file, sentenceCount):
    try:
        pdf_text = ''
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page_text = pdf_reader.pages[page_num].extract_text()
            pdf_text += page_text + ' '  # Concatenate text from all pages
        parser = PlaintextParser.from_string(pdf_text, Tokenizer('english'))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentenceCount)  # Summarize to 3 sentences
        return ' '.join(str(sentence) for sentence in summary)
    except Exception as e:
        print(f"Error in summarizing PDF file: {str(e)}")
        return ''

@app.route('/')
def front():
    return render_template('front.html')

@app.route('/textSummarize', methods=['POST'])
def text_summarize():
    try:
        # Get text documents
        text_documents = json.loads(request.form.get('textDocuments'))
        sentenceCount = request.form.get('sentenceCount')

        # Process text documents
        text_summary = summarize_text_documents(text_documents, int(sentenceCount))

        result = {
            'summary': f'Text Documents: {text_summary}'
        }

        return jsonify(result)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)})

@app.route('/pdfSummarize', methods=['POST'])
def pdf_summarize():
    try:
        # Get PDF files
        pdf_files = request.files.getlist('pdfFiles')
        sentenceCount = request.form.get('sentenceCount')

        # Process PDF files
        pdf_summaries = [summarize_pdf_file(pdf_file, int(sentenceCount)) for pdf_file in pdf_files]

        result = {
            'summary': f'PDF Documents: {" ".join(pdf_summaries)}'
        }

        return jsonify(result)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
