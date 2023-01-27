from cs50 import get_string


def main():
    text = get_string("Text: ")

    score = (0.0588 * (count_letters(text) * (100 / count_words(text)))) - \
        (0.296 * (count_sentences(text) * (100 / count_words(text)))) - \
        15.8

    if score < 1:
        print("Before Grade 1")
    elif score >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {score:.0f}")


def count_letters(txt):
    counter = 0
    for i in range(len(txt)):
        if txt[i].isalpha():
            counter += 1
    return counter


def count_words(txt):
    counter = 1
    for i in range(len(txt)):
        if txt[i] == " ":
            counter += 1
    return counter


def count_sentences(txt):
    counter = 0
    for i in range(len(txt)):
        if txt[i] == "." or txt[i] == "!" or txt[i] == "?":
            counter += 1
    if counter == 0:
        counter = 1
    return counter


main()