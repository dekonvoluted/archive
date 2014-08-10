#!/usr/bin/env python3

'''Script to create/maintain incremental backups'''

from argparse import ArgumentParser,RawDescriptionHelpFormatter
from os import path
from configparser import ConfigParser

def archive_preset( preset, source, destination ):
    pass

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
    args = parser.parse_args()

    process_preset_files( args.PRESETS )

