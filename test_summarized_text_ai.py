import pytest
import json
from summarized_text_ai import summarize_text

def test_basic_functionality():
    """Test that the summarize_text function returns the expected structure."""
    text = "This is a simple test sentence to check if the function works."
    result = summarize_text(text)
    
    # Check the structure of the result
    assert isinstance(result, dict)
    assert "summary" in result
    assert "text_summary" in result["summary"]
    assert "points" in result["summary"]
    assert isinstance(result["summary"]["points"], list)

def test_short_text():
    """Test summarization of a short text."""
    short_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. 
    AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals.
    The term "artificial intelligence" had previously been used to describe machines that mimic and display "human" cognitive skills that are associated with the human mind, such as "learning" and "problem-solving". 
    This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, which does not limit how intelligence can be articulated.
    """
    
    result = summarize_text(short_text)
    
    # Verify the result
    assert len(result["summary"]["text_summary"]) > 0
    assert len(result["summary"]["points"]) > 0
    
    # The summary should be significantly shorter than the original text
    assert len(result["summary"]["text_summary"]) < len(short_text) * 0.5
    
    # Print the result for manual inspection
    print("\n=== Short Text Summary ===")
    print(f"Summary: {result['summary']['text_summary']}")
    print("Points:")
    for i, point in enumerate(result["summary"]["points"], 1):
        print(f"{i}. {point}")

def test_long_text():
    """Test summarization of a longer text."""
    long_text = """
    Climate change refers to long-term shifts in temperatures and weather patterns. These shifts may be natural, such as through variations in the solar cycle. But since the 1800s, human activities have been the main driver of climate change, primarily due to burning fossil fuels like coal, oil and gas.

    Burning fossil fuels generates greenhouse gas emissions that act like a blanket wrapped around the Earth, trapping the sun's heat and raising temperatures. Examples of greenhouse gas emissions that are causing climate change include carbon dioxide and methane. These come from using gasoline for driving a car or coal for heating a building, for example. Clearing land and forests can also release carbon dioxide. Landfills for garbage are a major source of methane emissions. Energy, industry, transport, buildings, agriculture and land use are among the main emitters.

    Greenhouse gas concentrations are at their highest levels in 2 million years and continue to rise. As a result, the Earth is now about 1.1°C warmer than it was in the 1800s. The last decade (2011-2020) was the warmest on record.

    Many people think climate change mainly means warmer temperatures. But temperature rise is only the beginning of the story. Because the Earth is a system, where everything is connected, changes in one area can influence changes in all others. The consequences of climate change now include, among others, intense droughts, water scarcity, severe fires, rising sea levels, flooding, melting polar ice, catastrophic storms and declining biodiversity.
    """
    
    result = summarize_text(long_text)
    
    # Verify the result
    assert len(result["summary"]["text_summary"]) > 0
    assert len(result["summary"]["points"]) > 0
    
    # The summary should be significantly shorter than the original text
    assert len(result["summary"]["text_summary"]) < len(long_text) * 0.25
    
    # For longer texts, we expect more bullet points
    assert len(result["summary"]["points"]) >= 4
    
    # Print the result for manual inspection
    print("\n=== Long Text Summary ===")
    print(f"Summary: {result['summary']['text_summary']}")
    print("Points:")
    for i, point in enumerate(result["summary"]["points"], 1):
        print(f"{i}. {point}")

def test_sports_article():
    """Test summarization of a sports article."""
    sports_article = """
    The Indiana Pacers and Milwaukee Bucks do not like each other. They have created a rivalry over the last couple of years that is turning into one of the best in the NBA.

    These two teams squared off in the playoffs last year, which the Pacers won. Now, they renew their rivalry this postseason, meeting in the first round of the playoffs yet again.

    There have been a lot of great moments over the last few years between these two teams. There are five moments that really stick out as the best part of this rivalry.

    Read more: Pacers' Myles Turner Makes NBA History With Special Season

    5. Tyrese Haliburton's floater to win Game 3
    Tyrese Haliburton showed that he can be clutch in big moments. He hit a floater over Patrick Beverley and got fouled. That and one opportunity with just a second left in overtime gave the Pacers a 2-1 series lead.

    Haliburton showed that he was able to come up big in the biggest moments. It gave the team the confidence to finish them off in six games.

    4. Patrick Beverley fires a ball at a Pacers fan
    In what ended up being the final moment of Patrick Beverley's NBA career, he fired a fan directly at a Pacers fan at the end of Game 6 last year.


    It was a moment that underscored how dirty of a player he has been throughout his career. He was suspended for five games, but he hasn't served it because no team has signed him after that moment.

    More Pacers news: Pacers Must Exploit Bucks Big Weakness to Advance

    3. Tyrese Haliburton hits game-winning three
    Haliburton hit another game-winning shot against the Bucks, this time just a few weeks ago. He hit a corner three over Giannis Antetokounmpo while also getting fouled.

    The 3-point shot tied the game while hitting the free throw gave the Pacers the lead. They ended up winning the game, keeping them from being swept by Milwaukee this year.

    2. Tyrese Haliburton does the 'Dame Time' celebration in Las Vegas
    During the inaugural NBA Cup, the Indiana Pacers took on the Bucks in the semifinals against the Bucks. That was when Tyrese Haliburton announced his arrival to stardom in the NBA.

    After hitting a three to essentially close out the Bucks, Haliburton hit the Dame Time celebration right in front of the Milwaukee bench.


    That was one of the big moments that started the Bucks hating the Pacers. Haliburton also showed everyone that he can be one of the best players on a title-contending team.

    1. Ballgate
    By far, the biggest moment in this rivalry was Ballgate. In a regular season game last year, Antetokounmpo set a franchise record in scoring for a single game.

    He wanted to get the game ball to commemorate that record. The Pacers wanted to give it to Oscar Tshiebwe, who had scored his first NBA bucket.

    Antetokounmpo lost his mind, trying to storm into Indiana's locker room to retrieve the ball. It turns out that the Bucks had the game ball all along.

    More great moments will certainly come from this year's playoff series.

    More Indiana Pacers news: Pacers Must Exploit Bucks Big Weakness to Advance

    Biggest Storylines For Pacers in Upcoming Playoff Series vs Bucks
    """
    
    result = summarize_text(sports_article)
    
    # Verify the result
    assert len(result["summary"]["text_summary"]) > 0
    assert len(result["summary"]["points"]) > 0
    
    # The summary should be significantly shorter than the original text
    assert len(result["summary"]["text_summary"]) < len(sports_article) * 0.2
    
    # For this longer article, we expect more bullet points
    assert len(result["summary"]["points"]) >= 5
    
    # Print the result for manual inspection
    print("\n=== Sports Article Summary ===")
    print(f"Summary: {result['summary']['text_summary']}")
    print("Points:")
    for i, point in enumerate(result["summary"]["points"], 1):
        print(f"{i}. {point}")

def test_error_handling():
    """Test that the function handles errors gracefully."""
    # Test with empty text
    empty_result = summarize_text("")
    assert "summary" in empty_result
    assert "text_summary" in empty_result["summary"]
    assert "points" in empty_result["summary"]
    
    # The function should return a default message for empty input
    assert empty_result["summary"]["text_summary"] != ""
    
    # Test with very short text that might be difficult to summarize
    short_result = summarize_text("Hello world.")
    assert "summary" in short_result
    assert "text_summary" in short_result["summary"]
    assert "points" in short_result["summary"]

if __name__ == "__main__":
    # Run the tests and display the results
    pytest.main(["-v", __file__])
