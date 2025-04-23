import requests
import json
import re

def summarize_text(text):
    """
    Summarizes the input text using the Ollama API with the mistral model.
    
    Args:
        text (str): The text to summarize
        
    Returns:
        dict: A dictionary with "summary" containing "text_summary" and "points" array
    """
    # Ollama API endpoint
    url = "https://ollama-proxy.cent-su.org/api/chat"
    
    # Prepare the message for summarization
    message = {
        "role": "user",
        "content": f"""You are an expert text summarizer. Your task is to create a highly condensed summary of the following text that captures the essential information while being significantly shorter than the original.

For shorter texts (under 500 words), create:
1. A very concise paragraph summary (2-3 sentences maximum)
2. 3-4 key bullet points

For longer texts (500+ words), create:
1. A concise paragraph summary (4-5 sentences maximum)
2. 5-7 key bullet points

Your summary must:
- Be at least 75% shorter than the original text
- Focus only on the most important information
- Eliminate all redundancy and unnecessary details
- Use simple, direct language
- Maintain the core meaning and key takeaways
- NOT be a mere rewording of the original text

The bullet points must:
- Each cover a distinct, important aspect of the text
- Be non-redundant (no overlapping information)
- Be concise (1-2 sentences maximum per point)
- Be arranged in order of importance

Text to summarize:
{text}

Format your response exactly like this:
SUMMARY: [your very concise paragraph summary here]
POINTS:
- [first point]
- [second point]
- [third point]
(etc.)"""
    }
    
    # Prepare the payload for Ollama API
    payload = {
        "model": "mistral",
        "messages": [message],
        "stream": False
    }
    
    try:
        # Make the API call
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Parse the response
        result = response.json()
        
        # Extract the generated text from the message content
        generated_text = result.get("message", {}).get("content", "").strip()
        
        if not generated_text:
            return {"summary": {"text_summary": "Failed to generate summary", "points": []}}
        
        # Parse the response to extract summary and points
        # First, split the response into summary and points sections
        parts = re.split(r'SUMMARY:|POINTS:', generated_text)
        
        # Extract the summary text (should be in the second part if split worked correctly)
        text_summary = "No summary generated"
        if len(parts) >= 2:
            text_summary = parts[1].strip()
        
        # Extract the bullet points
        points = []
        if len(parts) >= 3:
            # Find all lines starting with a dash/bullet
            points_text = parts[2]
            # Extract each bullet point
            points = [point.strip() for point in re.findall(r'-\s*(.*?)(?=\n-|\n|$)', points_text, re.DOTALL) if point.strip()]
        
        # Create the response structure
        summary_response = {
            "summary": {
                "text_summary": text_summary,
                "points": points
            }
        }
        
        return summary_response
    
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        return {"summary": {"text_summary": f"Error: {str(e)}", "points": []}}
    except (json.JSONDecodeError, KeyError, AttributeError) as e:
        print(f"Error processing API response: {e}")
        return {"summary": {"text_summary": f"Error: {str(e)}", "points": []}}

# Example usage
if __name__ == "__main__":
    # Test with a short example
    short_example = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. 
    AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals.
    The term "artificial intelligence" had previously been used to describe machines that mimic and display "human" cognitive skills that are associated with the human mind, such as "learning" and "problem-solving". 
    This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, which does not limit how intelligence can be articulated.
    AI applications include advanced web search engines, recommendation systems, understanding human speech, self-driving cars, automated decision-making, and competing at the highest level in strategic game systems.
    As machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect.
    """
    
    print("=== SHORT TEXT EXAMPLE ===")
    short_result = summarize_text(short_example)
    
    # Ensure proper JSON formatting
    formatted_json = json.dumps(short_result, indent=2, ensure_ascii=False)
    print(formatted_json)
    
    # Also print in a more readable format
    print("\n--- Readable Format ---")
    summary = short_result["summary"]
    print(f"Summary:\n{summary['text_summary']}\n")
    print("Key Points:")
    for i, point in enumerate(summary["points"], 1):
        print(f"{i}. {point}")
    
    # Test with a longer example
    print("\n\n=== LONGER TEXT EXAMPLE ===")
    long_example = """
    Climate change refers to long-term shifts in temperatures and weather patterns. These shifts may be natural, such as through variations in the solar cycle. But since the 1800s, human activities have been the main driver of climate change, primarily due to burning fossil fuels like coal, oil and gas.

    Burning fossil fuels generates greenhouse gas emissions that act like a blanket wrapped around the Earth, trapping the sun's heat and raising temperatures. Examples of greenhouse gas emissions that are causing climate change include carbon dioxide and methane. These come from using gasoline for driving a car or coal for heating a building, for example. Clearing land and forests can also release carbon dioxide. Landfills for garbage are a major source of methane emissions. Energy, industry, transport, buildings, agriculture and land use are among the main emitters.

    Greenhouse gas concentrations are at their highest levels in 2 million years and continue to rise. As a result, the Earth is now about 1.1°C warmer than it was in the 1800s. The last decade (2011-2020) was the warmest on record.

    Many people think climate change mainly means warmer temperatures. But temperature rise is only the beginning of the story. Because the Earth is a system, where everything is connected, changes in one area can influence changes in all others. The consequences of climate change now include, among others, intense droughts, water scarcity, severe fires, rising sea levels, flooding, melting polar ice, catastrophic storms and declining biodiversity.

    People are experiencing climate change in diverse ways. Climate change can affect our health, ability to grow food, housing, safety and work. Some of us are already more vulnerable to climate impacts, such as people living in small island nations and other developing countries. Conditions like sea-level rise and saltwater intrusion have advanced to the point where whole communities have had to relocate, and protracted droughts are putting people at risk of famine. In the future, the number of "climate refugees" is expected to rise.

    Every increase in global warming matters. In a series of UN reports, thousands of scientists and government reviewers agreed that limiting global temperature rise to no more than 1.5°C would help us avoid the worst climate impacts and maintain a livable climate. Yet the current path of carbon dioxide emissions could increase global temperature by as much as 4.4°C by the end of the century.

    The emissions that cause climate change come from every part of the world and affect everyone, but some countries produce much more than others. The 100 least-emitting countries generate 3 per cent of total emissions. The 10 countries with the largest emissions contribute 68 per cent. Everyone must take climate action, but people and countries creating more of the problem have a greater responsibility to act first.

    Many climate change solutions can deliver economic benefits while improving our lives and protecting the environment. We also have global frameworks and agreements to guide progress, such as the Sustainable Development Goals, the UN Framework Convention on Climate Change and the Paris Agreement. Three broad categories of action are: cutting emissions, adapting to climate impacts and financing required adjustments.

    Switching energy systems from fossil fuels to renewables like solar or wind will reduce the emissions driving climate change. But we have to start right now. While a growing coalition of countries is committing to net zero emissions by 2050, about half of emissions cuts must be in place by 2030 to keep warming below 1.5°C. Fossil fuel production must decline by roughly 6 per cent per year between 2020 and 2030.

    Adapting to climate consequences protects people, homes, businesses, livelihoods, infrastructure and natural ecosystems. It covers current impacts and those likely in the future. Adaptation will be required everywhere, but must be prioritized now for the most vulnerable people with the fewest resources to cope with climate hazards. The rate of return can be high. Early warning systems for disasters, for instance, save lives and property, and can deliver benefits up to 10 times the initial cost.

    We can pay the bill now, or pay dearly in the future. Climate action requires significant financial investments by governments and businesses. But climate inaction is vastly more expensive. One critical step is for industrialized countries to fulfill their commitment to provide $100 billion a year to developing countries so they can adapt and move toward greener economies.
    """
    
    long_result = summarize_text(long_example)
    
    # Ensure proper JSON formatting
    formatted_json = json.dumps(long_result, indent=2, ensure_ascii=False)
    print(formatted_json)
    
    # Also print in a more readable format
    print("\n--- Readable Format ---")
    summary = long_result["summary"]
    print(f"Summary:\n{summary['text_summary']}\n")
    print("Key Points:")
    for i, point in enumerate(summary["points"], 1):
        print(f"{i}. {point}")
