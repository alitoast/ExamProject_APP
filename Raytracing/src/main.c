#include <stdio.h>
#include <stdlib.h>
#include "scene/scene.h"


int main(int argc, char *argv[]) {
    if (argc != 5) {
        printf("Uso: %s <file scena> <output PPM> <larghezza> <altezza>\n", argv[0]);
        return 1;
    }

    const char *scene_file = argv[1];
    const char *output_file = argv[2];
    int width = atoi(argv[3]);
    int height = atoi(argv[4]);

    Scene scene;
    load_scene(scene_file, &scene);

    unsigned char *image = malloc(3 * width * height);
    if (!image) {
        printf("Errore: memoria insufficiente\n");
        return 1;
    }

    render_scene(&scene, image, width, height);
    save_ppm(output_file, image, width, height);

    free(image);
    free(scene.spheres);

    printf("Rendering completato! Immagine salvata in %s\n", output_file);
    return 0;
}
