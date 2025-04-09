import pytest
from text_classifier import classify

def test_food_classification():
    """Test that food-related text is classified correctly."""
    text = "I want a cheeseburger with fries and a milkshake"
    result = classify(text)
    assert "Topic" in result
    assert result["Topic"].lower() in ["food", "meal", "restaurant", "cuisine", "burger"]

def test_sports_classification():
    """Test that sports-related text is classified correctly."""
    text = "The new england patriots won a lot of superbowls with Tom Brady as quarterback"
    result = classify(text)
    assert "Topic" in result
    assert result["Topic"].lower() in ["sports", "football", "nfl", "patriots", "superbowl"]

def test_technology_classification():
    """Test that technology-related text is classified correctly."""
    text = "Apple released a new iPhone with improved camera and faster processor"
    result = classify(text)
    assert "Topic" in result
    assert result["Topic"].lower() in ["technology", "tech", "iphone", "apple", "electronics", "gadget"]

def test_politics_classification():
    """Test that politics-related text is classified correctly."""
    text = "The president signed a new bill addressing climate change and renewable energy"
    result = classify(text)
    print(f"Politics test - Actual topic returned: '{result['Topic']}'")
    assert "Topic" in result
    assert result["Topic"].lower() in ["politics", "government", "policy", "legislation", "political", "climate", "environment", "energy", "climatechange"]

def test_health_classification():
    """Test that health-related text is classified correctly."""
    text = "Regular exercise and a balanced diet can help prevent heart disease"
    result = classify(text)
    assert "Topic" in result
    assert result["Topic"].lower() in ["health", "medical", "wellness", "fitness", "healthcare"]

if __name__ == "__main__":
    # Run the tests and print results
    print("Running test_food_classification...")
    try:
        test_food_classification()
        print("✅ PASSED: Food classification test")
    except AssertionError as e:
        print(f"❌ FAILED: Food classification test - {e}")
    
    print("\nRunning test_sports_classification...")
    try:
        test_sports_classification()
        print("✅ PASSED: Sports classification test")
    except AssertionError as e:
        print(f"❌ FAILED: Sports classification test - {e}")
    
    print("\nRunning test_technology_classification...")
    try:
        test_technology_classification()
        print("✅ PASSED: Technology classification test")
    except AssertionError as e:
        print(f"❌ FAILED: Technology classification test - {e}")
    
    print("\nRunning test_politics_classification...")
    try:
        test_politics_classification()
        print("✅ PASSED: Politics classification test")
    except AssertionError as e:
        print(f"❌ FAILED: Politics classification test - {e}")
    
    print("\nRunning test_health_classification...")
    try:
        test_health_classification()
        print("✅ PASSED: Health classification test")
    except AssertionError as e:
        print(f"❌ FAILED: Health classification test - {e}")
