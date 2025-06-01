/*
Alice Macuz 
SM3201385
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <float.h>
#include <math.h>
#include "scene.h"

/**
 * Funzione: load_scene
 * Carica una scena da file leggendo i parametri del viewport, il colore di sfondo
 * e l'elenco delle sfere. Alloca la memoria necessaria per le sfere.
 *
 *
 * @param filename Nome del file da cui leggere la scena.
 * @param scene Puntatore alla struttura Scene dove caricare i dati.
 *
 * @return true se il caricamento è avvenuto con successo, false in caso di errore.
 */
bool load_scene(const char *filename, Scene *scene) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        fprintf(stderr,"Errore: impossibile aprire %s\n", filename);
        return false;
    }
    // legge i parametri della scena
    fscanf(file, "VP %f %f %f\n", &scene->viewport_width, &scene->viewport_height, &scene->viewport_distance);
    fscanf(file, "BG %hhu %hhu %hhu\n", &scene->bg_r, &scene->bg_g, &scene->bg_b);
    fscanf(file, "OBJ_N %d\n", &scene->sphere_count);

    printf("Scena caricata correttamente!\n");
    printf("Viewport: %.3f x %.3f, distanza %.3f\n", scene->viewport_width, scene->viewport_height, scene->viewport_distance);
    printf("Colore di sfondo: (%d, %d, %d)\n", (int)scene->bg_r, (int)scene->bg_g, (int)scene->bg_b);
    printf("Numero di sfere: %d\n", scene->sphere_count);

    // alloca memoria per le sfere
    scene->spheres = malloc(scene->sphere_count * sizeof(Sphere));
    if (!scene->spheres) {
        fprintf(stderr, "Errore: L'allocamento della memoria non è andato a buon fine.\n");
        fclose(file);
        return false;
    }
    
    // legge le sfere con contatore per vedere se il numero di sfere corrisponde OBJ_N
    int sphere_count_read = 0; // 
    for (int i = 0; i < scene->sphere_count; i++) {
        Sphere *s = &scene->spheres[i];
        fscanf(file, "S %f %f %f %f %hhu %hhu %hhu\n",
               &s->center.x, &s->center.y, &s->center.z,
               &s->radius, &s->r, &s->g, &s->b);

        printf("Sfera %d - Centro: (%.2f, %.2f, %.2f), Raggio: %.2f, Colore: (%d, %d, %d)\n",
               i + 1, s->center.x, s->center.y, s->center.z, s->radius, s->r, s->g, s->b);
        sphere_count_read++;
    }

    // se c'è un mismatch presenta errore
    if (sphere_count_read != scene->sphere_count) {
        fprintf(stderr, "Errore: Le sfere non corrispondono (expected %d, read %d)\n",
                scene->sphere_count, sphere_count_read);
        free(scene->spheres);
        fclose(file);
        return false;
}

    fclose(file);
    return true;
}


/**
 * Funzione: intersect_ray_sphere
 * Calcola l'intersezione tra un raggio e una sfera.
 * 
 *
 * @param origin Origine del raggio (camera).
 * @param direction Direzione del raggio normalizzata.
 * @param sphere La sfera da testare.
 * @param t Output: distanza dell'intersezione più vicina se esiste.
 * @return 1 se c'è intersezione, 0 altrimenti.
 */
int intersect_ray_sphere(Vector3 origin, Vector3 direction, Sphere sphere, float *t) {
    Vector3 oc = {origin.x - sphere.center.x, origin.y - sphere.center.y, origin.z - sphere.center.z};

    float a = direction.x * direction.x + direction.y * direction.y + direction.z * direction.z;
    float b = 2.0f * (oc.x * direction.x + oc.y * direction.y + oc.z * direction.z);
    float c = oc.x * oc.x + oc.y * oc.y + oc.z * oc.z - sphere.radius * sphere.radius;

    float discriminant = b * b - 4 * a * c;
    if (discriminant < 0) {
        return 0; // nessuna intersezione
    }

    float t0 = (-b - sqrtf(discriminant)) / (2.0f * a);
    float t1 = (-b + sqrtf(discriminant)) / (2.0f * a);

    *t = (t0 > 0) ? t0 : t1;
    return (*t > 0);
}


/**
 * Funzione: render_scene
 * Genera l'immagine calcolando il colore di ciascun pixel in base alle intersezioni
 * tra i raggi lanciati dalla camera e gli oggetti della scena.
 * Utilizza OpenMP per parallelizzare il rendering dei pixel.
 *
 *
 * @param scene puntatore alla struttura scena da renderizzare
 * @param image array in cui scrivere i dati RGB dell'immagine
 * @param width larghezza dell'immagine in pixel
 * @param height altezza dell'immagine in pixel
 */
void render_scene(Scene *scene, unsigned char *image, int width, int height) {
    Vector3 camera = {0, 0, 0}; // la camera è sempre all'origine

    float aspect_ratio = (float)width / height;
    float viewport_w = scene->viewport_width;
    float viewport_h = viewport_w / aspect_ratio;
    float focal_length = scene->viewport_distance;

    #pragma omp parallel for schedule(dynamic)
    for (int j = 0; j < height; j++) {
        for (int i = 0; i < width; i++) {
            // calcolo direzione del raggio
            float u = (i - width / 2.0f) * (viewport_w / width);
            float v = (j - height / 2.0f) * (viewport_h / height);
            Vector3 direction = {u, v, focal_length};
            // normalizza il vettore
            float length = sqrtf(direction.x * direction.x + direction.y * direction.y + direction.z * direction.z);
            direction.x /= length;
            direction.y /= length;
            direction.z /= length;

            float nearest_t = FLT_MAX;
            int hit_sphere = -1;

            // controlla intersezioni
            for (int s = 0; s < scene->sphere_count; s++) {
                float t;
                if (intersect_ray_sphere(camera, direction, scene->spheres[s], &t)) {
                    if (t < nearest_t) {
                        nearest_t = t;
                        hit_sphere = s;
                    }
                }
            }

            int index = (j * width + i) * 3;
            if (hit_sphere >= 0) {
                image[index] = scene->spheres[hit_sphere].r;
                image[index + 1] = scene->spheres[hit_sphere].g;
                image[index + 2] = scene->spheres[hit_sphere].b;
            } else {
                image[index] = scene->bg_r;
                image[index + 1] = scene->bg_g;
                image[index + 2] = scene->bg_b;
            }
        }
    }
}

/*
 * Funzione: free_scene
 * Libera la memoria allocata per le sfere nella scena.
 */
void free_scene(Scene *scene) {
    free(scene->spheres);
}