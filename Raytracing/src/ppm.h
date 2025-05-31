/*
Alice Macuz 
SM3201385
*/

#ifndef PPM_H
#define PPM_H

#include <stdbool.h>
#include "scene.h"

bool save_ppm(const char *filename, unsigned char *image, int width, int height);

#endif
