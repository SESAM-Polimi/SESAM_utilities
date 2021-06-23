"""
Author: Lorenzo Rinaldi

"""

from SESAM_utilities import functions 


bib_path = "references.bib"
xlsx_path = "references.xlsx"
properties = ['year','title','author','journal']
    
articles = functions.bibtex_parser(bib_path,xlsx_path,properties)
