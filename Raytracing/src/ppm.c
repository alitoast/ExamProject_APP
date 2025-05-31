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

bool save_ppm(const char *filename, unsigned char *image, int width, int height) {
    // crea file se non esiste, sovrascrivi se esiste; con permessi di lettura e scrittura per tutti
    int fd = open(filename, O_RDWR | O_CREAT | O_TRUNC, 0666);
    if (fd < 0) {
        perror("Errore: impossibile aprire il file per scrittura");
        return false;
    }

    char header[64];
    int header_len = snprintf(header, sizeof(header), "P6\n%d %d\n255\n", width, height);
    size_t image_size = width * height * 3;
    size_t file_size = header_len + image_size;

    // ridimensiona il file alla dimensione necessaria
    if (ftruncate(fd, file_size) == -1) {
        perror("Errore: ridimensionamento fallito");
        close(fd);
        return false;
    }

    // mappa il file in memoria
    void *map = mmap(NULL, file_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (map == MAP_FAILED) {
        perror("Errore: mmap fallito");
        close(fd);
        return false;
    }

    // copia l'intestazione nella memoria mappata e subito dopo i dati
    memcpy(map, header, header_len);
    memcpy((unsigned char *)map + header_len, image, image_size);

    // sincronizza le modifiche su disco
    if (msync(map, file_size, MS_SYNC) == -1) {
        perror("Errore: sincronizzazione con disco fallita");
    }

    // libera la memoria e chiudi il file
    if (munmap(map, file_size) == -1) {
        perror("Errore: munmap fallito");
    }
    close(fd);

    return true;
}
