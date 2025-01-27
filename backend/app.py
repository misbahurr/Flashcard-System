from flask import Flask, jsonify, request
from models import db, User, Flashcard, Review
from srs import calculate_next_review
from ai_suggestions import get_related_flashcards

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

@app.route('/api/flashcard', methods=['POST'])
def create_flashcard():
    data = request.json
    new_card = Flashcard(
        question=data['question'],
        answer=data['answer'],
        user_id=data['user_id'],
        topic=data.get('topic', 'general')
    )
    db.session.add(new_card)
    db.session.commit()
    return jsonify({"message": "Flashcard created!"}), 201

@app.route('/api/review', methods=['POST'])
def log_review():
    data = request.json
    card = Flashcard.query.get(data['card_id'])
    
    new_review = Review(
        flashcard_id=data['card_id'],
        performance=data['score'],
        next_review=calculate_next_review(data['score'], card.current_interval)
    )
    
    db.session.add(new_review)
    db.session.commit()
    
    # Get AI suggestions
    suggestions = get_related_flashcards(card.user, card)
    return jsonify({
        "next_review": new_review.next_review,
        "suggestions": [s.question for s in suggestions]
    })