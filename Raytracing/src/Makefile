CC = gcc
CFLAGS = -Wall -O2 -fopenmp
LDFLAGS = -lm
EXEC = raytracer

SRC = main.c scene.c ppm.c
OBJ = $(SRC:.c=.o)

all: $(EXEC)

$(EXEC): $(OBJ)
	$(CC) $(CFLAGS) -o $(EXEC) $(OBJ) $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@


.PHONY: all clean
clean:
	rm -f $(OBJ) $(EXEC)

.PHONY: run
run: $(EXEC)
	./$(EXEC) scene.txt output.ppm 1920 1080

convert: output.ppm
	convert $< output.png
	