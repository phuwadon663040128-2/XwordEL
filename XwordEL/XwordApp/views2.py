from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings

from collections import Counter
from lxml import etree

from XwordEL.test_api import test_api

from .crossword_algo_mod import CrossWord, CrossWordFormatter
from .forms import CrosswordSessionForm, userUploadFile

# from .pdf_processer import get_words_from_pdf

def end_game(request):
    return render(request, 'endgame.html')

def OCR_API(request):
    API = settings.OCR_API_URL
    is_api_available = test_api(API)

    print(f"API is available: {is_api_available}")
    
    if is_api_available:
        # API is available, generate corresponding HTML.
        root = etree.Element("div", attrib={"class": "file-ocr-toggle"})
        cb_content = etree.SubElement(root, "div", attrib={"class": "cb-content"})
        label = etree.SubElement(cb_content, "label", attrib={"class": "cb", "for": "file-ocr"})
        etree.SubElement(label, "input", attrib={"type": "checkbox", "id": "file-ocr", "name": "file-ocr", "value": "true"})
        etree.SubElement(label, "div", attrib={"class": "cb-transition"})
        etree.SubElement(cb_content, "span", attrib={"class": "cb-text"}).text = "OCR"
    else:
        # API is not available, generate different HTML.
        root = etree.Element("div", attrib={"class": "file-ocr-toggle"})
        tooltip = etree.SubElement(root,"div", attrib={"class": "tooltip"})
        etree.SubElement(tooltip, "span", attrib={"class": "tooltiptext"}).text = "OCR API NOT AVAILABLE"
        fade_div = etree.SubElement(tooltip, "div", attrib={"class": "file-ocr-toggle fade", "style": "pointer-events: none"})
        cb_content = etree.SubElement(fade_div, "div", attrib={"class": "cb-content"})
        label = etree.SubElement(cb_content, "label", attrib={"class": "cb", "for": "file-ocr"})
        etree.SubElement(label, "input", attrib={"type": "checkbox", "id": "file-ocr", "name": "file-ocr", "value": "true", "disabled": "disabled"})
        etree.SubElement(label, "div", attrib={"class": "cb-transition"})
        etree.SubElement(cb_content, "span", attrib={"class": "cb-text"}).text = "OCR"

    # Convert the lxml etree element to a string and return as HttpResponse.
    return HttpResponse(etree.tostring(root, pretty_print=True, method="html").decode("utf-8"))

@login_required(login_url='/auth/login/')
def Spacy_API(request):
    API = settings.SPACY_API_URL
    return HttpResponse(test_api(API))
    


