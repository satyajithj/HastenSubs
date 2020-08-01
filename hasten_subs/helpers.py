import os
import re
import glob
import typing

_valid_sub_extensions = ['srt']
_valid_hasten_expr = '^[+-]?[0-5]{1}[0-9]{1}:[0-5]{1}[0-9]{1}$'

def get_files(src: str):
    """ Check if 'src' is a valid dir or a subtitle file,
    and return relevant data """

    subtitle_file_list = [] 

    if os.path.isdir(src):
        # 'src' is a directory
        print('> The provided path is a directory')

        for ext in _valid_sub_extensions:
            found = glob.glob(os.path.join(src, '*.' + ext))
            if len(found) > 0:
                subtitle_file_list += found

    elif os.path.isfile(src):
        # 'src' is a files
        print('> The provided path is a file')

        for ext in _valid_sub_extensions:
            if src.endswith(ext):
                # Accept the file only if it contains a valid extension
                subtitle_file_list.append(src)

    else:
        # 'src' is neither a directory nor a file
        print('> The provided path is neither a valid directory nor a file')

    return subtitle_file_list

def decode_hasten_arg(hasten: str) -> typing.Tuple:
    """ Decode the hasten argument that is requested

    The accepted format is [+/-]MM:SS. For example

        +01:13  Delay by 1 minute and 13 seconds
        -02:07  Hasten by 2 minutes and 7 seconds
    """

    hasten = hasten.replace(' ', '') # Remove all spaces in the argument

    validity_test = 'VALID' if bool(re.match(_valid_hasten_expr, hasten)) else 'INVALID'
    print('> The specified hasten argument "{}" is {}'.format(hasten, validity_test))

    if validity_test == 'INVALID':
        print('> A valid argument is of the form: [+/-]MM:SS (Ex: +01:13, -02:07)')
        return ()

    sign = -1 if hasten[0] == '-' else 1    # Hasten/Delay?
    action = 'hastened' if hasten[0] == '-' else 'delayed'

    # Extract the values for minutes and seconds
    hasten = hasten[1:]
    ms = hasten.split(':')
    minutes, seconds = int(ms[0]), int(ms[1])
    decoded_tuple = (sign * minutes, sign * seconds)

    print('> Decoded argument: (M: {}, S: {})'.format(*decoded_tuple))
    print('> All the detected subtitle files will be {} by {} mins and {} secs'.format(action, minutes, seconds))

    return decoded_tuple


