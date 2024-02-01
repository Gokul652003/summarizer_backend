import PyPDF2

def extract_sentences_from_pdf(pdf_file_path):
    sentences = []
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page_text = pdf_reader.pages[page_num].extract_text()
            sentences.extend(page_text.split('. '))  # Split text into sentences based on period
    return sentences

# Example usage:
pdf_file_path = "1.pdf"  # Replace with the path to your PDF file
sentences = extract_sentences_from_pdf(pdf_file_path)
print(sentences)
