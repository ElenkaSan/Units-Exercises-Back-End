def same_frequency(num1, num2):
    """Do these nums have same frequencies of digits?    
        >>> same_frequency(551122, 221515)
        True        
        >>> same_frequency(321142, 3212215)
        False        
        >>> same_frequency(1212, 2211)
        True
    """
    amn = {}
    for string in num1, num2:
        amn[string] = amn.get(string, 0) + 1
    return len((str(num1))) == len(str(num2))
   