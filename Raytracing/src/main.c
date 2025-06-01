/*
Alice Macuz 
SM3201385
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "scene.h"
#include "ppm.h"

#define SUCCESS 0
#define ERROR_USAGE 2
#define ERROR_SCENE_LOADING 3
#define ERROR_MEMORY 4
#define ERROR_IMAGE_SAVING 5



int main(int argc, char *argv[]) {
    if (argc != 5) {
        printf("Uso: %s <file scena> <output PPM> <larghezza> <altezza>\n", argv[0]);
        return ERROR_USAGE;
    }

    const char *scene_file = argv[1];
    const char *output_file = argv[2];
    int width = atoi(argv[3]);
    int height = atoi(argv[4]);

    // caricamento scena
    Scene scene;
    load_scene(scene_file, &scene);
    if (!load_scene(scene_file, &scene)) {
        printf("Errore: la scena non è stata caricata correttamente.\n");
        return ERROR_SCENE_LOADING;
    }

    // allocazione memoria
    unsigned char *image = malloc(3 * width * height);
    if (!image) {
        printf("Errore: memoria insufficiente\n");
        free_scene(&scene);
        return ERROR_MEMORY;
    }

    // rendering e salvataggio
    render_scene(&scene, image, width, height);
    if (!save_ppm(output_file, image, width, height)) {
        printf("Errore: salvataggio immagine fallito\n");
        free(image);
        free_scene(&scene);
        return ERROR_IMAGE_SAVING;
    }

    // pulizia ed uscita
    free(image);
    free_scene(&scene);
    printf("Rendering completato! Immagine salvata in %s\n", output_file);
    return SUCCESS;
}
