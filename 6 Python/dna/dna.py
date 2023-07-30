import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py PERSONFILENAME.csv DNAFILENAME.txt")

    # TODO: Read database file into a variable
    people = []
    with open(sys.argv[1], "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for myrow in reader:
            people.append(myrow)

    NUMSTR = len(people[0]) - 1
    strlen = [0] * NUMSTR

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as txtfile:
        dna = txtfile.read()

    # TODO: Find longest match of each STR in DNA sequence
    for i in range(NUMSTR):
        strlen[i] = longest_match(dna, list(people[0].keys())[1 + i])

    # TODO: Check database for matching profiles
    output = "No match"
    for i in range(len(people)):
        mybool = True
        for j in range(NUMSTR):
            if list(people[i].values())[1 + j] != str(strlen[j]):
                mybool = False
        if mybool == True:
            output = people[i]["name"]
            break

    print(output)
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
