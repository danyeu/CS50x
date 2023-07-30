#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int avg;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            avg = round(((image[i][j].rgbtRed + image[i][j].rgbtBlue + image[i][j].rgbtGreen) / 3.0));
            if (avg > 255)
            {
                avg = 255;
            }
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int newr;
    int newg;
    int newb;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            newr = round(0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue);
            newg = round(0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue);
            newb = round(0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue);
            if (newr > 255)
            {
                newr = 255;
            }
            if (newg > 255)
            {
                newg = 255;
            }
            if (newb > 255)
            {
                newb = 255;
            }
            image[i][j].rgbtRed = newr;
            image[i][j].rgbtBlue = newb;
            image[i][j].rgbtGreen = newg;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmpimage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            tmpimage[i][j].rgbtRed = image[i][width - 1 - j].rgbtRed;
            tmpimage[i][j].rgbtBlue = image[i][width - 1 - j].rgbtBlue;
            tmpimage[i][j].rgbtGreen = image[i][width - 1 - j].rgbtGreen;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = tmpimage[i][j].rgbtRed;
            image[i][j].rgbtBlue = tmpimage[i][j].rgbtBlue;
            image[i][j].rgbtGreen = tmpimage[i][j].rgbtGreen;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmpimage[height][width];
    int tmpr;
    int tmpg;
    int tmpb;
    int count;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            tmpr = 0;
            tmpg = 0;
            tmpb = 0;
            count = 0;
            for (int k = -1; k <= 1; k++)
            {
                for (int l = -1; l <= 1; l++)
                {
                    if ((i + k >= 0) && (i + k <= height - 1) && (j + l >= 0) && (j + l <= width - 1))
                    {
                        tmpr += image[i + k][j + l].rgbtRed;
                        tmpg += image[i + k][j + l].rgbtGreen;
                        tmpb += image[i + k][j + l].rgbtBlue;
                        count++;
                    }
                }
            }
            tmpr = round(tmpr / (count * 1.0));
            tmpb = round(tmpb / (count * 1.0));
            tmpg = round(tmpg / (count * 1.0));
            tmpimage[i][j].rgbtRed = tmpr;
            tmpimage[i][j].rgbtBlue = tmpb;
            tmpimage[i][j].rgbtGreen = tmpg;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = tmpimage[i][j].rgbtRed;
            image[i][j].rgbtBlue = tmpimage[i][j].rgbtBlue;
            image[i][j].rgbtGreen = tmpimage[i][j].rgbtGreen;
        }
    }
    return;
}
