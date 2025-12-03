from ete4 import NCBITaxa
import json
import pandas as pd
import re
from Bio import Entrez
from aws_handler import AwsHandler 
from utils import is_null, set_prompt_text
from constants import DEFAULT_EMAIL
Entrez.email = DEFAULT_EMAIL

class MetagenomicsAssistant:
    def __init__(self, aws_handler: AwsHandler):
        self.ncbi = NCBITaxa()
        self.aws_handler = aws_handler
        self.df_text = pd.read_csv('./files/old_reports.csv')
        self.df_data = pd.read_csv('./files/data_for_biojarvis.csv')
        self.df_acronym = pd.read_csv('./files/acronyms.csv')
        
        self.df_data['TaxID'] = self.df_data['TaxID'].astype(str)
        self.df_acronym['TaxID'] = self.df_acronym['TaxID'].astype(str)

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
        try:
            organism_lineage = self.ncbi.get_lineage(tax_id)
            organism_ranks = self.ncbi.get_rank(organism_lineage)
            organism_names = self.ncbi.get_taxid_translator(organism_lineage)

            for taxon_id in organism_lineage:
                if organism_ranks.get(taxon_id) == rank:
                    return organism_names.get(taxon_id) 
            return None
        except Exception as e:
            print(f"Erro ao obter rank {rank} para TaxID {tax_id}: {e}")
            return None
    
    def get_organism_name(self, tax_id):
        """
        Get only organism name from dict
        """
        try:
            tax_id_int = int(tax_id) if isinstance(tax_id, str) else tax_id
            taxid_dict = self.ncbi.get_taxid_translator([tax_id_int])
            return taxid_dict.get(tax_id_int, '')
        except Exception as e:
            print(f'Error when catching organism name for {tax_id}: {e}')
            return ''
        
    def get_organism_tax_id(self, organism_name):
        """
        Get TaxID from organism name
        """
        try:
            name_dict = self.ncbi.get_name_translator([organism_name])
            if organism_name in name_dict:
                taxids = name_dict[organism_name]
                return taxids[0] if taxids else ''
            return ''
        except Exception as e:
            print(f'Error when catching TaxID for {organism_name}: {e}')
            return ''
    
    def get_organism_disease(self, tax_id):
        """
        Get organism disease from 'data_for_biojarvis.csv' by TaxID
        """
        try:
            tax_id_str = str(tax_id)
            result = self.df_data.loc[self.df_data['TaxID'] == tax_id_str, 'Diseases']
            if not result.empty:
                value = result.values[0]
                return value if not is_null(value) else None
            return None
        except Exception as e:
            print(f"Erro ao obter doença para TaxID {tax_id}: {e}")
            return None
    
    def get_organism_transmission(self, tax_id):
        """
        Get organism transmission from 'data_for_biojarvis.csv' by TaxID
        """
        try:
            tax_id_str = str(tax_id)
            result = self.df_data.loc[self.df_data['TaxID'] == tax_id_str, 'Transmissions']
            if not result.empty:
                value = result.values[0]
                return value if not is_null(value) else None
            return None
        except Exception as e:
            print(f"Erro ao obter transmissão para TaxID {tax_id}: {e}")
            return None
    
    def get_organism_hosts(self, tax_id):
        """
        Get organism hosts from 'data_for_biojarvis.csv' by TaxID
        """
        try:
            tax_id_str = str(tax_id)
            result = self.df_data.loc[self.df_data['TaxID'] == tax_id_str, 'Hosts']
            if not result.empty:
                value = result.values[0]
                return value if not is_null(value) else None
            return None
        except Exception as e:
            print(f"Erro ao obter hosts para TaxID {tax_id}: {e}")
            return None
    
    def get_organism_acronym(self, tax_id):
        """
        Get organism Acronym (if exists) from 'acronym.csv' by TaxID
        """
        try:
            tax_id_str = str(tax_id)
            result = self.df_acronym.loc[self.df_acronym['TaxID'] == tax_id_str, 'Acronym']
            if not result.empty:
                value = result.values[0]
                return value if not is_null(value) else None
            return None
        except Exception as e:
            print(f"Erro ao obter acrônimo para TaxID {tax_id}: {e}")
            return None
    
    def get_genome_size(self, tax_id):
        """
        Access 'nucleotide' database and get organism size.
        """
        try:
            scientific_name = self.get_organism_name(tax_id)
            if not scientific_name:
                return ''
                
            handle_data = Entrez.esearch(
                db = 'nucleotide',
                term = f'{scientific_name} [Organism] AND complete genome AND (bp OR nucleotides)',
                retmax = 20
            )
            record_articles = Entrez.read(handle_data)
            handle_data.close()

            for sequence_id in record_articles.get('IdList', []):
                handle_data = Entrez.efetch(
                    db = 'nucleotide', 
                    id = sequence_id, 
                    rettype = 'gb',
                    retmode = 'text'
                )
                gb_text = handle_data.read()
                handle_data.close()
                match_search = re.search(r'LOCUS\s+\S+\s+(\d+)\s+bp', gb_text)
                if match_search:
                    return int(match_search.group(1))
            return ''
        except Exception as e:
            print(f"Erro ao obter tamanho do genoma para TaxID {tax_id}: {e}")
            return ''
    
    def set_organism_fields(self, tax_id):
        """
        Set organism fields for primary source for prompt
        """
        organism_informations = {
            'Name': self.get_organism_name(tax_id),
            'Acronym': self.get_organism_acronym(tax_id),
            'Size': f'{self.get_genome_size(tax_id)}',
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
    
    def build_bedrock_request(self, information_dict, language):
        text_reference = self.set_text_to_prompt()
        if type(information_dict) == int:
            information_dict = self.set_organism_fields(information_dict)

        prompt_text = set_prompt_text(information_dict, text_reference, language)
        return AwsHandler.get_bedrock_prompt_response(prompt_text)

    def invoke_bedrock_model(self, tax_id, language):
        information_to_request = self.set_organism_fields(tax_id)
        request_body = self.build_bedrock_request(information_to_request, language)
        return self.aws_handler.return_bedrock_response(request_body)
             