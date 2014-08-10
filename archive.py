#!/usr/bin/env python3

'''Script to create/maintain incremental backups'''

from argparse import ArgumentParser,RawDescriptionHelpFormatter

def archive_preset( preset, source, destination ):
    pass

def process_preset_files( preset_files ):
    pass

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

