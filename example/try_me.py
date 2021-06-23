"""
Author: Lorenzo Rinaldi

"""

from SESAM_utilities import functions 


bib_path = "sesam_publications.bib"
xlsx_path = "sesam_publications.xlsx"
properties = ['year','title','author','journal']
    
articles = functions.bibtex_parser(bib_path,xlsx_path,properties)
