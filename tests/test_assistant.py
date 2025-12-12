import pandas as pd
import pytest

from assistant import MetagenomicsAssistant


class _DummyAwsHandler:
    """Minimal placeholder passed into MetagenomicsAssistant."""


@pytest.fixture(autouse=True)
def _stub_csv(monkeypatch):
    """Stub pandas.read_csv so tests avoid reading real files."""

    def fake_read_csv(path, *_, **__):
        if "old_reports" in path:
            return pd.DataFrame({"content": ["style-a", "style-b"]})
        if "data_for_biojarvis" in path:
            return pd.DataFrame({"TaxID": [], "Diseases": [], "Transmissions": [], "Hosts": []})
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


def test_build_bedrock_request_uses_prompt_helpers(monkeypatch):
    assistant = MetagenomicsAssistant(aws_handler=_DummyAwsHandler())
    assistant.set_text_to_prompt = lambda: ["style-a", "style-b"]

    captured = {}

    def fake_set_prompt(info_dict, references):
        captured["info"] = info_dict
        captured["refs"] = references
        return "FORMATTED_PROMPT"

    def fake_get_response(prompt_text):
        captured["prompt"] = prompt_text
        return b"encoded-payload"

    monkeypatch.setattr("assistant.set_prompt_text", fake_set_prompt)
    monkeypatch.setattr("assistant.AwsHandler.get_bedrock_prompt_response", fake_get_response)

    result = assistant.build_bedrock_request({"Name": "Test organism"})

    assert result == b"encoded-payload"
    assert captured["info"] == {"Name": "Test organism"}
    assert captured["refs"] == ["style-a", "style-b"]
    assert captured["prompt"] == "FORMATTED_PROMPT"


def test_set_organism_fields_filters_null_entries(monkeypatch):
    assistant = MetagenomicsAssistant(aws_handler=_DummyAwsHandler())

    monkeypatch.setattr(MetagenomicsAssistant, "get_organism_name", lambda self, tax_id: "Organism X")
    monkeypatch.setattr(MetagenomicsAssistant, "get_organism_acronym", lambda self, tax_id: None)
    monkeypatch.setattr(MetagenomicsAssistant, "get_genome_size", lambda self, tax_id: 2048)
    monkeypatch.setattr(MetagenomicsAssistant, "get_organism_disease", lambda self, tax_id: "Example disease")
    monkeypatch.setattr(MetagenomicsAssistant, "get_organism_transmission", lambda self, tax_id: "")
    monkeypatch.setattr(MetagenomicsAssistant, "get_organism_hosts", lambda self, tax_id: "Humans")

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
