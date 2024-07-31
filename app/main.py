from flask import Flask, request, jsonify
from app.controllers.events_controller import events_bp
from app.services.events_service import db

app = Flask(__name__)

# Register the blueprint for the events routes
app.register_blueprint(events_bp)

@app.route('/ping', methods=['GET'])
def ping():
    print("My name is Ayush and this app rocks")
    return jsonify({"response": "pong"}), 200

if __name__ == "__main__":
    app.run(debug=True)


# @app.route('/add', methods=['POST'])
# def add_document():
#     data = request.json
#     doc_ref = db.collection('your_collection').document(data['id'])
#     doc_ref.set(data)
#     return jsonify({"success": True}), 200

# @app.route('/get/<doc_id>', methods=['GET'])
# def get_document(doc_id):
#     doc_ref = db.collection('your_collection').document(doc_id)
#     doc = doc_ref.get()
#     if doc.exists:
#         return jsonify(doc.to_dict()), 200
#     else:
#         return jsonify({"error": "Document not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
