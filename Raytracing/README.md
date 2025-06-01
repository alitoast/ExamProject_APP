# Raytracing


## **Description**
This project is a Raytracer implemented in C, it renders scenes described in a text file to PPM format. It supports:
- Loading scene data (viewport, background, spheres).
- Raytracing to compute pixel colors.
- Saving the rendered image in PPM format.
- Optional conversion to **PNG** using ImageMagick.


---

## **How to Compile and Run**
### 1. **Build the Project**
```bash
cd Raytracing/src
make
```
- This compiles `main.c`, `scene.c`, and `ppm.c` into an executable named `raytracer`.

### 2. **Run the Program**
```bash
make run
```
Executes the raytracer with default arguments:  
  ```bash
  ./raytracer scene.txt output.ppm 1920 1080
  ```

Otherwise execute the program with custom scene_file, output_file and dimensions using:
```bash
./raytracer <scene_file> <output_file> <width> <height>
```

### 3. **Convert PPM to PNG (Optional)**
```bash
make convert
```
Converts automatically `output.ppm` to `output.png`. (Ensure ImageMagick is installed).

### 4. **Clean Up**
```bash
make clean
```
Removes compiled files (`raytracer`, `.o`, `output.ppm`, `output.png`).

---


## **Dependencies**
- **GCC** (C compiler).
- **OpenMP** (for parallel rendering).
- **ImageMagick** (optional, for PPM-to-PNG conversion).
  
     On Ubuntu/Debian run:
  
    ```bash
    sudo apt update
    sudo apt install imagemagick
    ```

    On macOS (with Homebrew):

    ```bash
    brew install imagemagick
    ```


