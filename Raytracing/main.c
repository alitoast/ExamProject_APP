/*
Alice Macuz 
SM3201385
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "load_scene.h"
#include "scene.h"
#include "ppm.h"

#define SUCCESS 0
#define ERROR_USAGE 2
#define ERROR_SCENE_LOADING 3
#define ERROR_MEMORY 4
#define ERROR_IMAGE_SAVING 5

/**
 * Funzione: main
 * Punto di ingresso del programma.
 * 
 * Questa funzione gestisce l'intero flusso di lavoro del raytracer:
 * 1. Verifica l'uso corretto del programma.
 * 2. Carica la scena da un file.
 * 3. Alloca memoria per l'immagine.
 * 4. Renderizza la scena.
 * 5. Salva l'immagine in formato PPM.
 * 6. Libera le risorse allocate.
 *
 * @param argc Numero di argomenti passati alla riga di comando.
 * @param argv Array di stringhe contenenti gli argomenti.
 *
 * @return 0 in caso di successo, codice di errore altrimenti.
 */
int main(int argc, char *argv[]) {
    // verifica numero argomenti
    if (argc != 5) {
        fprintf(stderr,"Errore: l'utilizzo corretto è: %s <file scena> <output PPM> <larghezza> <altezza>\n", argv[0]);
        return ERROR_USAGE;
    }

    // parsing degli argomenti della riga di comando
    const char *scene_file = argv[1];
    const char *output_file = argv[2];
    int width = atoi(argv[3]);
    int height = atoi(argv[4]);

    // caricamento scena
    Scene scene;
    if (!load_scene(scene_file, &scene)) {
        fprintf(stderr,"Errore: la scena non è stata caricata correttamente.\n");
        return ERROR_SCENE_LOADING;
    }

    // allocazione memoria
    unsigned char *image = malloc(3 * width * height);
    if (!image) {
        fprintf(stderr,"Errore: memoria insufficiente\n");
        free_scene(&scene);
        return ERROR_MEMORY;
    }

    // rendering 
    render_scene(&scene, image, width, height);

    // salvataggio
    if (!save_ppm(output_file, image, width, height)) {
        fprintf(stderr,"Errore: salvataggio immagine fallito\n");
        free(image);
        free_scene(&scene);
        return ERROR_IMAGE_SAVING;
    }

    // pulizia ed uscita
    free(image);
    free_scene(&scene);
    fprintf(stderr,"Rendering completato! Immagine salvata in %s\n", output_file);
    return SUCCESS;
}
