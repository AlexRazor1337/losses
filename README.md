# losses.py [![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://stand-with-ukraine.pp.ua)

**losses.py** is a Python script that allows to watch an actual data of the russian army losses in the [Russo-Ukrainian War](https://en.wikipedia.org/wiki/Russo-Ukrainian_War).

You can watch the data in the console or generate an image with this. For this you'll need file with a background and file with a font in **.ttf** format.

For the image making part, you'll have a file `config.json` created when you use script for creating image for the first time. Detailed description of the file and usage can be found down bellow.

The data comes from the [Ministry of Finance website](https://index.minfin.com.ua/ua/russian-invading/casualties/). Script parses, strips and prepares it to be printed as table or writed on image.

This script was made as a final project of [CS50’s Introduction to Programming with Python](https://cs50.harvard.edu/python/2022/project/).

# Demo

Here you can see how the script prints data to the console:
![demo](https://user-images.githubusercontent.com/26604491/173046200-58bc1ac2-edd1-4ec0-a54a-121f52cf5226.gif)

If you run the script with image generation mode you'll get something like this:
![result](https://user-images.githubusercontent.com/26604491/173244554-f9945b62-90d2-4d15-a08c-694748faf083.jpg)


# How to run

Console stats output:  
1. Install Python 3.
2. Run `pip install -r requirements.txt` to install dependencies.
3. Run `python project.py`  


Generating image:  
1. Install Python 3.
2. Run `pip install -r requirements.txt` to install dependencies.
3. Run `python project.py -i`. This will generate config file.
4. Edit `config.json`, specifying resource files and font sizes.
5. Run `python project.py -i` again. This will produce `result.jpg` file.

Config file example:
```json
{
    "background_path": "./resources/image.jpg",
    "font_path": "./resources/font.ttf",
    "font_size": 25,
    "header_font_size": 32,
    "header_text": "Протягом 24.02-%s\n орієнтовані втрати противника склали:"
}
```
**NOTE:** `header_text` must contain `%s` for the current date.

Also, you can run tests for the script. For this:
1. Install pytest: `pip install pytest`
2. Run `pytest test_project.py`

#
[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua)
