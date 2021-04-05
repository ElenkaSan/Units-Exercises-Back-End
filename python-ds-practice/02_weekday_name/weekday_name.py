def weekday_name(day_of_week):
    """Return name of weekday.    
        >>> weekday_name(1)
        'Monday'        
        >>> weekday_name(7)
        'Sunday'        
    For days not between 1 and 7, return None    
        >>> weekday_name(9)
        >>> weekday_name(0)
    """
    weekdays = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
    return weekdays.get(day_of_week, 'None')