import os
import typing
import datetime
import traceback

from tqdm import tqdm

class NegativeTimeTagException(SystemExit):
    pass

def _update_time_tags(op: typing.Tuple, line: str) -> str:

    time_tags = line.rstrip().split()
    tags = time_tags[::2]
    connector = time_tags[1]

    for i, tag in enumerate(tags):
        hms, ms = tag.split(',')
        h, m, s = hms.split(':')
        h, m, s = int(h), int(m), int(s)

        m, s = m + op[0], s + op[1]

        # Correct the seconds for overflow
        if s < 0 or s > 59:
            m += s // 60
            s %= 60
        # Correct the minutes for overflow
        if m < 0 or m > 59:
            h += m // 60
            m %= 60
        
        if h < 0 or m < 0 or s < 0:
            raise NegativeTimeTagException

        tags[i] = '{:02d}:{:02d}:{:02d},{}'.format(h, m, s, ms)

    return tags[0] + ' ' + connector + ' ' + tags[1]


def transform_subs(op: typing.Tuple, file_list: typing.List):
    """ Create subtitle files with updated time stamps """

    print()
    for file_path in tqdm(file_list):
        # Get the file name and extension
        head, tail = os.path.split(file_path)
        tail_split = tail.split('.')

        # Generate a new file name
        dst_file_name = '_' + tail_split[0] + '.' + tail_split[1]
        dst_file_path = os.path.join(head, dst_file_name)

        # Open the destination file
        # Create it if it does not exist
        dst_file = open(dst_file_path, 'w+')

        # Run the transformation and updates
        with open(file_path, 'r') as src:

            line_number = 0
            while True:
                line = src.readline()   # Read a line from the source file
                line_number += 1

                if '-->' in line:
                    # Line contains time tags
                    try:
                        new_line = _update_time_tags(op, line)
                        dst_file.write(new_line + '\n')
                    except NegativeTimeTagException:
                        print()
                        print('> ERROR')
                        print('> Could not complete processing the file: {}'.format(file_path))
                        print('> Generated a NEGATIVE time tag. The delay is too long')
                        break
                    except ValueError:
                        print()
                        print('> ERROR')
                        print('> File: {}'.format(file_path))
                        print('> Line number: {}'.format(line_number))
                        print(traceback.format_exc())
                else:
                    dst_file.write(line)

                if not line:
                    break

        dst_file.close()

    print()
    print('> Processing complete')
