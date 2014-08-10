#!/usr/bin/env python3

'''Script to create/maintain incremental backups'''

__version__ = '1.0'

from argparse import ArgumentParser,RawDescriptionHelpFormatter
from os import path,mkdir,symlink,unlink
from configparser import ConfigParser
from datetime import date
from subprocess import call

def archive_preset( preset, source, destination ):
    today = date.today().strftime( '%Y-%m-%d' )
    destination_path = destination + '/' + preset + '/'

    # Avoid error messages during the first run
    if not path.isdir( destination_path ):
        mkdir( destination_path )
        mkdir( destination_path + '/' + today )
        symlink( destination_path + '/' + today, destination_path + '/latest' )

    # Compose the rsync call
    sync_command = '/usr/bin/rsync'
    sync_command += ' --verbose --archive --exclude=lost+found'
    sync_command += ' --link-dest=' + destination_path + '/latest '
    sync_command += source + '/ '
    sync_command += destination_path + '/' + today

    call( sync_command, shell=True )

    # Update link to latest backup
    unlink( destination_path + '/latest' )
    symlink( destination_path + '/' + today, destination_path + '/latest' )

def process_preset_files( preset_files ):
    for preset_file in preset_files:
        if not path.isfile( preset_file ):
            print( preset_file, 'is not a valid input.' )
        else:
            config = ConfigParser()
            config.read( preset_file )

            for section in config.sections():
                preset = section
                source = path.realpath( config[ section ][ 'source' ] )
                destination = path.realpath( config[ section ][ 'destination' ] )

                if not path.isdir( source ):
                    print( source, 'is not a valid source.' )
                    exit( 1 )

                if not path.isdir( destination ):
                    print( destination, 'is not a valid destination.' )
                    exit( 1 )

                archive_preset( preset, source, destination )

if __name__ == '__main__':
    parser = ArgumentParser( formatter_class=RawDescriptionHelpFormatter, description = '''
    Create and maintain incremental backups.
    Backups are described by presets like this,

        [home]
        source = /home/user/
        destination = /mnt/backup/

    A single preset file can contain many such presets.
    Multiple preset files can be supplied as arguments.''' )
    parser.add_argument( 'PRESETS', nargs='+', help='One or more INI files containing presets.' )
    parser.add_argument( '--version', action='version', version = __version__ )
    args = parser.parse_args()

    process_preset_files( args.PRESETS )

