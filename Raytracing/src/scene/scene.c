#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include "scene.h"

void load_scene(const char *filename, Scene *scene) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        printf("Errore: impossibile aprire %s\n", filename);
        exit(1);
    }

    fscanf(file, "VP %f %f %f\n", &scene->viewport_width, &scene->viewport_height, &scene->viewport_distance);
    fscanf(file, "BG %hhu %hhu %hhu\n", &scene->bg_r, &scene->bg_g, &scene->bg_b);
    fscanf(file, "OBJ_N %d\n", &scene->sphere_count);

    printf("Scena caricata correttamente!\n");
    printf("Viewport: %.3f x %.3f, distanza %.3f\n", scene->viewport_width, scene->viewport_height, scene->viewport_distance);
    printf("Colore di sfondo: (%d, %d, %d)\n", scene->bg_r, scene->bg_g, scene->bg_b);
    printf("Numero di sfere: %d\n", scene->sphere_count);

    scene->spheres = malloc(scene->sphere_count * sizeof(Sphere));
    if (!scene->spheres) {
        fprintf(stderr, "Errore: L'allocamento della memoria non è andato a buon fine.\n");
        exit(1);
    }
    
    int sphere_count_read = 0; //what if the number of spheres in the file doesn't match OBJ_N
    for (int i = 0; i < scene->sphere_count; i++) {
        Sphere *s = &scene->spheres[i];
        fscanf(file, "S %f %f %f %f %hhu %hhu %hhu\n",
               &s->center.x, &s->center.y, &s->center.z,
               &s->radius, &s->r, &s->g, &s->b);

        printf("Sfera %d - Centro: (%.2f, %.2f, %.2f), Raggio: %.2f, Colore: (%d, %d, %d)\n",
               i + 1, s->center.x, s->center.y, s->center.z, s->radius, s->r, s->g, s->b);
        sphere_count_read++;
    }

    if (sphere_count_read != scene->sphere_count) {
    fprintf(stderr, "Errore: Le sfere con corrispondono (expected %d, read %d)\n",
            scene->sphere_count, sphere_count_read);
    exit(1);
}

    fclose(file);
}