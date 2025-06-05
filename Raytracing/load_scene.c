/*
Alice Macuz 
SM3201385
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <float.h>
#include "load_scene.h"
#include "scene.h"

/**
 * Funzione: load_scene
 * Carica una scena da file di testo, leggendo i parametri del viewport, il colore di sfondo
 * e l'elenco delle sfere. Alloca dinamicamente la memoria necessaria per le sfere e
 * e verifica la correttezza del formato del file.
 *
 * @param filename Nome del file di input contenente la descrizione della scena.
 * @param scene Puntatore alla struttura dove caricare i dati.
 *
 * @return true se il caricamento è avvenuto con successo, false altrimenti.
 */
bool load_scene(const char *filename, Scene *scene) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        fprintf(stderr,"Errore: impossibile aprire %s\n", filename);
        return false;
    }

    // lettura parametri viewport
    if (fscanf(file, "VP %f %f %f\n", &scene->viewport_width, &scene->viewport_height, &scene->viewport_distance) != 3) {
        fprintf(stderr, "Errore: formato file non valido (VP)\n");
        fclose(file);
        return false;
    }

    // lettura colore background 
    if (fscanf(file, "BG %hhu %hhu %hhu\n", &scene->bg_r, &scene->bg_g, &scene->bg_b) != 3) {
        fprintf(stderr, "Errore: formato file non valido (BG)\n");
        fclose(file);
        return false;
    }

    // lettura conta sfere
    if (fscanf(file, "OBJ_N %d\n", &scene->sphere_count) != 1) {
        fprintf(stderr, "Errore: formato file non valido (OBJ_N)\n");
        fclose(file);
        return false;
    }

    printf("Scena caricata correttamente!\n");
    printf("Viewport: %.3f x %.3f, distanza %.3f\n", scene->viewport_width, scene->viewport_height, scene->viewport_distance);
    printf("Colore di sfondo: (%d, %d, %d)\n", (int)scene->bg_r, (int)scene->bg_g, (int)scene->bg_b);
    printf("Numero di sfere: %d\n", scene->sphere_count);

    // allocazione dinamica memoria per le sfere
    scene->spheres = malloc(scene->sphere_count * sizeof(Sphere));
    if (!scene->spheres) {
        fprintf(stderr, "Errore: L'allocamento della memoria non è andato a buon fine.\n");
        fclose(file);
        return false;
    }
    
    // lettura le sfere con contatore 
    int sphere_count_read = 0; // 
    for (int i = 0; i < scene->sphere_count; i++) {
        Sphere *s = &scene->spheres[i];

        // lettura dei dati di una singola sfera
        if (fscanf(file, "S %f %f %f %f %hhu %hhu %hhu\n",
               &s->center.x, &s->center.y, &s->center.z,
               &s->radius, &s->r, &s->g, &s->b) != 7) {
        fprintf(stderr, "Errore: formato file non valido (S)\n");
        free(scene->spheres);
        fclose(file);
        return false;
        }
        
        // stampa informazioni per ogni sfera
        printf("Sfera %d - Centro: (%.2f, %.2f, %.2f), Raggio: %.2f, Colore: (%d, %d, %d)\n",
               i + 1, s->center.x, s->center.y, s->center.z, s->radius, s->r, s->g, s->b);
        sphere_count_read++;
    }

    // verifica che il numero di sfere lette corrisponda a OBJ_N
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