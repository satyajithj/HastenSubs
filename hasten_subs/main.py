import click

import core
import helpers

@click.command()
@click.option('--src', default='.', help='The absolute path to a subtitle file or a directory containing subtitle files')
@click.option('--hasten', default='+00:04', help='Time to hasten or delay by (Ex: +01:13, -02:07)')

def run(src, hasten):

    # Check whether valid files are available
    #########################################

    file_list = helpers.get_files(src)
    num_files = len(file_list)

    if num_files == 0:
        print('> Could not find any valid files')
        return
    else:
        print('> {} valid files are available'.format(num_files))

    # Valid files are available, what now?
    # Validate and decode the 'hasten' argument
    ###################################################################
    operation = helpers.decode_hasten_arg(hasten)

    # Transform the subtitle files
    core.transform_subs(op=operation, file_list=file_list)
    print('> Goodbye')

if __name__=='__main__':
    run()