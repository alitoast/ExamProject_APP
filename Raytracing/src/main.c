/*
Alice Macuz 
SM3201385
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "scene.h"
#include "ppm.h"

int main(int argc, char *argv[]) {
    if (argc != 5) {
        printf("Uso: %s <file scena> <output PPM> <larghezza> <altezza>\n", argv[0]);
        return 1;
    }

    const char *scene_file = argv[1];
    const char *output_file = argv[2];
    int width = atoi(argv[3]);
    int height = atoi(argv[4]);

    // caricamento scena
    Scene scene;
    load_scene(scene_file, &scene);
    if (!load_scene(scene_file, &scene)) {
        return 1;
    }

    // allocazione memoria
    unsigned char *image = malloc(3 * width * height);
    if (!image) {
        printf("Errore: memoria insufficiente\n");
        free_scene(&scene);
        return 1;
    }

    // rendering e salvataggio
    render_scene(&scene, image, width, height);
    save_ppm(output_file, image, width, height);
    if (!save_ppm(output_file, image, width, height)) {
        fprintf(stderr, "Errore: salvataggio immagine fallito\n");
        free(image);
        free_scene(&scene);
        return 1;
    }

    // pulizia ed uscita
    free(image);
    free_scene(&scene);
    printf("Rendering completato! Immagine salvata in %s\n", output_file);
    return 0;
}
