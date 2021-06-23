"""
Author: Lorenzo Rinaldi

"""

import pandas as pd
import bibtexparser


#%%
class functions():
    
    def bibtex_parser(self,bib_path,xlsx_path, properties=['year', 'title', 'author', 'journal', 'doi']):
        
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
