def valid_parentheses(parens):
    """Are the parentheses validly balanced?
        >>> valid_parentheses("()")
        True
        >>> valid_parentheses("()()")
        True
        >>> valid_parentheses("(()())")
        True
        >>> valid_parentheses(")()")
        False
        >>> valid_parentheses("())")
        False
        >>> valid_parentheses("((())")
        False
        >>> valid_parentheses(")()(")
        False
    """    
    total = 0
    for val in parens:
        if val == '(':
            total = total + 1
        elif val == ')':
            total = total - 1
        if total < 0:
            return False
    return total == 0
