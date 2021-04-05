def reverse_vowels(s):
    """Reverse vowels in a string.
    Characters which are not vowels do not change position in string, but all
    vowels (y is not a vowel), should reverse their order.
    >>> reverse_vowels("Hello!")
    'Holle!'
    >>> reverse_vowels("Tomatoes")
    'Temotaos'
    >>> reverse_vowels("Reverse Vowels In A String")
    'RivArsI Vewols en e Streng'
    reverse_vowels("aeiou")
    'uoiea'
    reverse_vowels("why try, shy fly?")
    'why try, shy fly?''
    """
    string = list(s)
    ltr = 0
    word = len(s) - 1
    while ltr < word:
        if string[ltr].lower() not in set('aeiou'):
            ltr += 1
        elif string[word].lower() not in set('aeiou'):
            word -= 1
        else:
            string[ltr], string[word] = string[word], string[ltr]
            ltr += 1
            word -= 1
    return ''.join(string)