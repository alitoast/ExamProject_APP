/*
Alice Macuz 
SM3201385
*/

#ifndef SCENE_H
#define SCENE_H

#include <stdint.h>
#include <stdbool.h>

// vettori 3D, sfere e scena

typedef struct {
    float x, y, z;
} Vector3;

typedef struct {
    Vector3 center;
    float radius;
    uint8_t r, g, b; 
} Sphere;

typedef struct {
    float viewport_width, viewport_height, viewport_distance;
    uint8_t bg_r, bg_g, bg_b;
    int sphere_count;
    Sphere *spheres;
} Scene;

int intersect_ray_sphere(Vector3 origin, Vector3 direction, Sphere sphere, float *t);
void render_scene(Scene *scene, unsigned char *image, int width, int height);
void free_scene(Scene *scene);
#endif