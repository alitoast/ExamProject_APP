# Raytracing


## **Description**
This project is a Raytracer implemented in C, it renders scenes described in a text file to PPM format. It supports:
- Loading scene data (viewport, background, spheres).
- Raytracing to compute pixel colors.
- Saving the rendered image in PPM format.
- Optional conversion to **PNG** using ImageMagick.

---
## **Code Structure**


- `main.c`: Parses command-line arguments, loads the scene, renders, and saves the output.
- `load_scene.c`: Handles reading and parsing the scene file, including viewport, background color, and object data.
- `load_scene.h`: Declares the load_scene function used to load scene data from a .txt file.
- `scene.c`: Contains ray-sphere intersection function and rendering logic.
- `scene.h`: Defines core data structures and function prototypes used throughout the project.
- `ppm.c`: Implements saving the rendered image as a PPM file using memory-mapped I/O.
- `ppm.h`: Declares the interface for saving the rendered image in PPM format.  
- `Makefile`: Defines compilation rules for building and running the project.


---

## **How to Compile and Run**

The scene file is a text file containing the description of the scene. To test the program, you can use the provided `scene.txt` file.

### 1. **Build the Project**

```bash
make
```
- This compiles `main.c`, `load_scene.c`, `scene.c`, and `ppm.c` into an executable named `raytracer`.

### 2. **Run the Program**
```bash
make run
```
- Executes the raytracer with default arguments:  
  ```bash
  ./raytracer scene.txt output.ppm 1920 1080
  ```

- Otherwise execute the program with custom scene_file, output_file and dimensions (width and height) using:
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
Removes compiled files (`raytracer`, `.o`).

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

---

## **Error Codes**

The program returns the following errors if they arise:

| **Error Code** | **Error Name**        | **Description**                |
| -------------- | --------------------- | ------------------------------ |
| 0            | `SUCCESS`             | Program executed successfully. |
| 2            | `ERROR_USAGE`         | Incorrect command-line usage.  |
| 3            | `ERROR_SCENE_LOADING` | Failed to load the scene file. |
| 4            | `ERROR_MEMORY`        | Failed to allocate memory.      |
| 5            | `ERROR_IMAGE_SAVING`  | Failed to save the image.      |
