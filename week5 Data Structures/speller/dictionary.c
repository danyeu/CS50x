// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 27 * 27;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    char upper[LENGTH + 1] = {0};

    for (int i = 0; i < LENGTH; i++)
    {
        upper[i] = toupper(word[i]);
    }

    node *ptr = table[hash(upper)];

    while (ptr != NULL)
    {
        if (strcasecmp(word, ptr->word) == 0)
        {
            return true;
        }
        ptr = ptr->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int number = 0;
    for (int i = 0; i < 2; i++)
    {
        if (word[i] == 0)
        {
            i = 999;
        }
        else if (word[i] == 39)
        {
            number += 27;
        }
        else
        {
            number += toupper(word[i]) - 64;
        }
    }
    return number;
}

int wcount = 0;

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];

    while (fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            unload();
            return false;
        }

        strcpy(n->word, word);

        hash(n->word);

        if (table[hash(n->word)] == NULL)
        {
            table[hash(n->word)] = n;
            wcount++;
        }
        else
        {
            n->next = table[hash(n->word)];
            table[hash(n->word)] = n;
            wcount++;
        }
    }

    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return wcount;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *ptr = table[i];

        while (ptr != NULL)
        {
            node *tmp = ptr;
            ptr = ptr->next;
            free(tmp);
        }
        free(ptr);
    }
    return true;
}
