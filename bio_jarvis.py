# Libraries
from ete4 import NCBITaxa # Provides access to taxonomy data
import json # Handling json variables
import pandas as pd # Data analysis and csv manipulation
import re # Operations with regular expressions
from Bio import Entrez # Provides code to access NCBI over the WWW.
from aws_handler import AwsHandler 
from utils import is_null

class MetagenomicsAssistant:
    def __init__(self, aws_handler: AwsHandler):
        self.ncbi = NCBITaxa()
        self.aws_handler=aws_handler
        self.df_text = pd.read_csv('./files/treated_clean_final.csv')
        self.df_data = pd.read_csv('./files/data_for_biojarvis_metagen.csv')
        self.df_acronym = pd.read_csv('./files/acronyms_filled_and_treated.csv')

    def set_text_to_prompt(self):
        """
        Return 2 random texts from 'treated_clean_final.csv'
        """
        text_to_prompt = self.df_text['content'].sample(n=2).to_list()
        return text_to_prompt
    
    def get_organism_rank(self, tax_id: int, rank: str):
        lineage = 