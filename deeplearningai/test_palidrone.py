def is_palindrome(sentence):
    punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    left, right = 0, len(sentence) - 1

    while left < right:
        # Skip non-alphanumeric left
        while left < right and (not sentence[left].isalnum()):
            left += 1
        # Skip non-alphanumeric right
        while left < right and (not sentence[right].isalnum()):
            right -= 1
        # Now compare, ignoring case
        print("MARK: ", sentence[left], sentence[right])
        if sentence[left].lower() != sentence[right].lower():
            return False
        left += 1
        right -= 1
    return True


def test_palindrome1():
    sentence = "Draw, O coward!"
    assert is_palindrome(sentence)

def test_palindrome2():
    sentence = "I like bread"
    assert not is_palindrome(sentence)
