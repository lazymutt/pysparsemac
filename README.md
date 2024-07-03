
# PySparseMac

Handles creation, mounting, and compression of MacOS sparse disk images
## Installation

Install PySparseMac from here or with pip (***soon***)

```bash
  pip install pysparsemac
```

## Documentation

I have another project that automates a service backup. I decided I wanted to write all of the files to a disk image and compress it in an automated fashion. This is the result, a wrapper around `hdiutil`.

#### create_disk(path, name, size)
>*creates an uncompressed disk image at specificed location.*

>**path**: full path (directory and filename) of uncompressed disk image to be created
>**name**: volume name of the mounted disk image
>**size**: size of uncompressed disk image

#### mount_disk(path)
>*mount the disk image previously created.*

>**path**: full path (directory and filename) of uncompressed disk image

#### unmount_disk(vol_id)
>*unmounts a mounted disk image.*

>**vol_id**: Volume ID of the disk to unmount

#### compress_disk(path)
>*creates a compressed ULMO format disk in the same directory as the uncompressed disk.*

>**path**: full path (directory and filename) of uncompressed disk image to be compressed

#### move_final_disk(path, destination_dir)
>*move compressed disk to different location.*

>**path**: full path (directory and filename) of compressed disk image to be moved
>**destination_dir**: destination to move disk to

#### demo_it()
>*runs through the full suite of functions to demonstrate the module.* 

## Usage/Examples

```python
import pysparsemac

pysparsemac.demo_it()
```


## Roadmap

Version | Date | Notes
------- | ---- | -----
0.0.1 | 2024.05.18 | Initial release, thanks PyCon24! Demo.
0.0.2 | 2024.05.19 | Added types
0.0.3 | 2024.06.18 | Cleaned up, prepare for Github/PyPI
0.0.4 | 2024.06.20 | Removed types
0.0.5 | 2024.06.28 | Error checking, exceptions
0.1.0 | 2024.06.29 | Public release
0.1.1 | 2024.07.03 | reworked suprocess calls, destination path, compressed path synthesis

- Docs

- Add more integrations(?)


## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

[@lazymutt](https://www.github.com/lazymutt) Todd McDaniel
