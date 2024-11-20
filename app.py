from flask import Flask, request, jsonify
from document_processor import load_document, process_load_document

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        # Read the file into a PIL Image
        poller_object = load_document(file.stream)
        result = process_load_document(poller_object)
        return jsonify({'message': 'Image received, processing done', 'data': result}), 200, {'Content-Type': 'application/json'}
    else:
        return jsonify({'message': 'Allowed file types are png'}), 400, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True)