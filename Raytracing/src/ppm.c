/*
Alice Macuz 
SM3201385
*/

#include <stdio.h>
#include <stdlib.h>
#include "ppm.h"

void save_ppm(const char *filename, unsigned char *image, int width, int height) {
    FILE *file = fopen(filename, "wb");
    if (!file) {
        printf("Errore: impossibile scrivere %s\n", filename);
        exit(1);
    }

    fprintf(file, "P6\n%d %d\n255\n", width, height);
    fwrite(image, 3, width * height, file);
    fclose(file);
}
