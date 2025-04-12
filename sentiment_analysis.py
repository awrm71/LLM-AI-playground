import requests
import json

def sentiment_analysis(text):
    """
    Analyze the sentiment of the given text using Ollama API.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        dict: A dictionary with keys "sentiment" and "rationale"
    """
    # Construct the prompt for sentiment analysis
    prompt = f"""
    Analyze the sentiment of the following text and provide:
    1. The sentiment as ONLY ONE WORD: "Positive", "Negative", or "Neutral"
    2. A brief rationale (2-5 words) explaining why you classified it that way
    
    Format your response exactly like this:
    Sentiment: [your one-word sentiment]
    Rationale: [your brief explanation]
    
    Text: "{text}"
    """
    
    # Send request to Ollama API
    try:
        response = requests.post(
            "https://ollama-proxy.cent-su.org/api/chat",
            json={
                "model": "mistral",  # Using mistral model as seen in the notebook
                "messages": [{"role": "user", "content": prompt}]
            },
            stream=True  # Enable streaming response
        )
        
        # Process the response
        full_response = ""
        for line in response.iter_lines():
            if line:
                json_obj = json.loads(line.decode("utf-8"))
                if "message" in json_obj and "content" in json_obj["message"]:
                    full_response += json_obj["message"]["content"]
        
        # Parse the response to extract sentiment and rationale
        # More robust parsing
        sentiment = "neutral"  # Default
        rationale = "no specific reason provided"  # Default
        
        # Extract sentiment more precisely
        if "sentiment: positive" in full_response.lower():
            sentiment = "positive"
        elif "sentiment: negative" in full_response.lower():
            sentiment = "negative"
        elif "sentiment: neutral" in full_response.lower():
            sentiment = "neutral"
        
        # Try to extract rationale using different approaches
        if "rationale:" in full_response.lower():
            # If formatted as requested
            rationale_part = full_response.lower().split("rationale:")[1].strip()
            
            # Extract the first complete sentence
            if "." in rationale_part:
                rationale = rationale_part.split(".")[0].strip() + "."
            else:
                # If no period, take the whole rationale but ensure it's a complete thought
                rationale = rationale_part.strip()
            
            # Ensure the rationale doesn't end abruptly
            if len(rationale) > 100:
                # If it's too long, find the last space before 100 chars and cut there
                last_space = rationale[:100].rfind(' ')
                if last_space > 0:
                    rationale = rationale[:last_space].strip()
            
            # Always add a period if it doesn't end with punctuation
            if rationale and not rationale[-1] in ['.', '!', '?']:
                rationale += "."
        else:
            # Try to extract a reason from the response
            # Remove the sentiment part if it exists
            cleaned_response = full_response.lower()
            for term in ["positive", "negative", "neutral", "sentiment:"]:
                cleaned_response = cleaned_response.replace(term, "")
            
            # Take a complete thought as the rationale
            sentences = cleaned_response.split('.')
            if sentences:
                rationale = sentences[0].strip()
            
            # Always add a period if it doesn't end with punctuation
            if rationale and not rationale[-1] in ['.', '!', '?']:
                rationale += "."
        
        # Format the dictionary with proper commas
        result = {
            "sentiment": sentiment,
            "rationale": rationale
        }
        return result
    
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        # Format the dictionary with proper commas
        result = {
            "sentiment": "neutral",
            "rationale": "error in analysis",
            "error": str(e)
        }
        return result

# Example usage
if __name__ == "__main__":
    # Test examples
    examples = [
        "I love the weather today",
        "I have a lot of work due at the end of the day, it's making me stressed",
        "I have coding to do later",
        "I do not like green eggs and ham",
        "I won the lottery"
    ]
    
    for example in examples:
        result = sentiment_analysis(example)
        print(f"Text: {example}")
        # Use a custom format with proper JSON structure
        print("Result: {")
        print(f"  \"sentiment\": \"{result['sentiment']}\",")
        print(f"  \"rationale\": \"{result['rationale']}\"")
        print("}")
        print()
