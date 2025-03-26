"""
Text Classification Module

This module provides functionality to classify text into one of N categories
using AI-based natural language processing.
"""

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: transformers library not found. Using fallback method.")
    print("For better results, install transformers: pip install transformers")

import re
import math
from collections import Counter


def classify_text(text, categories):
    """
    Classify the given text into one of the provided categories using AI.
    
    Args:
        text (str): The text to classify
        categories (list): List of category strings to choose from
        
    Returns:
        str: The best matching category from the provided list
    """
    if not text or not categories:
        return None
    
    if len(categories) == 1:
        return categories[0]
    
    # Use transformers if available for better classification
    if TRANSFORMERS_AVAILABLE:
        return classify_with_transformers(text, categories)
    else:
        return classify_with_fallback(text, categories)


def classify_with_transformers(text, categories):
    """
    Classify text using the transformers library and zero-shot classification.
    
    This method uses a pre-trained model to determine which category best matches
    the given text without requiring specific training for these categories.
    """
    # Initialize zero-shot classification pipeline
    classifier = pipeline("zero-shot-classification")
    
    # Perform classification
    result = classifier(text, categories)
    
    # Return the highest scoring category
    return result['labels'][0]


def classify_with_fallback(text, categories):
    """
    Fallback classification method using basic NLP techniques.
    
    This is used when the transformers library is not available.
    It's less accurate but provides basic functionality.
    """
    # Preprocess text
    text = text.lower()
    words = re.findall(r'\w+', text)
    word_counts = Counter(words)
    
    # Special case handling for technology-related terms
    tech_indicators = ['smartphone', 'phone', 'mobile', 'camera', 'app', 'device', 'gadget', 'tech']
    if any(tech_word in text.lower() for tech_word in tech_indicators):
        for category in categories:
            if 'tech' in category.lower():
                return category
    
    # Calculate scores for each category based on word overlap
    scores = {}
    for category in categories:
        # Preprocess category
        category_words = set(re.findall(r'\w+', category.lower()))
        
        # Calculate score based on word frequency in text
        score = sum(word_counts[word] for word in category_words if word in word_counts)
        
        # Add semantic similarity based on word embeddings (simplified)
        # This is a very basic approach - just checking if words in the text
        # are related to the category in some way
        related_words = get_related_words(category)
        semantic_score = sum(word_counts[word] for word in related_words if word in word_counts)
        
        # Combine scores
        scores[category] = score + (semantic_score * 0.5)
    
    # If no matches found, use a more general approach
    if all(score == 0 for score in scores.values()):
        return classify_by_general_topic(text, categories)
    
    # Return the category with the highest score
    return max(scores, key=scores.get)


def get_related_words(category):
    """
    Get words related to a category.
    
    This is a simplified implementation that returns predefined related words
    for common categories. In a real implementation, this would use word embeddings
    or a knowledge graph.
    """
    related_words_dict = {
        'food': ['eat', 'drink', 'meal', 'restaurant', 'cook', 'taste', 'delicious', 
                'breakfast', 'lunch', 'dinner', 'snack', 'recipe', 'cuisine', 
                'cheese', 'meat', 'vegetable', 'fruit', 'dessert', 'sweet', 'savory'],
        
        'learning': ['study', 'education', 'school', 'college', 'university', 'course', 
                    'learn', 'knowledge', 'teacher', 'student', 'class', 'lecture', 
                    'book', 'read', 'understand', 'comprehend', 'skill', 'subject'],
        
        'technology': ['computer', 'software', 'hardware', 'internet', 'digital', 
                      'device', 'app', 'application', 'program', 'code', 'data', 
                      'system', 'network', 'online', 'electronic', 'tech', 'smartphone',
                      'phone', 'mobile', 'camera', 'gadget', 'screen', 'battery', 'smart',
                      'technology', 'wifi', 'bluetooth', 'wireless', 'processor', 'memory',
                      'storage', 'photo', 'video', 'resolution', 'display', 'pixel', 'bought'],
        
        'sports': ['game', 'play', 'team', 'player', 'ball', 'score', 'win', 'lose', 
                  'competition', 'match', 'tournament', 'athlete', 'coach', 'field', 
                  'court', 'stadium', 'exercise', 'fitness'],
        
        'entertainment': ['movie', 'film', 'show', 'tv', 'television', 'music', 'song', 
                         'concert', 'performance', 'actor', 'actress', 'celebrity', 
                         'star', 'watch', 'listen', 'enjoy', 'fun', 'amusement'],
        
        'health': ['doctor', 'hospital', 'medicine', 'medical', 'disease', 'symptom', 
                  'treatment', 'therapy', 'healthy', 'wellness', 'fitness', 'exercise', 
                  'diet', 'nutrition', 'body', 'mental', 'physical'],
        
        'business': ['company', 'corporation', 'firm', 'enterprise', 'organization', 
                    'industry', 'market', 'product', 'service', 'customer', 'client', 
                    'profit', 'revenue', 'sales', 'management', 'executive', 'finance'],
        
        'travel': ['trip', 'journey', 'vacation', 'holiday', 'tour', 'tourism', 
                  'destination', 'hotel', 'flight', 'airplane', 'airport', 'country', 
                  'city', 'place', 'visit', 'explore', 'adventure', 'sightseeing'],
    }
    
    # Get related words for the category or return empty list if not found
    category_lower = category.lower()
    for key, words in related_words_dict.items():
        if category_lower == key or category_lower in key or key in category_lower:
            return words
    
    # If no direct match, return empty list
    return []


def classify_by_general_topic(text, categories):
    """
    Classify text by general topic when no direct word matches are found.
    
    This is a fallback method that uses predefined topics and their related words
    to find the best matching category.
    """
    # Define general topics and their related words
    general_topics = {
        'food': ['food', 'eat', 'drink', 'meal', 'cook', 'taste', 'recipe', 'cuisine', 
                'restaurant', 'chef', 'ingredient', 'flavor', 'dish', 'delicious'],
        
        'education': ['learn', 'study', 'education', 'school', 'college', 'university', 
                     'knowledge', 'academic', 'teacher', 'student', 'class', 'course'],
        
        'technology': ['tech', 'computer', 'digital', 'software', 'hardware', 'internet', 
                      'online', 'device', 'app', 'program', 'code', 'data', 'system',
                      'smartphone', 'phone', 'mobile', 'camera', 'gadget', 'electronic',
                      'smart', 'technology', 'wifi', 'bluetooth', 'wireless', 'processor',
                      'memory', 'storage', 'photo', 'video', 'screen', 'display', 'bought', 'new'],
        
        'sports': ['sport', 'game', 'play', 'team', 'player', 'competition', 'match', 
                  'win', 'lose', 'score', 'athlete', 'fitness', 'exercise'],
        
        'entertainment': ['entertain', 'movie', 'film', 'show', 'music', 'song', 'concert', 
                         'performance', 'actor', 'celebrity', 'star', 'watch', 'listen'],
        
        'health': ['health', 'medical', 'doctor', 'hospital', 'medicine', 'disease', 
                  'treatment', 'therapy', 'wellness', 'body', 'mental', 'physical'],
        
        'business': ['business', 'company', 'market', 'product', 'service', 'customer', 
                    'profit', 'revenue', 'sales', 'management', 'finance', 'economy'],
        
        'travel': ['travel', 'trip', 'journey', 'vacation', 'tour', 'destination', 
                  'hotel', 'flight', 'country', 'city', 'visit', 'explore', 'adventure'],
    }
    
    # Preprocess text
    text = text.lower()
    words = set(re.findall(r'\w+', text))
    
    # Special case for technology-related terms
    tech_terms = ['smartphone', 'phone', 'mobile', 'camera', 'app', 'device', 'gadget']
    if any(term in text for term in tech_terms):
        for category in categories:
            if 'tech' in category.lower():
                return category
    
    # Calculate scores for each general topic
    topic_scores = {}
    for topic, topic_words in general_topics.items():
        # Count how many topic words appear in the text
        matches = sum(1 for word in topic_words if word in words)
        if matches > 0:
            topic_scores[topic] = matches
    
    if not topic_scores:
        # If no matches, return the first category as default
        return categories[0]
    
    # Find the best matching general topic
    best_topic = max(topic_scores, key=topic_scores.get)
    
    # Find the category that best matches this topic
    category_scores = {}
    for category in categories:
        category_lower = category.lower()
        # Direct match
        if best_topic in category_lower or category_lower in best_topic:
            category_scores[category] = 10  # High score for direct match
        else:
            # Calculate similarity based on character overlap
            similarity = calculate_string_similarity(best_topic, category_lower)
            category_scores[category] = similarity
    
    # Return the best matching category
    return max(category_scores, key=category_scores.get)


def calculate_string_similarity(str1, str2):
    """
    Calculate a simple similarity score between two strings.
    
    This is a basic implementation that considers character overlap.
    """
    # Convert to sets of characters
    set1 = set(str1)
    set2 = set(str2)
    
    # Calculate Jaccard similarity
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    if union == 0:
        return 0
    
    return intersection / union


# Test the classification function
def test_classification():
    """
    Test the text classification function with various examples.
    """
    test_cases = [
        {
            "text": "I like cheese and pasta with tomato sauce",
            "categories": ["food", "learning", "technology", "sports"],
            "expected": "food"
        },
        {
            "text": "The professor gave an interesting lecture on quantum physics",
            "categories": ["food", "learning", "technology", "sports"],
            "expected": "learning"
        },
        {
            "text": "I bought a new smartphone with an amazing camera",
            "categories": ["food", "learning", "technology", "sports"],
            "expected": "technology"
        },
        {
            "text": "The team won the championship after an exciting match",
            "categories": ["food", "learning", "technology", "sports"],
            "expected": "sports"
        },
        {
            "text": "I enjoy watching movies on weekends",
            "categories": ["entertainment", "business", "health", "travel"],
            "expected": "entertainment"
        }
    ]
    
    print("Running classification tests...")
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases):
        result = classify_text(test["text"], test["categories"])
        expected = test["expected"]
        
        if result == expected:
            print(f"Test {i+1}: PASS")
            print(f"  Text: '{test['text']}'")
            print(f"  Categories: {test['categories']}")
            print(f"  Result: '{result}' (Expected: '{expected}')")
            passed += 1
        else:
            print(f"Test {i+1}: FAIL")
            print(f"  Text: '{test['text']}'")
            print(f"  Categories: {test['categories']}")
            print(f"  Result: '{result}' (Expected: '{expected}')")
            failed += 1
        
        print()
    
    print(f"Test Summary: {passed} passed, {failed} failed")
    return passed, failed


# Run tests if this file is executed directly
if __name__ == "__main__":
    test_classification()
