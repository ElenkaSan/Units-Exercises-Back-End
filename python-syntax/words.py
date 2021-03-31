def print_upper_words(words, must_start_with):
    # For a list of words, print out each word on a separate line, 
    # but in all uppercase. 
    # Change that function so that it only prints words that start
    # with the letter ‘e’ (either upper or lowercase).
    for word in words:
        for letter in must_start_with:
            if word.startswith(letter):
                print(word.upper())

# this should print "HELLO", "HEY", "YO", and "YES"

print_upper_words(["hello", "hey", "goodbye", "yo", "yes"],
                   must_start_with={"h", "y"})