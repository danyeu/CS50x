#include <cs50.h>
#include <math.h>
#include <stdio.h>

int luhn(long cardnumber, long numdigits);

int main(void)
{
    long number;
    number = get_long("Number: ");

    if (number < 4000000000000 || number > 5599999999999999)
    {
        printf("INVALID\n");
    }
    else
    {
        long digits;
        for (int i = 13; i < 17; i++)
        {
            if ((number * 10) >= pow(10, i))
            {
                digits = i;
            }
        }

        if (digits == 14)
        {
            printf("INVALID\n");
        }
        else
        {
            if (luhn(number, digits) == 0)
            {
                printf("INVALID\n");
            }
            else
            {
                //check for visa, amex, mastercard
                float firstnums;
                float firstnums2;

                if (digits == 13)
                {
                    //if 13 and starts 4; visa
                    firstnums = (int)(number / 1e12);
                    if (firstnums == 4)
                    {
                        printf("VISA\n");
                    }
                    else
                    {
                        printf("INVALID\n");
                    }
                }
                else if (digits == 15)
                {
                    //if 15 and starts 34 37; amex
                    firstnums = (int)(number / 1e13);
                    if (firstnums == 34 || firstnums == 37)
                    {
                        printf("AMEX\n");
                    }
                    else
                    {
                        printf("INVALID\n");
                    }
                }
                else if (digits == 16)
                {
                    //if 16 and starts 4; visa, or starts 51-55; mastercard
                    firstnums = (int)(number / 1e14);
                    firstnums2 = (int)(number / 1e15);
                    if (firstnums == 51 || firstnums == 52 || firstnums == 53 || firstnums == 54 || firstnums == 55)
                    {
                        printf("MASTERCARD\n");
                    }
                    else if (firstnums2 == 4)
                    {
                        printf("VISA\n");
                    }
                    else
                    {
                        printf("INVALID\n");
                    }
                }
                else
                {
                    printf("INVALID\n");
                }
            }
        }
    }
}

int luhn(long cardnumber, long numdigits)
{
    long newcardnumber = cardnumber;
    long lastdigit = 0;
    long sumeven = 0;
    long sumodd = 0;

    for (int i = 1; i < numdigits + 1; i++)
    {
        lastdigit = newcardnumber % 10;

        if (i % 2 > 0)
        {
            //if odd
            sumodd = sumodd + lastdigit;
        }
        else
        {
            //if even
            sumeven = sumeven + (long)((2 * lastdigit) / 10);
            sumeven = sumeven + ((2 * lastdigit) % 10);
        }
        newcardnumber = (long)(newcardnumber / 10);
    }

    sumeven = sumeven + sumodd;

    if (sumeven % 10 == 0)
    {
        return (1);
    }
    else
    {
        return (0);
    }
}