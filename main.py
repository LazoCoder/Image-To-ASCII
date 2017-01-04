# Convert an image to ASCII.

from PIL import Image, ImageDraw, ImageFont
from sys import argv

# The region is the size of the pieces that the image will be split into.
# If width is set to 1 then the image will be divided into 1px x 2px
# pieces. Each piece will then be converted to an ASCII character.
WIDTH_OF_REGION = 1
HEIGHT_OF_REGION = int(WIDTH_OF_REGION * 2)

# The map will be generated.
# The keys will be gray values scaled up to 0 to 10,000.
# The values will be characters that contain those gray values.
char_map = {}


def char_image(char):
    # Get an image with a char drawn on it.
    font = ImageFont.truetype("Monaco", 40)
    image = Image.new('RGB', (50, 50), (255, 255, 255))
    drawer = ImageDraw.Draw(image)
    drawer.text((0, 0), char, font=font, fill=(0, 0, 0))
    image = image.convert('1')
    return image


def avg_gray_value(image):
    # Get the mean gray value of an image.
    width, height = image.size
    total_pixels_value = width * height * 255
    gray_value = 0
    for x in range(0, width):
        for y in range(0, height):
            gray_value += image.getpixel((x, y))
    return int(gray_value/total_pixels_value*10000)


def split_image(image):
    # Split up the image into regions and a return a list with all of them.
    regions = []
    count = 0
    for y in range(0, image.height-HEIGHT_OF_REGION, HEIGHT_OF_REGION):
        count += 1
        for x in range(0, image.width-WIDTH_OF_REGION, WIDTH_OF_REGION):
            rect = (x, y, x + WIDTH_OF_REGION, y + HEIGHT_OF_REGION)
            regions.append(image.crop(rect))
    return regions


def create_char_map(start_index, end_index):
    # Create the map that will link gray values to characters.
    load_characters(start_index, end_index)
    normalize_char_map()
    fill_char_map()


def load_characters(start_index, end_index):
    # Load characters with unique gray values to the character map.
    for i in range(start_index, end_index):
        char_img = char_image(chr(i))
        grey_val = avg_gray_value(char_img)
        if grey_val not in char_map:
            temp = {grey_val: chr(i)}
            char_map.update(temp)


def normalize_char_map():
    # Spread out the values so that the darkest is 0 and lightest is 10,0000.
    global char_map
    temp_map = {}
    max = 0
    min = 10000
    for val in char_map:
        if val > max:
            max = val
        if val < min:
            min = val
    for val in char_map:
        tmp_val = int(((10000-0)*(val-min)) / (max-min) + 0)
        temp_map.update({tmp_val: char_map.get(val)})
    char_map = temp_map


def fill_char_map():
    # Make sure there are no blank values. This increases the speed.
    recent = None
    for i in range(0, 10001):
        if i in char_map:
            recent = i
        else:
            char_map.update({i: char_map.get(recent)})


def print_char_map():
    # Debugging method for checking if the char map was created correctly.
    list = []
    for item in char_map:
        list.append(item)
    list.sort()
    print("Character Map:")
    for item in list:
        print(item, char_map.get(item))
    print("Total items in the character map:", len(char_map))


def to_ascii(filename):
    # The method that puts everything together to convert an image to ASCII.
    image = Image.open(filename).convert('L')
    create_char_map(33, 750)
    regions = split_image(image)
    columns = int(image.width / WIDTH_OF_REGION)
    if len(regions)%columns != 0:
        columns -= 1
    for i in range(0, len(regions)):
        if i % columns == 0 and i != 0:
            print()
        print(char_map.get(avg_gray_value(regions[i])), end='')
    print()


def print_usage():
    # Print how to execute the program and use the parameters.
    print('''
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
    ''')


if __name__ == "__main__":
    if len(argv) == 3:
        if int(argv[2]) >= 0:
            WIDTH_OF_REGION = int(argv[2])
            HEIGHT_OF_REGION = int(WIDTH_OF_REGION * 2)
            to_ascii(argv[1])
        else:
            print_usage()
    else:
        print_usage()
