from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_related_flashcards(user, current_flashcard):
    # Generate embeddings for all flashcards
    all_cards = [card.question for card in user.flashcards]
    embeddings = model.encode(all_cards)
    
    # Find similar cards
    current_embedding = model.encode([current_flashcard.question])
    similarities = cosine_similarity(current_embedding, embeddings)
    
    # Return top 3 related cards
    top_indices = np.argsort(similarities[0])[-3:]
    return [user.flashcards[i] for i in top_indices]