/*
Alice Macuz 
SM3201385
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <string.h>
#include "ppm.h"


/**
 * Funzione: save_ppm
 * Crea un file di output in formato binario PPM, mappa il file
 * in memoria, scrive l'header e i dati dell'immagine in memoria condivisa, e
 * infine sincronizza il contenuto su disco.
 *
 *
 * @param filename Nome del file di output.
 * @param image Puntatore a un array contenente i dati RGB (3 byte per pixel).
 * @param width Larghezza dell'immagine in pixel.
 * @param height Altezza dell'immagine in pixel.
 * @return true se l'immagine è stata salvata correttamente, false in caso di errore.
 */
bool save_ppm(const char *filename, unsigned char *image, int width, int height) {
    int fd = open(filename, O_RDWR | O_CREAT | O_TRUNC, 0666);
    if (fd < 0) {
        printf("Errore: impossibile aprire il file per scrittura");
        return false;
    }

    char header[64];
    int header_len = snprintf(header, sizeof(header), "P6\n%d %d\n255\n", width, height);
    size_t image_size = width * height * 3;
    size_t file_size = header_len + image_size;

    // ridimensiona il file alla dimensione necessaria
    if (ftruncate(fd, file_size) == -1) {
        printf("Errore: ridimensionamento fallito");
        close(fd);
        return false;
    }

    // mappa il file in memoria
    void *map = mmap(NULL, file_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (map == MAP_FAILED) {
        printf("Errore: mmap fallito");
        close(fd);
        return false;
    }

    // copia l'intestazione nella memoria mappata e subito dopo i dati
    memcpy(map, header, header_len);
    memcpy((unsigned char *)map + header_len, image, image_size);

    // sincronizza le modifiche su disco
    if (msync(map, file_size, MS_SYNC) == -1) {
        printf("Errore: sincronizzazione con disco fallita");
    }

    // libera la memoria e chiudi il file
    if (munmap(map, file_size) == -1) {
        printf("Errore: munmap fallito");
    }
    close(fd);

    return true;
}
