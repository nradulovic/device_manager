
Installation
============

Some requirements may be installed automatically via PIP:

"Requirements files" are files containing a list of items to be installed using
pip install like so:

    pip install -r requirements.txt

Additional requirements:
 - PyGObject: PIP installation is still not widespread for this library and it
   must be installed using OS package manager. Another alternative is to get
   the source and build/install it manually. 
   
   Debian/Ubuntu/Mint:
   
    sudo apt install python-gi python-gi-cairo python3-gi python3-gi-cairo gir1.2-gtk-3.0

   Fedora:

    sudo dnf install pygobject3 python3-gobject gtk3

   openSUSE

    sudo zypper install python-gobject python3-gobject gtk3

   The project was tested with PyGObject version 3.20.1