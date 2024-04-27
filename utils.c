#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "betterrand.c"

typedef struct {
    int r;
    int g;
    int b;
}RGB;

RGB* random_rgb(){
    RGB* color = malloc(sizeof(RGB));
    color->r = realrand(0,255);
    color->g = realrand(0,255);
    color->b = realrand(0,255);
    return color;
}

int getRGB_distance(RGB* userRGB, RGB* otherRGB){
    return (int)sqrt(pow((userRGB->r - otherRGB->r),2) + pow((userRGB->g - otherRGB->g),2) +pow((userRGB->b - otherRGB->b),2));

}


void free_memory(RGB *color){
    free(color);
}



