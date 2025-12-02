import fitz
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QImage,QPixmap
import base64

def render(doc,pgno,zoom):
    if not doc or pgno>=len(doc):
        return None
    page = doc.load_page(pgno)
    zmatrix = fitz.Matrix(zoom,zoom)
    pix = page.get_pixmap(matrix=zmatrix)
    if pix.alpha:
        qformat = QImage.Format.Format_RGBA8888
    else:
        qformat = QImage.Format.Format_RGB888
    img = QImage(pix.samples,pix.width,pix.height,pix.stride,qformat).copy()
    pixmp = QPixmap.fromImage(img)
    return pixmp

def exportImg(doc,pgno):
    if not doc or pgno>=len(doc):
        return None
    page = doc.load_page(pgno)
    zmatrix = fitz.Matrix(1.0,1.0)
    pix = page.get_pixmap(matrix=zmatrix)
    png = pix.tobytes('png')

    return base64.b64encode(png).decode("utf-8")