#include <cs50.h>
#include <stdio.h>

void blocks(string s, int n);

int main(void)
{
    int n = 0;
    while (n > 8 || n < 1)
    {
        n = get_int("Height: ");
    }

    for (int i = 1; i <= n; i++)
    {
        blocks(" ", n - i);
        blocks("#", i);
        printf("  ");
        blocks("#", i);
        printf("\n");
    }
}

void blocks(string s, int n)
{
    for (int j = 0; j < n; j++)
    {
        printf("%s", s);
    }
}