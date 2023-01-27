#include <cs50.h>
#include <stdio.h>
#include <ctype.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");

    float score = (0.0588 * (count_letters(text) * (100.0 / count_words(text)))) -
                  (0.296 * (count_sentences(text) * (100.0 / count_words(text)))) -
                  15.8;

    if (score < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (score >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %.0f\n", score);
    }
}

int count_letters(string text)
{
    int n = 0;
    int c = 0;
    while (text[n] != '\0')
    {
        if isalpha(text[n])
        {
            c++;
        }
        n++;
    }

    return c;
}

int count_words(string text)
{
    int n = 0;
    int c = 0;
    while (text[n] != '\0')
    {
        if ((int) text[n] == 32)
        {
            c++;
        }
        n++;
    }

    c++;
    return c;
}

int count_sentences(string text)
{
    int n = 0;
    int c = 0;
    while (text[n] != '\0')
    {
        if ((int) text[n] == 33 || (int) text[n] == 63 || (int) text[n] == 46)
        {
            c++;
        }
        n++;
    }

    return c;
}