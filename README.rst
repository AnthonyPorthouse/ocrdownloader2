
====================
OCRDownloader
====================

OCRDownloader is a command-line tool for batch downloading OC ReMix songs, making it easy to fetch tracks before new batch torrents are released.

Features
--------
- Download multiple OC ReMix tracks by specifying a range of track numbers
- Uses aria2 for fast and reliable downloads
- Simple CLI interface

Installation
------------
1. Ensure you have Python >= 3.12 installed.
2. Install aria2 (e.g., `sudo apt install aria2` on Debian/Ubuntu).
3. Install OCRDownloader:
   ::
	   git clone https://github.com/AnthonyPorthouse/ocrdownloader2.git
	   cd ocrdownloader2
	   pip install .

Usage
-----
Run the following command to download tracks:
::
	ocrdownloader 1000 1100

This downloads every track from 1000 to 1100 into the current working directory.

Command-line Options
--------------------
For more options, run:
::
	ocrdownloader --help

Dependencies
------------
- Python >= 3.7
- aria2

Contributing
------------
Pull requests and issues are welcome! Please see the repository for details.

License
-------
See `LICENCE.rst` for license information.
