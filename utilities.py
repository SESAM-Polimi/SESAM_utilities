"""
Author: Lorenzo Rinaldi, SESAM

"""

import pandas as pd
import bibtexparser
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import os, fnmatch
import shutil
import copy


_PAPERNAME_METHOD = {'LR': {'items': ['Year','Journal','Author','Title'],
                            'minimum_requirements': ['Year','Author'],
                            'separator':'_'}}
_SPECIAL_CHARACTERS = [(' ','_'), ('<',''), ('>',''), (':','-'), ('"',''), ('/','-'),('\\','-'),('?',''),('*','')]

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
        
    
    
    def get_files_names(path:str, file_extensions:list):

        """
        This function generates a list containing names of files contained in a given path
        
        Args:
            path: directory to search
            file_extension: list of the extensions to be selected
        
        Returns:
            filenames: dictionary whose keys are related to the extensions and the values are the strings containing the names of the files with the desired extension
        """
        
        listOfFiles = os.listdir(path)
        filenames = {}
        
        for item in file_extensions:
            extension = "*.{}".format(item)
            filenames[item] = []
            for entry in listOfFiles:
                if fnmatch.fnmatch(entry, extension):
                    filenames[item] += [os.path.join(path,entry)]
                   
        return filenames


    def get_pdf_metadata(file_paths):

        """
        This function generates a dictionary containing pdf metadata
        
        Args:
            file_paths: list or dictionary containing paths of pdf files to be analysed
            file_extension: list of the extensions to be selected
        
        Returns:
            filenames: dictionary whose keys are related to the extensions and the values are the strings containing the names of the files with the desired extension
        """

        if isinstance(file_paths, dict):
            pdf_files = file_paths['pdf']
        elif isinstance(file_paths, list):
            pdf_files = copy.deepcopy(file_paths)
            
        pdf_metadata = {}
        for file in pdf_files:   
            try:
                fp = open(file, 'rb')
                parser = PDFParser(fp)
                doc = PDFDocument(parser)
                pdf_metadata[file] = {}
                
                for i in doc.info[0].keys():
                    try:
                        pdf_metadata[file][i] = doc.info[0][i].decode("utf-8")
                    except:
                        pass
                fp.close()
            except:
                print('WARNING: problems with file named "{}"'.format(file))
        
        return pdf_metadata



    def rename_articles(metadata:dict, method:str, check=False):
        
        """
        This function renames pdf scientific articles according to pdf metadata
        
        SUPPORT FOR ELSEVIER ARTICLES ONLY AT THE MOMENT
        
        Args:
            metadata: dictionary whose keys are the paths of the pdf files, the values are the metadata
            method: string representing the renaming criterion, to be defined in the _PAPERNAME_METHOD dictionary in the upper part of this script        
            check: boolean to check the proceeding of the function step by step and show up when there are mistakes
        """        
                
        for file in list(metadata.keys()):
            
            if check==True:
                print(file)
                print('\n')
            
            "Replacing special characters from title, if available"
            try:
                title = copy.deepcopy(metadata[file]['Title']) 
                counter = 0
                for i in title:
                    if i in [spchar[0] for spchar in _SPECIAL_CHARACTERS]:
                        
                        metadata[file]['Title'] = metadata[file]['Title'][:counter]\
                                                      + [spchar[1] for spchar in _SPECIAL_CHARACTERS][[spchar[0] for spchar in _SPECIAL_CHARACTERS].index(i)]\
                                                      + metadata[file]['Title'][counter+1:]
                    counter += 1    
            except:
                pass
            
            
            "Extracting year from CreationDate parameter, if available"
            try:
                metadata[file]['Year'] = metadata[file]['CreationDate'].split(':')[1][:4]
            except:
                pass
    

            "Renaming Elsevier articles"
            if 'Creator' in list(metadata[file].keys()):
                if metadata[file]['Creator'] == 'Elsevier':
                    
                    try:
                        metadata[file]['DOI']     = metadata[file]['Subject'].split(' ')[-1]
                    except:
                        pass
                    
                    try:
                        metadata[file]['Journal'] = metadata[file]['DOI'].split('.')[2]
                    except:
                        pass
                    
                    try:
                        metadata[file]['Author']  = metadata[file]['Author'].split(' ')[-1]
                    except:
                        pass
                    
                    
                    new_name = []
                    for item in _PAPERNAME_METHOD[method]['items']:
                        try:
                            new_name += [metadata[file][item]]
                        except:
                            pass
                        
                    new_name = _PAPERNAME_METHOD[method]['separator'].join(new_name)+'.pdf'
        
                    count_properties = []
                    for item in _PAPERNAME_METHOD[method]['items']:
                        if item in new_name:
                            count_properties += [item]
                    
                    if set(_PAPERNAME_METHOD[method]['minimum_requirements']) <= set(count_properties):
                        len_max = 255
                        if len(new_name) >= len_max:
                            new_name = new_name[:(len_max-len('.pdf'))]
                            new_name += '.pdf'
                        
                        new_name = os.path.join('\\'.join(file.split('\\')[:-1]),new_name)
                        
                        os.rename(file, new_name)
                
                    
                
                

    
        
                
        
        
