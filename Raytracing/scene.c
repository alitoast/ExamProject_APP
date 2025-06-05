/*
Alice Macuz 
SM3201385
*/

#include <stdlib.h>
#include <unistd.h>
#include <float.h>
#include <math.h>
#include "scene.h"

/**
 * Funzione: intersect_ray_sphere
 * Calcola l'intersezione tra un raggio (definito dall'origine e dalla direzione) e una sfera.
 * La funzione risolve l'equazione quadratica del raggio e della sfera.
 *
 * @param origin Origine del raggio (camera).
 * @param direction Direzione del raggio, normalizzata.
 * @param sphere Sfera da testare per l'intersezione.
 * @param t Puntatore a un float che riceverà la distanza dell'intersezione più vicina (se presente).
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
 * Genera l'immagine RGB calcolando il colore di ogni pixel attraverso il calcolo
 * delle intersezioni tra raggi lanciati dalla camera e gli oggetti della scena.
 * Utilizza OpenMP per parallelizzare il rendering dei pixel.
 *
 * @param scene Puntatore alla struttura contenente i dati della scena da renderizzare.
 * @param image Array in cui scrivere i dati RGB dell'immagine (3 byte per pixel).
 * @param width Larghezza dell'immagine in pixel.
 * @param height Altezza dell'immagine in pixel.
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

            // normalizza la direzione del raggio
            float length = sqrtf(direction.x * direction.x + direction.y * direction.y + direction.z * direction.z);
            direction.x /= length;
            direction.y /= length;
            direction.z /= length;

            float nearest_t = FLT_MAX;
            int hit_sphere = -1;

            // verifica intersezioni con tutte le sfere
            for (int s = 0; s < scene->sphere_count; s++) {
                float t;
                if (intersect_ray_sphere(camera, direction, scene->spheres[s], &t)) {
                    if (t < nearest_t) {
                        nearest_t = t;
                        hit_sphere = s;
                    }
                }
            }

            // assegnazione colore del pixel: sfera più vicina o sfondo
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
 * Libera la memoria allocata dinamicamente per le sfere nella scena.
 */
void free_scene(Scene *scene) {
    free(scene->spheres);
}