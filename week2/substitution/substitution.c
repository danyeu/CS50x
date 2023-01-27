#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else
    {
        long n = 0;
        int alpha = 0;
        int nonalpha = 0;
        while (argv[1][n] != '\0')
        {
            if (isalpha(argv[1][n]))
            {
                alpha++;
            }
            else
            {
                nonalpha++;
            }
            n++;
        }
        if (nonalpha > 0 || alpha != 26)
        {
            printf("Key must contain 26 letters.\n");
            return 1;
        }
        else
        {
            char key[25];
            n = 0;
            while (argv[1][n] != '\0')
            {
                key[n] = tolower(argv[1][n]);
                n++;
            }

            int dupe = 0;
            for (int i = 0; i < 26; i++)
            {
                if (i > 0)
                {
                    for (int j = 0; j < i; j++)
                    {
                        if (key[i] == key[j])
                        {
                            dupe = 1;
                        }
                    }
                }
            }
            if (dupe == 1)
            {
                printf("Key must contain 26 unique letters.\n");
                return 1;
            }
            else
            {
                //ask for input
                string input = get_string("plaintext: ");
                //convert input
                char output[strlen(input) + 1];
                n = 0;
                char lower;
                while (input[n] != '\0')
                {
                    if isalpha(input[n])
                    {
                        lower = tolower(input[n]);
                        if isupper(input[n])
                        {
                            output[n] = toupper(key[(int)(lower) - 97]);
                        }
                        else
                        {
                            output[n] = key[(int)(lower) - 97];
                        }

                    }
                    else
                    {
                        output[n] = input[n];
                    }
                    n++;
                }
                //"hello" has strlen = 5 (it exludes '\0'). array[5] has 5 slots [0-4]. must add one slot for 6th [5] char '\0'
                output[strlen(input)] = '\0';
                //output converted
                printf("ciphertext: %s\n", output);
            }
        }
    }
k    return 0;
}