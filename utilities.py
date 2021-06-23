"""
Author: Lorenzo Rinaldi, SESAM

"""

import pandas as pd
import bibtexparser
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import os
# from os.path import isfile, join


#%%
class functions():
    
    """
    This class contains general functions useful in multiple occasions.
    
    Notes for the contributors:
        1) if you add a new function, please make sure you use the same syntax as the functions already implemented
           and make sure to add a documentation
        2) thank you for the support!!!

    """
    
    
    def bibtex_parser(bib_path:str, xlsx_path:str, properties=['year', 'title', 'author', 'journal', 'doi'], doi_links=True):
        
        """
        This function generates an .xlsx file from a list of documents contained in a .bib file
        
        Args:
            bib_path: string containing the path where to import the .bib file
            xlsx_path: string containing the path where to export the .xlsx file
            properties: list containing the properties to be parsed from the imported documents
            doi_links: bool; if True the doi columns will contain clickable hyperlinks
        
        Returns:
            selection: pandas DataFrame containing the parsed information of about the imported documents contained in the .bib file
        """
        
        with open(bib_path, encoding="utf8") as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
            
        df = pd.DataFrame(bib_database.entries)
        selection = df[properties]
        
        if 'title' in selection.columns:
            title_position = list(selection.columns).index('title')
            for i in range(selection.shape[0]):
                try:
                    selection.iloc[i,title_position] = selection.iloc[i,title_position].split('{')[1].split('}')[0]
                except:
                    pass
    
        if 'year' in selection.columns:
            year_position = list(selection.columns).index('year')
            for i in range(selection.shape[0]):
                try:
                    selection.iloc[i,year_position] = int(selection.iloc[i,year_position])
                except:
                    pass

        if 'doi' in selection.columns and doi_links==True:
            doi_position = list(selection.columns).index('doi')
            for i in range(selection.shape[0]):
                try:
                    selection.iloc[i,doi_position] = 'https://doi.org/'+selection.iloc[i,doi_position]
                except:
                    pass
        
        selection.to_excel(xlsx_path, index=False)
        
        return selection
        
    
    def get_files_path_from_directory(path, file_extension:str):
        
        filenames = os.listdir(path)
        
       
        for file in filenames:
            if file[-len(file_extension)] != file_extension:
                filenames.remove(file)
               
        return filenames


    def elsevier_pdf_metadata_miner(pdf_path:list):

        """
        This function generates a dictionary containing metadata information of one or multiple pdf articles downloaded from Elsevier
        
        Args:
            pdf_path: list containing the paths of the files to import
        
        Returns:
            info: dictionary containing metadata information of the imported pdf articles
        """
        
        fp = open(pdf_path, 'rb')
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        info = {}
        for i in doc.info[0].keys():
            try:
                info[i] = doc.info[0][i].decode("utf-8")
            except:
                pass
            
        return info

        
                
        
        
