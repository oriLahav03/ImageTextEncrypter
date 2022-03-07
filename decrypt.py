from tkinter import filedialog

import tkinter as tk

import numpy as np
import PIL.Image


def get_action_choice():
    """
    The function show the menu of options and take from user what he want to do.
    :return: The choice.
    :rtype: str
    """
    options_msg = {
        '1': 'Decrypt text.',
        '2': 'Decrypt file.'
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


def decrypt_file():
    # TODO: fix the index seek
    """
    The function decrypt the file from in the image.
    :return: None
    :rtype: None
    """
    jpg_end = b"\xff\xd9"
    png_end = b"\x00\x00\x00\x00IEND\xaeB`\x82"

    path = choose_file_dialog()
    file_name = path.split('/')[-1].split('.')[0]

    with open(path, 'rb') as f:
        content = f.read()

        # print(content)
        if jpg_end in content:
            end_hex = jpg_end
        elif png_end in content:
            end_hex = png_end
        else:
            # print(content)
            return
        offset = content.index(end_hex)
        with open('a.txt', 'w') as r:
            r.write(str(content[content.index(end_hex):]))
        # print(f.tell())
        f.seek(offset + len(end_hex))
        # print(f.tell())
            # x9aB\xb4\x966\xdf\xbf\xb4\x9a\xd5v\xdei\xf2
        length = f.read(1).decode()
        if length == '':
            exit('There is no file in this image')
        extension = f.read(int(length)).decode()
        with open(f'{file_name}_decrypted.{extension}', 'wb') as s:
            s.write(f.read())


def decrypt_message():
    """
    The function decrypt the message from in a image.
    :return: None
    :rtype: None
    """
    image = PIL.Image.open(choose_file_dialog(), 'r')
    image_array = np.array(list(image.getdata()))

    channels = 4 if image.mode == 'RGBA' else 3

    pixels = image_array.size // channels

    secret_bits = [bin(image_array[i][j])[-1] for i in range(pixels) for j in range(3)]
    secret_bits = ''.join(secret_bits)
    secret_bits = [secret_bits[i:i+8] for i in range(0, len(secret_bits), 8)]

    secret_message = [chr(int(secret_bits[i], 2)) for i in range(len(secret_bits))]
    secret_message = ''.join(secret_message)

    stop_indicator = input('Enter the stop indicator: ')

    if stop_indicator in secret_message:
        print(secret_message[:secret_message.index(stop_indicator)])
    else:
        print('Could not find the secret message!')


def main():
    choice = get_action_choice()

    match choice:
        case '1':
            decrypt_message()
        case '2':
            decrypt_file()
    input()


if __name__ == "__main__":
    main()
