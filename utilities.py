"""
Author: Lorenzo Rinaldi

"""

import pandas as pd
import bibtexparser


#%%
class functions():
    
    def bibtex_parser(bib_path:str, xlsx_path:str, properties=['year', 'title', 'author', 'journal', 'doi']):
        
        
        """
        This function generates an .xlsx file from a list of documents contained in a .bib file
        
        Args:
            bib_path: string containing the path where to import the .bib file
            xlsx_path: string containing the path where to export the .xlsx file
            properties: list containing the properties to be parsed from the imported documents
        
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
                selection.iloc[i,title_position] = selection.iloc[i,title_position].split('{')[1].split('}')[0]
    
        if 'year' in selection.columns:
            year_position = list(selection.columns).index('year')
            for i in range(selection.shape[0]):
                selection.iloc[i,year_position] = int(selection.iloc[i,year_position])
        
        selection.to_excel(xlsx_path, index=False)
        
        return selection
