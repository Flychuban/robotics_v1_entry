from utils.image import StrideImage, PackedImage
from utils.eye_pattern import *
from utils.function_tracer import FunctionTracer
from curses.ascii import isspace
from utils.pixel import Pixel
from utils.resolution import Resolution

from utils.image import (
    ImageType,
    PackedImage,
    StrideImage,
)
from typing import (
    List,
    Tuple,
    Union
)

MIN_RED_VALUE = 200
MINUS_RED_150 = 150



# This class checks current position whether is The border of the image (final positions)
class IsBorder:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column
    def __eq__(self, other: object) -> bool:
        return self.row == other.row and self.column == other.column


def transformPixelImage(image: Union[PackedImage, StrideImage]) -> [[Pixel]]:
    pixels = None
    if isinstance(image, PackedImage):
        pixels = image.pixels
    if isinstance(image, StrideImage):
        pixels = image.merge_pixel_components()

    result = []

    for i in range(0, (len(pixels)), image.resolution.width):
        result.append(pixels[i: i + image.resolution.width])

    return result


def transformToPackedImage(cast: [[Pixel]]) -> PackedImage:
    pixels = []
    for row in cast:
        pixels += row
    return PackedImage(Resolution(width=len(cast[0]), height=len(cast)), pixels)
def transformToStrideImage(cast: [[Pixel]]) -> StrideImage:
    pixels = []
    for row in cast:
        pixels += row
    return StrideImage(Resolution(width=len(cast[0]), height=len(cast)), pixels)


def compute_solution(images: List[Union[PackedImage, StrideImage]]):
    ft = FunctionTracer("compute_solution", "seconds")

    for i in range(0,len(images)):
        print(f'processing image {i}')
        updatedCast = rectifyImage(images[i])
        if isinstance(images[i], PackedImage):
            images[i] = transformToPackedImage(updatedCast)
        if isinstance(images[i], StrideImage):
            images[i] = transformToStrideImage(updatedCast)

    del ft


def rectifyImage(image: Union[PackedImage, StrideImage]) -> PackedImage:
    resolution = image.resolution
    # transform the list of pixels to 2d array of pixels
    cast = transformPixelImage(image)
    for row in range(0, resolution.height):
        for column in range(0, resolution.width):
            topLeftCorner = IsBorder(row, column)
            findMatchingPattern(cast, topLeftCorner)
    return cast


def findMatchingPattern(cast: [[Pixel]], topLeftCorner: IsBorder):
    # we have to check third pattern firstly because it is based on first and second pattern. 
    patterns = [EYE_PATTERN_3, EYE_PATTERN_4, EYE_PATTERN_1, EYE_PATTERN_2]
    for pattern in patterns:
        if checkElementPattern(cast, topLeftCorner, pattern):
            changeRedEyes(cast, pattern, topLeftCorner)


def checkElementPattern(cast: [[Pixel]], topLeftCorner: IsBorder, pattern: EyePattern) -> bool:
    for rowOutOfElement in range(0, len(pattern)):
        for columnOutOfElement in range(0, len(pattern[0])):
            patternSymbol = pattern[rowOutOfElement][columnOutOfElement]
            castRedComponnet = cast[topLeftCorner.row + rowOutOfElement][topLeftCorner.column + columnOutOfElement].red
            if(not(isspace(patternSymbol)) and castRedComponnet < MIN_RED_VALUE):
                return  False
    return True

def changeRedEyes(cast: [[Pixel]], pattern: EyePattern, topLeftCorner: IsBorder):
    for rowOutOfElement in range(0, len(pattern)):
        for columnOutOfElement in range(0, len(pattern[0])):
            if(not(isspace(pattern[rowOutOfElement][columnOutOfElement]))):
                cast[topLeftCorner.row + rowOutOfElement][topLeftCorner.column + columnOutOfElement].red = cast[topLeftCorner.row + rowOutOfElement][topLeftCorner.column + columnOutOfElement].red - MINUS_RED_150

            