import requests
import json

def classify(text):
    """
    Classifies the input text into a single-word topic using the Ollama API.
    
    Args:
        text (str): The text to classify
        
    Returns:
        dict: A dictionary with a single key "Topic" and a value representing the topic
    """
    # Ollama API endpoint (using the proxy server from the notebook)
    url = "https://ollama-proxy.cent-su.org/api/chat"
    
    # Prepare the message for classification
    message = {
        "role": "user",
        "content": f"Classify the following text into a single-word topic. Only respond with one word that best represents the topic.\n\nText: {text}\n\nTopic:"
    }
    
    # Prepare the payload for Ollama API
    payload = {
        "model": "mistral", # Using mistral as seen in the notebook
        "messages": [message],
        "stream": False
    }
    
    try:
        # Make the API call
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Parse the response
        result = response.json()
        
        # Extract the generated text (topic) from the message content
        generated_text = result.get("message", {}).get("content", "").strip()
        
        # If multiple words or empty, handle appropriately
        if not generated_text:
            return {"Topic": "Unknown"}
        
        # Take the first word if multiple words are returned
        # Split on spaces and special characters like slashes
        import re
        topic = re.split(r'[\s/]+', generated_text)[0]
        
        return {"Topic": topic}
    
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        return {"Topic": "Error", "Error": str(e)}
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error processing API response: {e}")
        return {"Topic": "Error", "Error": str(e)}

# Example usage
if __name__ == "__main__":
    # Test with examples
    examples = [
        "I want a cheeseburger",
        "The new england patriots won a lot of superbowls"
    ]
    
    for example in examples:
        result = classify(example)
        print(f"Text: {example}")
        print(f"Classification: {result}")
        print()
