import logging
import sqlite3
from ete4 import NCBITaxa
import json
import pandas as pd
import re
from Bio import Entrez
from aws_handler import AwsHandler
from utils import is_null, set_prompt_text
from constants import DEFAULT_EMAIL, OLD_REPORTS_PATH, DATA_PATH, ACRONYMS_PATH

Entrez.email = DEFAULT_EMAIL


class MetagenomicsAssistant:
    def __init__(self, llm_handler):
        self.ncbi = NCBITaxa()
        self.llm_handler = llm_handler
        self.df_text = pd.read_pickle(OLD_REPORTS_PATH)
        self.df_data = pd.read_csv(DATA_PATH)
        self.df_acronym = pd.read_csv(ACRONYMS_PATH)

        self.df_data["TaxID"] = self.df_data["TaxID"].astype(str)
        self.df_acronym["TaxID"] = self.df_acronym["TaxID"].astype(str)

    def set_text_to_prompt(self) -> list[str]:
        """
        Return 2 random texts from 'treated_clean_final.csv'
        """
        text_to_prompt = self.df_text["content"].sample(n=2).to_list()
        return text_to_prompt

    def get_organism_rank(self, tax_id: str | int, rank: str) -> str | None:
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
            logging.error(f"Error getting rank {rank} for TaxID {tax_id}: {e}")
            return None

    def get_organism_name(self, tax_id: str | int) -> str:
        """
        Get only organism name from dict
        """
        try:
            tax_id_int = int(tax_id) if isinstance(tax_id, str) else tax_id
            taxid_dict = self.ncbi.get_taxid_translator([tax_id_int])
            return taxid_dict.get(tax_id_int, "")
        except Exception as e:
            print(f"Error when catching organism name for {tax_id}: {e}")
            logging.error(f"Error when catching organism name for {tax_id}: {e}")
            return ""

    def get_organism_tax_id(self, organism_name: str) -> str:
        """
        Get TaxID from organism name
        """
        try:
            name_dict = self.ncbi.get_name_translator([organism_name])
            if organism_name in name_dict:
                taxids = name_dict[organism_name]
                return taxids[0] if taxids else ""
            return ""
        except Exception as e:
            print(f"Error when catching TaxID for {organism_name}: {e}")
            logging.error(f"Error when catching TaxID for {organism_name}: {e}")
            return ""

    def _get_data_with_fallback(
        self, tax_id: str | int, dataframe: pd.DataFrame, column_name: str
    ) -> str | None:
        """
        Helper to get data with fallback strategies:
        1. Direct lookup
        2. Merged IDs (reverse lookup in ete3 sqlite)
        3. Descendants lookup
        """
        try:
            # 1. Direct Lookup
            tax_id_str = str(tax_id)
            result = dataframe.loc[dataframe["TaxID"] == tax_id_str, column_name]
            if not result.empty:
                value = result.values[0]
                return value if not is_null(value) else None

            # If not found, prepare candidates
            candidates = set()

            # 2. Merged Check (Reverse lookup: finding old IDs merged INTO this tax_id)
            # We need to query the internal sqlite db of ete3
            try:
                db_path = self.ncbi.dbfile
                if db_path:
                    # We create a new connection to be safe with threading/handling
                    with sqlite3.connect(db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            "SELECT taxid_old FROM merged WHERE taxid_new = ?",
                            (int(tax_id),),
                        )
                        merged_rows = cursor.fetchall()
                        for row in merged_rows:
                            candidates.add(str(row[0]))
            except Exception as e:
                logging.warning(f"Failed to query merged table for {tax_id}: {e}")

            # 3. Descendants Check
            # Check if any descendant is in the CSV
            try:
                # 3a. Direct Children via SQL (Reliable for 'no rank' nodes)
                if db_path:
                    with sqlite3.connect(db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            "SELECT taxid FROM species WHERE parent = ?", (int(tax_id),)
                        )
                        children = cursor.fetchall()
                        for child in children:
                            candidates.add(str(child[0]))

                # 3b. Deep Descendants via ete3
                descendants = self.ncbi.get_descendant_taxa(tax_id)
                # Limit to reasonable number to avoid query explosion if high up in tree
                # But for a species/genus it should be fine.
                for desc_id in descendants:
                    candidates.add(str(desc_id))
            except Exception as e:
                logging.warning(f"Failed to get descendants for {tax_id}: {e}")

            if not candidates:
                return None

            # 4. Check candidates in Dataframe
            # We filter the dataframe for TaxIDs in candidates
            matches = dataframe[dataframe["TaxID"].isin(list(candidates))]
            if not matches.empty:
                # We return the first match.
                # Ideally we might want the "closest", but any match is better than none.
                value = matches.iloc[0][column_name]
                return value if not is_null(value) else None

            return None

        except Exception as e:
            logging.error(f"Error in _get_data_with_fallback for {tax_id}: {e}")
            return None

    def get_organism_disease(self, tax_id: str | int) -> str | None:
        """
        Get organism disease from 'data_for_biojarvis.csv' by TaxID
        """
        return self._get_data_with_fallback(tax_id, self.df_data, "Diseases")

    def get_organism_transmission(self, tax_id: str | int) -> str | None:
        """
        Get organism transmission from 'data_for_biojarvis.csv' by TaxID
        """
        return self._get_data_with_fallback(tax_id, self.df_data, "Transmissions")

    def get_organism_hosts(self, tax_id: str | int) -> str | None:
        """
        Get organism hosts from 'data_for_biojarvis.csv' by TaxID
        """
        return self._get_data_with_fallback(tax_id, self.df_data, "Hosts")

    def get_organism_acronym(self, tax_id: str | int) -> str | None:
        """
        Get organism Acronym (if exists) from 'acronym.csv' by TaxID
        """
        return self._get_data_with_fallback(tax_id, self.df_acronym, "Acronym")

    def get_genome_size(self, tax_id: str | int) -> int | str:
        """
        Access 'nucleotide' database and get organism size.
        """
        try:
            scientific_name = self.get_organism_name(tax_id)
            if not scientific_name:
                return ""

            handle_data = Entrez.esearch(
                db="nucleotide",
                term=f"{scientific_name} [Organism] RefSeq [filter] AND complete genome AND (bp OR nucleotides)",
                retmax=20,
            )
            record_articles = Entrez.read(handle_data)
            handle_data.close()

            for sequence_id in record_articles.get("IdList", []):
                handle_data = Entrez.efetch(
                    db="nucleotide", id=sequence_id, rettype="gb", retmode="text"
                )
                gb_text = handle_data.read()
                handle_data.close()
                match_search = re.search(r"LOCUS\s+\S+\s+(\d+)\s+bp", gb_text)
                if match_search:
                    return int(match_search.group(1))
            return ""
        except Exception as e:
            print(f"Erro ao obter tamanho do genoma para TaxID {tax_id}: {e}")
            logging.error(f"Error getting genome size for TaxID {tax_id}: {e}")
            return ""

    def set_organism_fields(self, tax_id: str | int) -> dict:
        """
        Set organism fields for primary source for prompt
        """
        organism_informations = {
            "Name": self.get_organism_name(tax_id),
            "Acronym": self.get_organism_acronym(tax_id),
            "Size": f"{self.get_genome_size(tax_id)}",
            "Diseases": self.get_organism_disease(tax_id),
            "Transmissions": self.get_organism_transmission(tax_id),
            "Hosts": self.get_organism_hosts(tax_id),
            "Family": self.get_organism_rank(tax_id, "family"),
            "Genus": self.get_organism_rank(tax_id, "genus"),
        }
        organism_informations = {
            dict_organism_info_key: dict_organism_info_value
            for dict_organism_info_key, dict_organism_info_value in organism_informations.items()
            if not is_null(dict_organism_info_value)
        }
        return organism_informations

    def generate_report(
        self,
        tax_id: str | int,
        language: str = "english",
        organism_info: dict | None = None,
    ) -> str:
        """
        Generate report using the configured LLM handler
        """
        if organism_info:
            information_dict = organism_info
        else:
            information_dict = self.set_organism_fields(tax_id)

        if not information_dict or not information_dict.get("Name"):
            return f"Error: Failed to retrieve basic organism information for TaxID {tax_id}. The TaxID might be invalid or not present in the local database. Try updating the database using the --update-db flag."

        text_reference = self.set_text_to_prompt()
        prompt_text = set_prompt_text(information_dict, text_reference, language)
        return self.llm_handler.generate_text(prompt_text)
