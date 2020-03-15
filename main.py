import cv2 as cv
import numpy as np
import os

DEBUG = True


def debug_print(*args):
    if DEBUG:
        print(*args)


def uint16_to_indexed_hex(uint16_no, index):
    """
    Convert uint16 value to uint8 base on given index. Result will also between 0 to 3.
    :param uint16_no: uint16 value that will convert into uint8 base on given index
    :param index: index that gonna use while converting uint16 to uint8
    :return: uint8 value that will be between 0 to 3
    """
    # for example if we pass 5000(0x1388 - 00010011 10001000) as uint16 number
    # when index = 0
    #   mask = 0xC000
    # return = 0x0000 but we need as uint8 so return = 0x00

    # index can only shift right 14 time (7 = 14 / 2)
    # if index is greater then 7 then there is something wrong
    if index > 7:
        return None
    # return value is uint8
    return (0xC000 >> (index * 2) & uint16_no) >> (7 - index) * 2


def convert_uint16_to_list_of_uint8(uint16_no):
    """
    Convert given uint16 to list of uint8
    :param uint16_no: uint16 that will be converted into list of uint8s
    :return: list of uint8 with max 2 bit values
    """
    return [uint16_to_indexed_hex(uint16_no, index) for index in range(0, 8)]


def add_secret_file_size_into_base_image(image, width, height):
    """
    Embed steganography image file size into base image file
    :param image: np array of base image
    :param width: width of steganography image
    :param height: height of steganography image
    :return: embedded np array of base image
    """
    # Adding Width Inside Image
    image[0, 0:8, 0] = convert_uint16_to_list_of_uint8(np.uint16(width))
    # Adding Height Inside Image
    image[0, 0:8, 1] = convert_uint16_to_list_of_uint8(np.uint16(height))
    return image


def get_steganography_file_size(image):
    """
    Extract Width and Height value from image
    :param image: np array of image
    :return: list of int [height, width]
    """
    # list of int that store uint8 of width and height
    dimension = []
    # Getting width value from image
    dimension.extend(np.uint8((np.uint8(image[0, 0:8, 0]) & 0x03)))
    # Getting height value from image
    dimension.extend(np.uint8((np.uint8(image[0, 0:8, 1]) & 0x03)))
    # Converting into uint16
    dimension = np.uint16(dimension)
    # Setting width and height value to 0 with type of uint16
    width = np.uint16(0)
    height = np.uint16(0)
    # Converting uint8 pieces of width and height into uint16
    for i in range(0, 16):
        if i < 8:
            width = width | np.uint16(dimension[i] << (7 - (i % 8)) * 2)
        else:
            height = height | (dimension[i] << ((7 - (i % 8)) * 2))
    return [height, width]


def add_secret_image_inside_base_image(base_image, secret_image):
    """
    Embed the whole image into the base image
    :param base_image: np array of base image
    :param secret_image: np array of secret image
    :return: Embedded whole image changed on base image
    """
    # assigning base image rows
    base_image_rows = base_image.shape[1]
    # Iterating through 3 layers (blue, green and red, NOTE: not rgb, bgr)
    for layer in range(0, 3):
        # getting one layer from secret image
        current_layer = secret_image[:, :, layer].reshape((secret_image.shape[0] * secret_image.shape[1], 1))
        # assigning var to zeros of (total pixels, 1, 4)
        current_layer_with_4_pieces = np.zeros((secret_image.shape[0] * secret_image.shape[1], 1, 4))
        # this looping is for breaking uint8 into 4 uint8(value between 0 - 3)
        for i in range(0, 4):
            # breaking uint8 into pieces
            current_layer_with_4_pieces[:, :, i] = np.uint8((current_layer & (0xC0 >> (i * 2))) >> ((3 - i) * 2))
        # convert this (total pixels, 1, 4) array to 1-d array
        current_layer_with_4_pieces = current_layer_with_4_pieces.flatten()
        # checking gaps to fill to make rectangle array
        gaps = len(current_layer_with_4_pieces) % base_image_rows
        # Calculating columns
        columns = int(len(current_layer_with_4_pieces) / base_image_rows) + 1 if gaps > 0 else 0
        # Fill required gaps with zeros
        current_layer = np.append(current_layer_with_4_pieces, np.zeros((base_image_rows - gaps)))
        # convert current layer to base image rows with min. columns
        base_image[1:columns + 1, :, layer] = np.uint8(base_image[1:columns + 1, :, layer]) | np.uint8(
            current_layer.reshape((columns, base_image_rows)))
    return base_image


def get_secret_image_inside_base_image(base_img, width, height):
    """
    Extract secret image from base image
    :param height: height of secret image
    :param width: width of secret image
    :param base_img: np array of base image
    :return: np array of secret image that was embedded inside base image
    """
    # Setting secret image to zeros with given width and height
    secret_image = np.zeros((height, width, 3))
    # assigning base image rows
    base_image_rows = base_img.shape[1]
    # total amount of pixels after breaking them into 4 pieces of uint8
    total_pixels_after_broken = height * width * 4
    # calculating gaps that was filled with zeros
    gaps = total_pixels_after_broken % base_image_rows
    # calculating columns
    columns = int(total_pixels_after_broken / base_image_rows) + (1 if gaps > 0 else 0)
    # Iterating through 3 layers
    for layer in range(0, 3):
        # getting current layer with total pixels * 4, then take only last 2 bit, then flatten the array and then
        # reshape it into (total pixel, 4) np array
        current_layer = (base_img[1:columns + 1, :, layer] & 0x03).flatten()[0:total_pixels_after_broken].reshape(
            (width * height), 4)
        # shift bit respectively and assigning to respectively layer
        secret_image[:, :, layer] = (
                (current_layer[:, 0] << 6) | (current_layer[:, 1] << 4) | (current_layer[:, 2] << 2) | (
            current_layer[:, 3])).reshape((height, width))
    return secret_image


def embed_image_into_another_image():
    """
    Embed secret image into image which is bigger then secret image
    :return: None
    """
    steganography_img = None
    base_image = None

    while True:
        try:
            # Accepting Base Image Location
            base_image_location = input("Enter Absolute Location of BASE IMAGE: ")
            # Reading Image
            base_image = cv.imread(base_image_location)
            # Deleting all last 2 bits
            base_image = base_image & 0xFC
            # Printing Warning Message
            print("By using this Image you can hide MAX OF ", (base_image.shape[0] - 1) * base_image.shape[1] / 4,
                  " pixels image")
            break
        except:
            print("Please Enter Valid Image Location")

    while True:
        try:
            # Accepting Secret Image Location
            secret_image_location = input("Enter Absolute Location of SECRET IMAGE: ")
            # Reading Image
            secret_img = cv.imread(secret_image_location)
            # Checking image is exceeding max limit
            if secret_img.shape[0] * secret_img.shape[1] > (base_image.shape[0] - 1) * base_image.shape[1] / 4:
                # print warning and run loop again
                print(
                    f'Image is too big to hide inside previous image [MAX PIXELS:{(base_image.shape[0] - 1) * base_image.shape[1] / 4}]')
            else:
                break
        except:
            print("Please Enter Valid Image Location")

    # Adding secret image width and height into the base image
    base_image = add_secret_file_size_into_base_image(base_image, secret_img.shape[1], secret_img.shape[0])

    # Embedding whole secret image into the base image
    embedded_image = add_secret_image_inside_base_image(base_image, secret_img)
    # Getting Name of Result image
    embedded_image_name = input("Please Enter A Name For Steganography Image(Just Name Dont Add Location): ") + ".png"
    # File Location(path) where image will store
    embedded_image_location = input("Please Enter Absolute Location To Save Stegangography Image : ", )
    # Joining Path and name
    embedded_image_full_path = os.path.join(embedded_image_location, embedded_image_name)

    cv.imshow("Base Image", cv.resize(base_image, (int(base_image.shape[1] * 0.3), int(base_image.shape[0] * 0.3))))
    cv.imshow("Secret Image", cv.resize(secret_img, (int(secret_img.shape[1] * 0.3), int(secret_img.shape[0] * 0.3))))
    cv.imshow("Embedded Image", cv.resize(embedded_image, (int(embedded_image.shape[1] * 0.5), int(embedded_image.shape[0] * 0.5))))

    # Writing image to given location with given name
    cv.imwrite(embedded_image_full_path, embedded_image)


def extracting_secret_image_from_embedded_image():
    while True:
        try:
            embedded_image_location = input("Please Enter Absolute Path to Embedded Image: ")
            embedded_image = cv.imread(embedded_image_location)
            print(embedded_image)
            break
        except:
            print("Please Enter Valid Image Location")
    [height, width] = get_steganography_file_size(embedded_image)

    secret_image = get_secret_image_inside_base_image(embedded_image, width, height)

    # Getting Name of secret image
    secret_image_name = input(
        "Please Enter A Name For Secret Image(Just Name Dont Add Location): ") + ".jpg"
    # File Location(path) where image will store
    secret_image_location = input("Please Enter Absolute Location To Save Secret Image : ", )
    # Joining Path and name
    secret_image_full_path = os.path.join(secret_image_location, secret_image_name)

    cv.imshow("Secret Image", cv.resize(secret_image, (int(secret_image.shape[1] * 0.5), int(secret_image.shape[0] * 0.5))))
    cv.imshow("Embedded Image",
              cv.resize(embedded_image, (int(embedded_image.shape[1] * 0.3), int(embedded_image.shape[0] * 0.3))))

    # Writing image to given location with given name
    cv.imwrite(secret_image_full_path, secret_image)


if __name__ == '__main__':
    while True:
        selection = input("Enter 1 To Embed Image Into Anther Image\nEnter 2 To Extract Embedded Image From Another "
                          "Image\nEnter 0 To Quit\n: ")
        if int(selection) == 0:
            break
        elif int(selection) == 1:
            embed_image_into_another_image()
        else:
            extracting_secret_image_from_embedded_image()
        if cv.waitKey(100000):
            pass
        cv.destroyAllWindows()
