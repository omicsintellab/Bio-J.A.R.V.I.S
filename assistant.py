# assistant.py

from ete4 import NCBITaxa
from Bio import Entrez
import pandas as pd
from typing import Dict, Any, Optional

from aws_handler import AwsHandler
from utils import is_null, set_prompt_text
from constants import DEFAULT_EMAIL

Entrez.email = DEFAULT_EMAIL


class MetagenomicsAssistant:
    """
    High-level orchestration layer that:
    - Resolves organism metadata
    - Builds prompts
    - Dispatches requests to AWS Bedrock models
    """

    def __init__(self, aws_handler: AwsHandler) -> None:
        self.ncbi = NCBITaxa()
        self.aws_handler = aws_handler

        # Load reference datasets
        self.df_text = pd.read_csv("./files/old_reports.csv")
        self.df_data = pd.read_csv("./files/data_for_biojarvis.csv")
        self.df_acronym = pd.read_csv("./files/acronyms.csv")

        self.df_data["TaxID"] = self.df_data["TaxID"].astype(str)
        self.df_acronym["TaxID"] = self.df_acronym["TaxID"].astype(str)

    # ------------------------------------------------------------------
    # Prompt helpers
    # ------------------------------------------------------------------

    def _random_reference_texts(self) -> list[str]:
        """
        Select random reference texts to guide style.
        """
        return self.df_text["content"].sample(n=2).tolist()

    def _build_prompt(self, tax_id: int, language: str) -> str:
        """
        Build the final LLM prompt.
        """
        organism_info = self.set_organism_fields(tax_id)
        references = self._random_reference_texts()
        return set_prompt_text(organism_info, references, language)

    def _build_payload(self, prompt: str, model: str) -> bytes:
        """
        Build a Bedrock-compatible payload according to model family.
        """

        if model == "amazon":
            # Amazon Nova Micro: STRICT schema (no `type`, no topP)
            return self.aws_handler.build_nova_payload(
                prompt=prompt,
                max_tokens=500,
                temperature=0.1,
            )

        # Claude / OpenAI-style / Gemma
        return self.aws_handler.build_openai_style_payload(
            prompt=prompt,
            max_tokens=500,
            temperature=0.1,
            top_p=0.1,
        )

    # ------------------------------------------------------------------
    # Public generation API
    # ------------------------------------------------------------------

    def generate_with_nova(self, tax_id: int, language: str = "english") -> str:
        prompt = self._build_prompt(tax_id, language)
        payload = self._build_payload(prompt, model="amazon")
        return self.aws_handler.invoke_nova_micro(payload)

    def generate_with_openai(self, tax_id: int, language: str = "english") -> str:
        prompt = self._build_prompt(tax_id, language)
        payload = self._build_payload(prompt, model="openai")
        return self.aws_handler.invoke_openai(payload)

    def generate_with_claude(self, tax_id: int, language: str = "english") -> str:
        prompt = self._build_prompt(tax_id, language)
        payload = self._build_payload(prompt, model="claude")
        return self.aws_handler.invoke_claude(payload)

    def generate_with_gemma(self, tax_id: int, language: str = "english") -> str:
        prompt = self._build_prompt(tax_id, language)
        payload = self._build_payload(prompt, model="gemma")
        return self.aws_handler.invoke_gemma(payload)

    # ------------------------------------------------------------------
    # Organism metadata
    # ------------------------------------------------------------------

    def set_organism_fields(self, tax_id: int) -> Dict[str, Any]:
        """
        Aggregate organism metadata into a clean dict.
        """
        data = {
            "Name": self.get_organism_name(tax_id),
            "Acronym": self.get_organism_acronym(tax_id),
            "Size": self.get_genome_size(tax_id),
            "Diseases": self.get_organism_disease(tax_id),
            "Transmissions": self.get_organism_transmission(tax_id),
            "Hosts": self.get_organism_hosts(tax_id),
            "Family": self.get_organism_rank(tax_id, "family"),
            "Genus": self.get_organism_rank(tax_id, "genus"),
        }

        # Remove null / empty fields
        return {k: v for k, v in data.items() if not is_null(v)}

    # ------------------------------------------------------------------
    # NCBI + local data accessors
    # ------------------------------------------------------------------

    def get_organism_tax_id(self, organism_name: str) -> Optional[str]:
        """
        Resolve TaxID from organism name.
        """
        name2taxid = self.ncbi.get_name_translator([organism_name])
        if organism_name in name2taxid:
            return str(name2taxid[organism_name][0])
        return None

    def get_organism_name(self, tax_id: int) -> Optional[str]:
        """
        Get organism scientific name.
        """
        lineage = self.ncbi.get_lineage(tax_id)
        names = self.ncbi.get_taxid_translator(lineage)
        return names.get(tax_id)

    def get_organism_acronym(self, tax_id: int) -> Optional[str]:
        """
        Retrieve acronym from local dataset.
        """
        match = self.df_acronym[self.df_acronym["TaxID"] == str(tax_id)]
        if not match.empty:
            return match.iloc[0]["Acronym"]
        return None

    def get_genome_size(self, tax_id: int) -> Optional[str]:
        match = self.df_data[self.df_data["TaxID"] == str(tax_id)]
        if not match.empty:
            return match.iloc[0]["Size"]
        return None

    def get_organism_disease(self, tax_id: int) -> Optional[str]:
        match = self.df_data[self.df_data["TaxID"] == str(tax_id)]
        if not match.empty:
            return match.iloc[0]["Disease"]
        return None

    def get_organism_transmission(self, tax_id: int) -> Optional[str]:
        match = self.df_data[self.df_data["TaxID"] == str(tax_id)]
        if not match.empty:
            return match.iloc[0]["Transmission"]
        return None

    def get_organism_hosts(self, tax_id: int) -> Optional[str]:
        match = self.df_data[self.df_data["TaxID"] == str(tax_id)]
        if not match.empty:
            return match.iloc[0]["Host"]
        return None

    def get_organism_rank(self, tax_id: int, rank: str) -> Optional[str]:
        """
        Retrieve a specific taxonomic rank (family, genus, etc.).
        """
        lineage = self.ncbi.get_lineage(tax_id)
        ranks = self.ncbi.get_rank(lineage)
        names = self.ncbi.get_taxid_translator(lineage)

        for tid in lineage:
            if ranks.get(tid) == rank:
                return names.get(tid)

        return None
