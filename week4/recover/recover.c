#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Filename
    char *inputfile = argv[1];

    // Open input file
    FILE *input = fopen(inputfile, "r");
    if (input == NULL)
    {
        printf("Could not open %s.\n", inputfile);
        return 1;
    }

    char *filename = malloc(8 * sizeof(char));
    unsigned char *buffer = malloc(512 * sizeof(unsigned char));
    int isjpg = 0;
    int o = -1;
    FILE *output;
    while (fread(buffer, 1, 512, input) == 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (o >= 0)
            {
                fclose(output);
            }
            isjpg = 1;
            o++;
            sprintf(filename, "%03i.jpg", o);
            // Open output file
            output = fopen(filename, "w");
            if (output == NULL)
            {
                fclose(input);
                printf("Could not create %s.\n", filename);
                return 1;
            }
        }
        if (isjpg == 1)
        {
            fwrite(buffer, 1, 512, output);
        }

    }
    fclose(input);
    fclose(output);
    free(filename);
    free(buffer);
    return 0;
}