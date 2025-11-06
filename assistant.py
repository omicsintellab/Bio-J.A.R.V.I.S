# Libraries
from ete4 import NCBITaxa # Provides access to taxonomy data
import json # Handling json variables
import pandas as pd # Data analysis and csv manipulation
import re # Operations with regular expressions
from Bio import Entrez # Provides code to access NCBI over the WWW.
from aws_handler import AwsHandler 
from utils import is_null, set_prompt_text

class MetagenomicsAssistant:
    def __init__(self, aws_handler: AwsHandler):
        self.ncbi = NCBITaxa()
        self.aws_handler = aws_handler
        self.df_text = pd.read_csv('./files/old_reports.csv')
        self.df_data = pd.read_csv('./files/data_for_biojarvis.csv')
        self.df_acronym = pd.read_csv('./files/acronyms.csv')

    def set_text_to_prompt(self):
        """
        Return 2 random texts from 'treated_clean_final.csv'
        """
        text_to_prompt = self.df_text['content'].sample(n=2).to_list()
        return text_to_prompt
    
    def get_organism_rank(self, tax_id, rank: str):
        """
        Get family or genus of organism by TaxID
        """
        organism_lineage = self.ncbi.get_lineage(tax_id)
        organism_ranks = self.ncbi.get_rank(organism_lineage)
        organism_names = self.ncbi.get_taxid_translator(organism_lineage)

        for taxon_id in organism_lineage:
            if organism_ranks.get(taxon_id) == rank:
                return organism_names.get(taxon_id) 
        return None
    
    def get_organism_name(self, tax_id):
        """
        Get only organism name from taxid_dict
        """
        taxid_dict = self.ncbi.get_lineage_translator([tax_id])
        return taxid_dict.get(tax_id, '')
    
    def get_organism_disease(self, tax_id):
        """
        Get organism disease from 'data_for_biojarvis.csv' by TaxID
        """
        try:
            return self.df_data.loc[self.df_data['TaxID'] == tax_id, 'Diseases'].values[0]
        except IndexError:
            return None
    
    def get_organism_transmission(self, tax_id):
        """
        Get organism transmission from 'data_for_biojarvis.csv' by TaxID
        """
        try:
            return self.df_data.loc[self.df_data['TaxID'] == tax_id, 'Transmissions'].values[0]
        except IndexError:
            return None
    
    def get_organism_hosts(self, tax_id):
        """
        Get organism hosts from 'data_for_biojarvis.csv' by TaxID
        """
        try:
            return self.df_data.loc[self.df_data['TaxID'] == tax_id, 'Hosts'].values[0]
        except IndexError:
            return None
    
    def get_organism_acronym(self, tax_id):
        """
        Get organism Acronym (if exists) from 'acronym.csv' by TaxID
        """
        try:
            return self.df_acronym.loc[self.df_acronym['TaxID'] == tax_id, 'Acronym'].values[0]
        except IndexError:
            return None
    
    def get_genome_size(self, tax_id):
        """
        Access 'nucleotide' database and get organism size.
        """
        scientific_name = self.get_organism_name(tax_id)
        handle_data = Entrez.esearch(
            db = 'nucleotide',
            term = f'{scientific_name} [Organism] AND complete genome',
            retmax = 10
        )
        record_articles = Entrez.read(handle_data)
        handle_data.close()

        for sequence_id in record_articles.get('IdList', []):
            handle_data = Entrez.efetch(
                db = 'bucleotide', 
                id = sequence_id, 
                rettype = 'gb',
                retmode = 'text'
            )
            gb_text = handle_data.read()
            handle_data.close()
            match_search = re.search(r'LOCUS\s+\S+\s+(\d+)\s+bp', gb_text)
            if match_search:
                return int(match_search.group(1))
        return None
    
    def set_organism_fields(self, tax_id):
        """
        Set organism fields for primary source for prompt
        """
        organism_informations = {
            'Name': self.get_organism_name(tax_id),
            'Acronym': self.get_organism_acronym(tax_id),
            'Size': f'{self.get_genome_size(tax_id)}pb',
            'Diseases': self.get_organism_disease(tax_id),
            'Transmissions': self.get_organism_transmission(tax_id),
            'Hosts': self.get_organism_hosts(tax_id),
            'Family': self.get_organism_rank(tax_id, 'family'),
            'Genus': self.get_organism_rank(tax_id, 'genus')
        }
        organism_informations = {
            dict_organism_info_key: dict_organism_info_value for dict_organism_info_key, dict_organism_info_value in organism_informations.items()
            if not is_null(dict_organism_info_value)
        }
        return organism_informations
    
    def build_bedrock_request(self, information_dict):
        text_reference = self.set_text_to_prompt()
        if type(information_dict) == int:
            information_dict = self.set_organism_fields(information_dict)

        prompt_text = set_prompt_text(information_dict, text_reference)
        return AwsHandler.get_bedrock_prompt_response(prompt_text)

    def invoke_bedrock_model(self, tax_id):
        information_to_request = self.set_organism_fields(tax_id)
        request_body = self.build_bedrock_request(information_to_request)
        return self.aws_handler.return_bedrock_response(request_body)
    