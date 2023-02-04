# must open clipboard before using any function
# must close clipboard afterwards

import ctypes
from ctypes.wintypes import *
from os.path import join as path_join
from sys import getfilesystemencoding

GMEM_MOVABLE = 2
INT_P = ctypes.POINTER(ctypes.c_int)

CF_UNICODETEXT = 13
CF_HDROP = 15
CF_BITMAP = 2   # hbitmap
CF_DIB = 8   # DIB and BITMAP are interconvertable as from windows clipboard
CF_DIBV5 = 17

# bitmap compression types
BI_RGB = 0
BI_RLE8 = 1
BI_RLE4 = 2
BI_BITFIELDS = 3
BI_JPEG = 4
BI_PNG = 5
BI_ALPHABITFIELDS = 6

format_dict = {
    1: 'CF_TEXT',
    2: 'CF_BITMAP',
    3: 'CF_METAFILEPICT',
    4: 'CF_SYLK',
    5: 'CF_DIF',
    6: 'CF_TIFF',
    7: 'CF_OEMTEXT',
    8: 'CF_DIB',
    9: 'CF_PALETTE',
    10: 'CF_PENDATA',
    11: 'CF_RIFF',
    12: 'CF_WAVE',
    13: 'CF_UNICODETEXT',
    14: 'CF_ENHMETAFILE',
    15: 'CF_HDROP',
    16: 'CF_LOCALE',
    17: 'CF_DIBV5',
}

# todo:
# implement more formats (JPEG)
# write docs docs docs

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
shell32 = ctypes.windll.shell32

user32.OpenClipboard.argtypes = HWND,
user32.OpenClipboard.restype = BOOL
user32.GetClipboardData.argtypes = UINT,
user32.GetClipboardData.restype = HANDLE
user32.SetClipboardData.argtypes = UINT, HANDLE
user32.SetClipboardData.restype = HANDLE
user32.CloseClipboard.argtypes = None
user32.CloseClipboard.restype = BOOL
user32.IsClipboardFormatAvailable.argtypes = UINT,
user32.IsClipboardFormatAvailable.restype = BOOL
user32.CountClipboardFormats.argtypes = None
user32.CountClipboardFormats.restype = UINT
user32.EnumClipboardFormats.argtypes = UINT,
user32.EnumClipboardFormats.restype = UINT
user32.GetClipboardFormatNameA.argtypes = UINT, LPSTR, UINT
user32.GetClipboardFormatNameA.restype = UINT
user32.RegisterClipboardFormatA.argtypes = LPCSTR,
user32.RegisterClipboardFormatA.restype = UINT
user32.RegisterClipboardFormatW.argtypes = LPCWSTR,
user32.RegisterClipboardFormatW.restype = UINT
user32.RegisterClipboardFormatW.argtypes = LPCWSTR,
user32.RegisterClipboardFormatW.restype = UINT
user32.EmptyClipboard.argtypes = None
user32.EmptyClipboard.restype = BOOL

kernel32.GlobalAlloc.argtypes = UINT, ctypes.c_size_t
kernel32.GlobalAlloc.restype = HGLOBAL
kernel32.GlobalSize.argtypes = HGLOBAL,
kernel32.GlobalSize.restype = UINT
kernel32.GlobalLock.argtypes = HGLOBAL, 
kernel32.GlobalLock.restype = LPVOID
kernel32.GlobalUnlock.argtypes = HGLOBAL,
kernel32.GlobalUnlock.restype = BOOL

shell32.DragQueryFile.argtypes = HANDLE, UINT, ctypes.c_void_p, UINT
shell32.DragQueryFile.restype = UINT


class BITMAPFILEHEADER(ctypes.Structure):
    _pack_ = 1  # structure field byte alignment
    _fields_ = [
        ('bfType', WORD),  # file type ("BM")
        ('bfSize', DWORD),  # file size in bytes
        ('bfReserved1', WORD),  # must be zero
        ('bfReserved2', WORD),  # must be zero
        ('bfOffBits', DWORD),  # byte offset to the pixel array
    ]   
sizeof_BITMAPFILEHEADER = ctypes.sizeof(BITMAPFILEHEADER)

class BITMAPINFOHEADER(ctypes.Structure):
    _pack_ = 1  # structure field byte alignment
    _fields_ = [
        ('biSize', DWORD),
        ('biWidth', LONG),
        ('biHeight', LONG),
        ('biPLanes', WORD),
        ('biBitCount', WORD),
        ('biCompression', DWORD),
        ('biSizeImage', DWORD),
        ('biXPelsPerMeter', LONG),
        ('biYPelsPerMeter', LONG),
        ('biClrUsed', DWORD),
        ('biClrImportant', DWORD)
    ]
sizeof_BITMAPINFOHEADER = ctypes.sizeof(BITMAPINFOHEADER)

class BITMAPV4HEADER(ctypes.Structure):
    _pack_ = 1 # structure field byte alignment
    _fields_ = [
        ('bV4Size', DWORD),
        ('bV4Width', LONG),
        ('bV4Height', LONG),
        ('bV4PLanes', WORD),
        ('bV4BitCount', WORD),
        ('bV4Compression', DWORD),
        ('bV4SizeImage', DWORD),
        ('bV4XPelsPerMeter', LONG),
        ('bV4YPelsPerMeter', LONG),
        ('bV4ClrUsed', DWORD),
        ('bV4ClrImportant', DWORD),
        ('bV4RedMask', DWORD),
        ('bV4GreenMask', DWORD),
        ('bV4BlueMask', DWORD),
        ('bV4AlphaMask', DWORD),
        ('bV4CSTypes', DWORD),
        ('bV4RedEndpointX', LONG),
        ('bV4RedEndpointY', LONG),
        ('bV4RedEndpointZ', LONG),
        ('bV4GreenEndpointX', LONG),
        ('bV4GreenEndpointY', LONG),
        ('bV4GreenEndpointZ', LONG),
        ('bV4BlueEndpointX', LONG),
        ('bV4BlueEndpointY', LONG),
        ('bV4BlueEndpointZ', LONG),
        ('bV4GammaRed', DWORD),
        ('bV4GammaGreen', DWORD),
        ('bV4GammaBlue', DWORD)
    ]
sizeof_BITMAPV4HEADER = ctypes.sizeof(BITMAPV4HEADER)

class BITMAPV5HEADER(ctypes.Structure):
    _pack_ = 1 # structure field byte alignment
    _fields_ = [
        ('bV5Size', DWORD),
        ('bV5Width', LONG),
        ('bV5Height', LONG),
        ('bV5PLanes', WORD),
        ('bV5BitCount', WORD),
        ('bV5Compression', DWORD),
        ('bV5SizeImage', DWORD),
        ('bV5XPelsPerMeter', LONG),
        ('bV5YPelsPerMeter', LONG),
        ('bV5ClrUsed', DWORD),
        ('bV5ClrImportant', DWORD),
        ('bV5RedMask', DWORD),
        ('bV5GreenMask', DWORD),
        ('bV5BlueMask', DWORD),
        ('bV5AlphaMask', DWORD),
        ('bV5CSTypes', DWORD),
        ('bV5RedEndpointX', LONG),
        ('bV5RedEndpointY', LONG),
        ('bV5RedEndpointZ', LONG),
        ('bV5GreenEndpointX', LONG),
        ('bV5GreenEndpointY', LONG),
        ('bV5GreenEndpointZ', LONG),
        ('bV5BlueEndpointX', LONG),
        ('bV5BlueEndpointY', LONG),
        ('bV5BlueEndpointZ', LONG),
        ('bV5GammaRed', DWORD),
        ('bV5GammaGreen', DWORD),
        ('bV5GammaBlue', DWORD),
        ('bV5Intent', DWORD),
        ('bV5ProfileData', DWORD),
        ('bV5ProfileSize', DWORD),
        ('bV5Reserved', DWORD)
    ]
sizeof_BITMAPV5HEADER = ctypes.sizeof(BITMAPV5HEADER)

def open_clipboard():
    """
    Opens clipboard. Must be called before any action in performed.

    :return: (int) 0 if function fails, otherwise 1
    """
    return user32.OpenClipboard(0)

def close_clipboard():
    """
    Closes clipboard. Must be called after all actions are performed.

    :return: (int) 0 if function fails, otherwise 1
    """
    return user32.CloseClipboard()

def empty_cliboard():
    """
    Empties clipboard. Should be called before any setter actions.

    :return: (int) 0 if function fails, otherwise 1
    """
    return user32.EmptyClipboard()
    
def get_UNICODETEXT():
    """
    get text from clipboard as string 

    :return: (str) text grabbed from clipboard 
    """

    # user32.OpenClipboard(0)
    data = user32.GetClipboardData(CF_UNICODETEXT)
    dest = kernel32.GlobalLock(data)
    text = ctypes.wstring_at(dest)
    kernel32.GlobalUnlock(data)
    # user32.CloseClipboard()

    return text

def set_UNICODETEXT(text):
    """
    set text to clipboard as CF_UNICODETEXT 

    :param str text: text to set to clipboard
    :return: 1 if function succeeds, something else othewise (or maybe just spit out an error)
    """

    data = text.encode('utf-16le')
    size = len(data) + 2

    h_mem = kernel32.GlobalAlloc(GMEM_MOVABLE, size)
    dest = kernel32.GlobalLock(h_mem)
    ctypes.memmove(dest, data, size)
    kernel32.GlobalUnlock(h_mem)

    # user32.OpenClipboard(0)
    # user32.EmptyClipboard()
    user32.SetClipboardData(CF_UNICODETEXT, h_mem)
    # user32.CloseClipboard()
    return 1

def get_FILEPATHS():
    """
    get list of files from clipboard. 

    :return: (list) filepaths
    """
    filepaths = []

    #user32.OpenClipboard(0)
    data = user32.GetClipboardData(CF_HDROP)
    file_count = shell32.DragQueryFile(data, -1, None, 0)
    for index in range(file_count):
        buf = ctypes.c_buffer(260)
        shell32.DragQueryFile(data, index, buf, ctypes.sizeof(buf))
        filepaths.append(buf.value.decode(getfilesystemencoding()))
    #user32.CloseClipboard()

    return filepaths

def get_DIB(filepath = '', filename = 'bitmap'):
    """
    get image from clipboard as a bitmap and saves to filepath.

    :param str filepath: filepath to save image into 
    :param str filename: filename of the image
    :return: 1 if function succeeds, something else othewise (or maybe just spit out an error)
    """

    # user32.OpenClipboard(0)
    if not user32.IsClipboardFormatAvailable(CF_DIB):
        raise_runtimerror("clipboard image not available in 'CF_DIB format")

    h_mem = user32.GetClipboardData(CF_DIB)
    dest = kernel32.GlobalLock(h_mem)
    size = kernel32.GlobalSize(dest)
    data = bytes((ctypes.c_char*size).from_address(dest))

    bm_ih = BITMAPINFOHEADER()
    header_size = sizeof_BITMAPINFOHEADER
    ctypes.memmove(ctypes.pointer(bm_ih), data, header_size)

    compression = bm_ih.biCompression
    if compression not in (BI_BITFIELDS, BI_RGB): 
        raise_runtimerror(f'unsupported compression type {format(compression)}')

    bm_fh = BITMAPFILEHEADER()
    ctypes.memset(ctypes.pointer(bm_fh), 0, sizeof_BITMAPFILEHEADER)
    bm_fh.bfType = ord('B') | (ord('M') << 8)
    bm_fh.bfSize = sizeof_BITMAPFILEHEADER + len(str(data))
    sizeof_COLORTABLE = 0
    bm_fh.bfOffBits = sizeof_BITMAPFILEHEADER + header_size + sizeof_COLORTABLE

    img_path = path_join(filepath, filename + '.bmp')
    with open(img_path, 'wb') as bmp_file:
        bmp_file.write(bm_fh)
        bmp_file.write(data)

    kernel32.GlobalUnlock(h_mem)
    # user32.CloseClipboard()
    return 1

def get_DIBV5(filepath = '', filename = 'bitmapV5'):
    """
    get image from clipboard as a bitmapV5 and saves to filepath

    :param str filepath: filepath to save image into 
    :param str filename: filename of the image
    :return: 1 if function succeeds, something else othewise (or maybe just spit out an error)
    """

    # user32.OpenClipboard(0)
    if not user32.IsClipboardFormatAvailable(CF_DIBV5):
        raise_runtimerror("clipboard image not available in 'CF_DIBV5' format")

    h_mem = user32.GetClipboardData(CF_DIBV5)
    dest = kernel32.GlobalLock(h_mem)
    size = kernel32.GlobalSize(dest)
    data = bytes((ctypes.c_char*size).from_address(dest))

    bm_ih = BITMAPV5HEADER()
    header_size = sizeof_BITMAPV5HEADER
    ctypes.memmove(ctypes.pointer(bm_ih), data, header_size)

    if bm_ih.bV5Compression == BI_RGB:
        # convert BI_RGB to BI_BITFIELDS so as to properly support an alpha channel
        # everything other than the usage of bitmasks is same compared to BI_BITFIELDS so we manually add that part and put bV5Compression to BI_BITFIELDS
        # info on these header structures -> https://docs.microsoft.com/en-us/windows/win32/gdi/bitmap-header-types
        # and -> https://en.wikipedia.org/wiki/BMP_file_format

        bi_compression = bytes([3, 0, 0, 0])
        bi_bitmasks = bytes([0, 0, 255, 0,  0, 255, 0, 0,  255, 0, 0, 0,  0, 0, 0, 255])
        data = data[:16] + bi_compression + data[20:40] + bi_bitmasks + data[56:]

    elif bm_ih.bV5Compression == BI_BITFIELDS:
        # we still need to add bitmask (bV5AlphaMask) for softwares to recognize the alpha channel
        data = data[:52] + bytes([0, 0, 0, 255]) + data[56:]

    else:
        raise_runtimerror(f'unsupported compression type {format(bm_ih.bV5Compression)}')

    bm_fh = BITMAPFILEHEADER()
    ctypes.memset(ctypes.pointer(bm_fh), 0, sizeof_BITMAPFILEHEADER)
    bm_fh.bfType = ord('B') | (ord('M') << 8)
    bm_fh.bfSize = sizeof_BITMAPFILEHEADER + len(str(data))
    sizeof_COLORTABLE = 0
    bm_fh.bfOffBits = sizeof_BITMAPFILEHEADER + header_size + sizeof_COLORTABLE

    img_path = path_join(filepath, filename + '.bmp')
    with open(img_path, 'wb') as bmp_file:
        bmp_file.write(bm_fh)
        bmp_file.write(data)

    kernel32.GlobalUnlock(h_mem)
    # user32.CloseClipboard()
    return 1

def get_PNG(filepath = '', filename = 'PNG'):
    """
    get image in 'PNG' or 'image/png' format from clipboard and saves to filepath

    :param str filepath: filepath to save image into
    :param str filename: filename of the image
    :return: 1 if function succeeds, something else othewise (or maybe just spit out an error)
    """

    # user32.OpenClipboard(0)
    png_format = 0
    PNG = user32.RegisterClipboardFormatW(ctypes.c_wchar_p('PNG'))
    image_png = user32.RegisterClipboardFormatW(ctypes.c_wchar_p('image/png'))
    if user32.IsClipboardFormatAvailable(PNG):
        png_format = PNG
    elif user32.IsClipboardFormatAvailable(image_png):
        png_format = image_png
    else:
        raise_runtimerror("clipboard image not available in 'PNG' or 'image/png' format")

    h_mem = user32.GetClipboardData(png_format)
    dest = kernel32.GlobalLock(h_mem)
    size = kernel32.GlobalSize(dest)
    data = bytes((ctypes.c_char*size).from_address(dest))
    kernel32.GlobalUnlock(h_mem)
    # user32.CloseClipboard()

    img_path = path_join(filepath, filename + '.png')
    with open (img_path, 'wb') as png_file:
        png_file.write(data)

    return 1

def set_DIB(src_bmp):
    """
    set source bitmap image to clipboard as a CF_DIB or CF_DIBV5 according to the image

    :param str src_bmp: filepath of source image
    :return: 1 if function succeeds, something else othewise (or maybe just spit out an error)
    """

    with open(src_bmp, 'rb') as img:
        data = img.read()
    output = data[14:]
    size = len(output) 
    print(list(bytearray(output)[:200]))

    mem = kernel32.GlobalAlloc(GMEM_MOVABLE, size)
    h_mem = kernel32.GlobalLock(mem)
    ctypes.memmove(ctypes.cast(h_mem, INT_P), ctypes.cast(output, INT_P), size) 
    kernel32.GlobalUnlock(mem)

    
    if output[0] in [56, 108, 124]:
        # img contains DIBV5 or DIBV4 or DIBV3 Header
        fmt = CF_DIBV5
    else:
        fmt = CF_DIB

    # user32.OpenClipboard(0)
    # user32.EmptyClipboard()
    user32.SetClipboardData(fmt, h_mem)
    # user32.CloseClipboard()
    return 1  

def set_PNG(src_png):
    """
    set source png image to clipboard in 'PNG' format

    :param str src_png: filepath of source image
    :return: 1 if function succeeds, something else othewise (or maybe just spit out an error)
    """
    with open(src_png, 'rb') as img:
        data = img.read()
    size = len(data) 

    mem = kernel32.GlobalAlloc(GMEM_MOVABLE, size)
    h_mem = kernel32.GlobalLock(mem)
    ctypes.memmove(h_mem, data, size) 
    kernel32.GlobalUnlock(mem)

    # user32.OpenClipboard(0)
    # user32.EmptyClipboard()
    PNG = user32.RegisterClipboardFormatW(ctypes.c_wchar_p('PNG'))
    user32.SetClipboardData(PNG, h_mem)
    # user32.CloseClipboard()
    return 1

def is_format_available(format_id):
    """
    checks whether specified format is currently available on the clipboard

    :param int format_id: id of format to check for
    :return: (bool) True if specified format is available
    """
    
    # user32.OpenClipboard(0)
    is_format = user32.IsClipboardFormatAvailable(format_id)
    # user32.CloseClipboard()
    return bool(is_format)

def get_available_formats(buffer_size = 32):
    """
    gets a dict of all the currently available formats on the clipboard

    :param int buffer_size: (optional) buffer size to store name of each format in
    :return: a dict {format_id : format_name} of all available formats
    """
    available_formats = dict()
    # user32.OpenClipboard(0)
    fmt = 0
    for i in range(user32.CountClipboardFormats()):
        # must put previous fmt (starting from 0) in EnumClipboardFormats() to get the next one
        fmt = user32.EnumClipboardFormats(fmt)
        name_buf = ctypes.create_string_buffer(buffer_size)
        name_len = user32.GetClipboardFormatNameA(fmt, name_buf, buffer_size)
        fmt_name = name_buf.value.decode()
        
        # standard formats do not return any name, so we set one from out dictionary
        if fmt_name == '' and fmt in format_dict.keys():
            fmt_name = format_dict[fmt]
        available_formats.update({fmt : fmt_name})

    # user32.CloseClipboard()
    return available_formats

def get_image(filepath = '', filename = 'image'):
    """
    gets image from clipboard in a format according to a priority list (PNG > DIBV5 > DIB)

    """
    # user32.OpenClipboard(0)
    PNG = user32.RegisterClipboardFormatW(ctypes.c_wchar_p('PNG'))
    image_png = user32.RegisterClipboardFormatW(ctypes.c_wchar_p('image/png'))
    
    if user32.IsClipboardFormatAvailable(PNG) or user32.IsClipboardFormatAvailable(image_png):
        get_PNG(filepath, filename)
        return 1
    elif user32.IsClipboardFormatAvailable(CF_DIBV5):
        get_DIBV5(filepath, filename)
        return 1
    elif user32.IsClipboardFormatAvailable(CF_DIB):
        get_DIB(filepath, filename)
        return 1
    else:
        raise_runtimerror('image on clipboard not available in any supported format')

def set_image(src_img):
    """
    (NOT FULLY IMPLEMENTED) set source image to clipboard in multiple formats (PNG, DIB).

    :param str src_img: filepath of source image
    :return: 1 if function succeeds, something else othewise (or maybe just spit out an error)
    """
    # this is more complicated... gotta interconvert images
    # looking into ways to get this done with ctypes as well - NO IM DONE

    # temporary solution
    img_extn = src_img[(len(src_img)-3):].lower()
    if img_extn == 'bmp':
        # image format is bitmap
        set_DIB(src_img)
    elif img_extn == 'png':
        # image format is png
        set_PNG(src_img)
    else:
        raise_runtimerror('Unsupported image format')

    return 1

def raise_runtimerror(error_msg):
    close_clipboard()
    raise RuntimeError(error_msg)

if __name__ == '__main__':
    if open_clipboard():
        # empty_cliboard()
        print(get_available_formats())
        # set_UNICODETEXT('pasta pasta pasta pasta pasta pasta')
        close_clipboard()