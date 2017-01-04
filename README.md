# Image-To-ASCII
Convert images to ASCII art.


## Usage

```

    Usage:
        main.py [image] [width]
    Parameters:
        [image]   The image to convert. Supports many formats.
        [width]   The width of the regions from the image to convert to ascii.
                  The height is by default the width multiplied by two.
    Example:
        main.py sample/gold_face.jpg 2
         - This loads the image gold_face.jpg from the "sample" directory.
         - It then divides the image into 2 pixel by 4 pixel regions.
         - Each region is then converted to a character.
         
```

## Sample
![alt-tag] (sample/gold_face.jpg)
![alt-tag] (sample/gold_face_ascii_screenshot.png)
