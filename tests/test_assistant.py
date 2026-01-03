import pandas as pd
import pytest

from assistant import MetagenomicsAssistant


class _DummyLLMHandler:
    """Minimal placeholder passed into MetagenomicsAssistant."""

    def generate_text(self, prompt: str) -> str:
        return "GENERATED_REPORT_CONTENT"


@pytest.fixture(autouse=True)
def _stub_csv(monkeypatch):
    """Stub pandas.read_csv so tests avoid reading real files."""

    def fake_read_csv(path, *_, **__):
        if "old_reports" in path:
            return pd.DataFrame({"content": ["style-a", "style-b"]})
        if "data_for_biojarvis" in path:
            return pd.DataFrame(
                {"TaxID": [], "Diseases": [], "Transmissions": [], "Hosts": []}
            )
        if "acronyms" in path:
            return pd.DataFrame({"TaxID": [], "Acronym": []})
        raise AssertionError(f"Unexpected file read: {path}")

    monkeypatch.setattr("assistant.pd.read_csv", fake_read_csv)


@pytest.fixture(autouse=True)
def _stub_taxonomy(monkeypatch):
    """Avoid downloading taxonomy data during tests."""

    class DummyNCBI:
        def __init__(self):
            pass

    monkeypatch.setattr("assistant.NCBITaxa", DummyNCBI)


def test_generate_report_uses_prompt_helpers(monkeypatch):
    dummy_handler = _DummyLLMHandler()
    assistant = MetagenomicsAssistant(llm_handler=dummy_handler)
    assistant.set_text_to_prompt = lambda: ["style-a", "style-b"]

    captured = {}

    def fake_set_prompt(info_dict, references, language):
        captured["info"] = info_dict
        captured["refs"] = references
        captured["language"] = language
        return "FORMATTED_PROMPT"

    monkeypatch.setattr("assistant.set_prompt_text", fake_set_prompt)

    # Mock data retrieval methods to avoid NCBI calls
    monkeypatch.setattr(
        MetagenomicsAssistant, "get_organism_name", lambda self, tax_id: "Organism X"
    )
    monkeypatch.setattr(
        MetagenomicsAssistant, "get_organism_acronym", lambda self, tax_id: None
    )
    monkeypatch.setattr(
        MetagenomicsAssistant, "get_genome_size", lambda self, tax_id: 2048
    )
    monkeypatch.setattr(
        MetagenomicsAssistant,
        "get_organism_disease",
        lambda self, tax_id: "Example disease",
    )
    monkeypatch.setattr(
        MetagenomicsAssistant, "get_organism_transmission", lambda self, tax_id: ""
    )
    monkeypatch.setattr(
        MetagenomicsAssistant, "get_organism_hosts", lambda self, tax_id: "Humans"
    )

    def fake_rank(self, tax_id, rank):
        return {"family": "Familiaceae", "genus": "Genus test"}.get(rank)

    monkeypatch.setattr(MetagenomicsAssistant, "get_organism_rank", fake_rank)

    # We also need to spy on the handler's generate_text to verify it received the prompt
    original_generate_text = dummy_handler.generate_text

    def fake_generate_text(prompt):
        captured["prompt_sent_to_llm"] = prompt
        return original_generate_text(prompt)

    dummy_handler.generate_text = fake_generate_text

    result = assistant.generate_report("12345", language="english")

    assert result == "GENERATED_REPORT_CONTENT"
    assert captured["info"] == {
        "Name": "Organism X",
        "Size": "2048",
        "Diseases": "Example disease",
        "Hosts": "Humans",
        "Family": "Familiaceae",
        "Genus": "Genus test",
    }
    assert captured["refs"] == ["style-a", "style-b"]
    assert captured["language"] == "english"
    assert captured["prompt_sent_to_llm"] == "FORMATTED_PROMPT"


def test_set_organism_fields_filters_null_entries(monkeypatch):
    assistant = MetagenomicsAssistant(llm_handler=_DummyLLMHandler())

    monkeypatch.setattr(
        MetagenomicsAssistant, "get_organism_name", lambda self, tax_id: "Organism X"
    )
    monkeypatch.setattr(
        MetagenomicsAssistant, "get_organism_acronym", lambda self, tax_id: None
    )
    monkeypatch.setattr(
        MetagenomicsAssistant, "get_genome_size", lambda self, tax_id: 2048
    )
    monkeypatch.setattr(
        MetagenomicsAssistant,
        "get_organism_disease",
        lambda self, tax_id: "Example disease",
    )
    monkeypatch.setattr(
        MetagenomicsAssistant, "get_organism_transmission", lambda self, tax_id: ""
    )
    monkeypatch.setattr(
        MetagenomicsAssistant, "get_organism_hosts", lambda self, tax_id: "Humans"
    )

    def fake_rank(self, tax_id, rank):
        return {"family": "Familiaceae", "genus": "Genus test"}.get(rank)

    monkeypatch.setattr(MetagenomicsAssistant, "get_organism_rank", fake_rank)

    result = assistant.set_organism_fields("12345")

    assert result == {
        "Name": "Organism X",
        "Size": "2048",
        "Diseases": "Example disease",
        "Hosts": "Humans",
        "Family": "Familiaceae",
        "Genus": "Genus test",
    }
