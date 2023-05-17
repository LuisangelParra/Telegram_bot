from pylatex import Document, Section, Alignat
import aspose.pdf as ap
import os
from pdf2image import convert_from_path

POPPLER_PATH = r"%s\poppler-23.05.0\Library\bin" % (os.getcwd())
PDF_PATH = r"%s\temps\results.pdf" % (os.getcwd())
SAVE_PATH = r"%s\generated_images" % (os.getcwd())

def latex_image(latex_code1, latex_code2, filename="results"):
    geometry_options = {"paperwidth": "150mm", "paperheight": "80mm",  "rmargin": "20mm", "lmargin": "20mm"}
    doc = Document(default_filepath=f"temps\{filename}",geometry_options=geometry_options)
    
    with doc.create(Section('Funcion No Recurrente:', numbering=False)):
        with doc.create(Alignat(numbering=False, escape=False))  as agn:
            agn.append(r"%s \\ " % (latex_code1))
            agn.append(r"%s" % (latex_code2))
    
    doc.generate_tex()
    options = ap.TeXLoadOptions()
    document = ap.Document(f"temps\{filename}.tex" , options)
    document.save(f"temps\{filename}.pdf")

    pages = convert_from_path(pdf_path=PDF_PATH, poppler_path=POPPLER_PATH)

    c = 0
    for page in pages:
        image_name = f'solve_rr_results.png'
        page.save(os.path.join(SAVE_PATH, image_name), 'PNG')
        c += 1




