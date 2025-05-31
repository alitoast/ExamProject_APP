CC = gcc
CFLAGS = -Wall -O2 -fopenmp
LDFLAGS = -lm
OBJ = main.o scene.o ppm.o
EXEC = raytracer

all: $(EXEC)

$(EXEC): $(OBJ)
	$(CC) $(CFLAGS) -o $(EXEC) $(OBJ) $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(EXEC)
