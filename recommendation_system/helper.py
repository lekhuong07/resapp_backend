# Python3 implementation of above approach
from math import floor, ceil
import math
import re
from collections import Counter

WORD = re.compile(r"\w+")

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)

# Function to calculate the
# Jaro Similarity of two s
def jaro_distance(s1, s2):
    # If the s are equal
    if (s1 == s2):
        return 1.0

    # Length of two s
    len1 = len(s1)
    len2 = len(s2)

    # Maximum distance upto which matching
    # is allowed
    max_dist = floor(max(len1, len2) / 2) - 1

    # Count of matches
    match = 0

    # Hash for matches
    hash_s1 = [0] * len(s1)
    hash_s2 = [0] * len(s2)

    # Traverse through the first
    for i in range(len1):

        # Check if there is any matches
        for j in range(max(0, i - max_dist),
                       min(len2, i + max_dist + 1)):

            # If there is a match
            if (s1[i] == s2[j] and hash_s2[j] == 0):
                hash_s1[i] = 1
                hash_s2[j] = 1
                match += 1
                break

    # If there is no match
    if (match == 0):
        return 0.0

    # Number of transpositions
    t = 0
    point = 0

    # Count number of occurrences
    # where two characters match but
    # there is a third matched character
    # in between the indices
    for i in range(len1):
        if (hash_s1[i]):

            # Find the next matched character
            # in second
            while (hash_s2[point] == 0):
                point += 1

            if (s1[i] != s2[point]):
                t += 1
            point += 1
    t = t // 2

    # Return the Jaro Similarity
    return (match / len1 + match / len2 +
            (match - t) / match) / 3.0


# Driver code
s1 = "CRATE"
s2 = "TRACE"

# Prjaro Similarity of two s
print(round(jaro_distance(s1, s2), 6))

# This code is contributed by mohit kumar 29