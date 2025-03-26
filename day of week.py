from datetime import datetime

def get_day_of_week(date_str):
    """
    Calculate the day of the week from a date string.
    
    Args:
        date_str (str): Date in format 'YYYY-MM-DD'
        
    Returns:
        str: Day of the week (e.g., 'Monday', 'Tuesday', etc.)
    """
    try:
        # Parse the date string
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        # Get the day of the week (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_index = date_obj.weekday()
        
        return days[day_index]
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."

# Tests
def test_get_day_of_week():
    # Test cases with known dates and expected days
    test_cases = [
        ('2023-01-01', 'Sunday'),    # January 1, 2023 was a Sunday
        ('2023-05-15', 'Monday'),    # May 15, 2023 was a Monday
        ('2023-07-04', 'Tuesday'),   # July 4, 2023 was a Tuesday
        ('2023-09-20', 'Wednesday'), # September 20, 2023 was a Wednesday
        ('2023-11-23', 'Thursday'),  # November 23, 2023 was a Thursday
        ('2023-12-29', 'Friday'),    # December 29, 2023 was a Friday
        ('2023-12-30', 'Saturday'),  # December 30, 2023 was a Saturday
        ('2025-03-26', 'Wednesday'), # March 26, 2025 is a Wednesday (current date)
        ('invalid-date', 'Invalid date format. Please use YYYY-MM-DD.')
    ]
    
    # Run tests
    passed = 0
    failed = 0
    
    for date_str, expected_day in test_cases:
        result = get_day_of_week(date_str)
        if result == expected_day:
            print(f"PASS: {date_str} -> {result}")
            passed += 1
        else:
            print(f"FAIL: {date_str} -> Got {result}, Expected {expected_day}")
            failed += 1
    
    print(f"\nTest Summary: {passed} passed, {failed} failed")

# Run tests if this file is executed directly
if __name__ == "__main__":
    test_get_day_of_week()
