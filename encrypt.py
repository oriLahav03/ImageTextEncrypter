import numpy as np
import PIL.Image
from tkinter import filedialog

import tkinter as tk


def get_action_choice():
    """
    The function show the menu of options and take from user what he want to do.
    :return: The choice.
    :rtype: str
    """
    options_msg = {
        '1': 'Encrypt text.',
        '2': 'Encrypt file.'
    }
    print('\n'.join([f'{key}: {value}' for key, value in options_msg.items()]))
    choice = input('Your Choice: ')
    if choice in options_msg:
        return choice
    else:
        exit(f"Invalid Option: '{choice}'")


def choose_file_dialog():
    """
    The function create file dialog and take the file path.
    :return: The path.
    :rtype: str
    """
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename()
    root.destroy()

    if path == '':
        exit('No file chosen!')
    else:
        return path


def get_hide_data(choice):
    """
    The function take from the user the message he want to encrypt.
    :param choice: the choice the user made.
    :type choice: str
    :return: the message, file extension / None
    :rtype: str or bytes, str or None
    """
    if int(choice) == 1:
        return input('Enter Your Message To Hide: '), None
    elif int(choice) == 2:
        print('Choose the file to hide in the image...')
        path = choose_file_dialog()
        with open(path, 'rb') as f:
            return f.read(), path.split('.')[-1]


def encrypt_file(path, file_name, secret, file_extension):
    """
    The function encrypt the message (file) inside of an image.
    :param path: the image path.
    :type path: str
    :param file_name: the image name.
    :type file_name: str
    :param secret: the message (file).
    :type secret: bytes
    :param file_extension: the message (file) extension.
    :type file_extension: str
    :return: None
    :rtype: None
    """
    with open(path, 'rb') as read_file, open(file_name + '_encoded.png', 'ab+') as f:
        original_file_data = read_file.read()
        extension_length = bytes(str(len(file_extension)), 'utf-8')
        extension = bytes(str(file_extension), 'utf-8')
        f.write(original_file_data + extension_length + extension + secret)
    print('Done!')


def encrypt_message(path, message_to_hide, file_name):
    """
    The function encrypt the message (text) inside of an image.
    :param path: the image path.
    :type path: str
    :param message_to_hide: the message (text).
    :type message_to_hide: str
    :param file_name: the image name.
    :type file_name: str
    :return: None
    :rtype: None
    """
    image = PIL.Image.open(path, 'r')
    width, height = image.size
    image_array = np.array(list(image.getdata()))

    if image.mode == 'P':
        exit('Not Supported!')

    channels = 4 if image.mode == 'RGBA' else 3
    pixels = image_array.size // channels

    stop_indicator = input('What would you want your stop indicator to be?: ')

    message_to_hide += stop_indicator

    byte_message = ''.join(f"{ord(c):08b}" for c in message_to_hide)
    bits = len(byte_message)

    if bits > pixels:
        exit('Not enough space')

    index = 0
    for i in range(pixels):
        for j in range(3):
            if index < bits:
                image_array[i][j] = int(bin(image_array[i][j])[2:-1] + byte_message[index], 2)
                index += 1

    image_array = image_array.reshape((height, width, channels))
    result = PIL.Image.fromarray(image_array.astype('uint8'), image.mode)
    result.save(f'{file_name}_encoded.png')
    print('Done!')


def main():
    choice = get_action_choice()
    message_to_hide, file_extension = get_hide_data(choice)

    print('Choose the image to hide the secret in...')
    path = choose_file_dialog()
    file_name = path.split('/')[-1].split('.')[0]

    match choice:
        case '1':
            encrypt_message(path, message_to_hide, file_name)
        case '2':
            encrypt_file(path, file_name, message_to_hide, file_extension)
    input()


if __name__ == "__main__":
    main()
