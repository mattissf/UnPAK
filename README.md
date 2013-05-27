UnPAK
============
Will extract .pak files from i.e. Quake I.

I needed the teleport sound as my message beep tone, so this small utility was born.

Clone git repository and execute bin/unpak

> bin/unpak -h
> usage: unpak [-h] [-d DESTINATION] [-v] pak_file
> 
> Extracts PAK archives
> 
> positional arguments:
> pak_file              Path to the PAK file
> 
> optional arguments:
>   -h, --help            show this help message and exit
>   -d DESTINATION, --destination DESTINATION
>                         Destination directory to extract files. Defaults to
>                         current working directory.
>   -v, --verbose         Print verbose information
