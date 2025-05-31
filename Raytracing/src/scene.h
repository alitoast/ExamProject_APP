#ifndef SCENE_H
#define SCENE_H

#include <stdint.h>

// 3D vectors, spheres and scene

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

void load_scene(const char *filename, Scene *scene); //reads scene from file txt

#endif