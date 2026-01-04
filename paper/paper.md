---
title: "BIO-J.A.R.V.I.S.: Automated Clinical Interpretation for Metagenomic Reports"

keywords:
  - python
  - metagenomics
  - bioinformatics

authors:
  - name: Gustavo Bezerra de Andrade
    orcid: 0009-0007-2705-9466
    affiliation: 1
  - name: Fernanda de Mello Malta
    orcid: 0000-0001-8887-5060
    affiliation: 2
  - name: João Renato Rebello Pinho
    orcid: 0000-0003-3999-0489
    affiliation: 2
  - name: Deyvid Amgarten
    orcid: 0000-0002-2612-5990
    affiliation: "1,3"
    corresponding: true

affiliations:
  - name: Faculdade Israelita de Ciências da Saúde Albert Einstein, Hospital Israelita Albert Einstein, São Paulo, Brazil
    index: 1
  - name: Hospital Israelita Albert Einstein, São Paulo, Brazil
    index: 2
  - name: Genesis Genomics, São Paulo, Brazil
    index: 3

date: "2025-12-09"
bibliography: paper.bib
---
## Summary

Clinical metagenomics (mNGS) has emerged as a powerful approach for infectious disease diagnostics, enabling unbiased identification of pathogens directly from raw patient samples without the need for microbial culture or targeted molecular assays. Over the past decade, this methodology has transitioned from a primarily research-driven technique to an increasingly adopted clinical practice, supported by advances in next-generation sequencing technologies (NGS) and curated genomic reference databases.

As mNGS becomes more widely implemented in routine diagnostic settings, there is a growing demand for tools that support standardized, reproducible, and clinically interpretable reporting of results. Here we present **Bio-J.A.R.V.I.S.**, a standalone Python application designed to automate the generation of clinical interpretations from taxonomic identifications produced by metagenomic bioinformatics workflows. The system integrates generative artificial intelligence features with established bioinformatics libraries, enabling automated retrieval of taxonomic information, summarization of relevant organism characteristics, and generation of consistent, accessible clinical text suitable for diagnostic reporting.

Bio-J.A.R.V.I.S. was evaluated through structured A/B testing with physicians and clinical analysts, demonstrating high user acceptance and substantial potential to streamline interpretative workflows in clinical metagenomics.

## Statement of need

Clinical metagenomics has substantially transformed infectious disease diagnostics by enabling
the simultaneous detection of multiple pathogens directly from biological samples. Despite
these advances, interpretation of metagenomic results remains a critical bottleneck,
particularly in culture-negative infections, rare or emerging pathogens, and complex clinical
scenarios [@chiu2019clinical]. The generation of clinically meaningful interpretative text often
requires extensive manual effort and specialized expertise, as illustrated by our diagnostic
experiences with arenavirus and hantavirus emerging infections
[@jcm_hantavirus_2020; @cmr_arenavirus_2024].

Additionally, the increasing volume of sequencing data has heightened the need for fast,
standardized, and reproducible interpretations. Although significant progress has been made
in sequencing technologies and bioinformatics pipelines, the absence of open-source tools
capable of automatically converting taxonomic outputs into clinically oriented narratives has
limited widespread implementation in routine diagnostics.

Bio-J.A.R.V.I.S. addresses this gap by functioning as a downstream generative AI–based
microservice that transforms validated organism information into structured clinical
interpretations. The system incorporates previously authored clinician-reviewed texts to guide
model behavior (through two-shot prompting), producing summaries that are clear, consistent, and aligned with clinical
reporting practices. By reducing manual workload and enhancing interpretative
standardization,Bio-J.A.R.V.I.S. supports operational efficiency and contributes to broader
adoption of metagenomics in infectious disease diagnostics.

## Features

Bio-J.A.R.V.I.S. provides a command-line tool designed to automate the retrieval, interpretation, and generation of clinical text from metagenomic results.

### TaxID and Organism Name

Users may provide either a NCBI standardized TaxID or an organism name, which is resolved against the NCBI Taxonomy database using the ETE4 toolkit [@ete4]. Once the organism is identified, the system retrieves additional information from the NCBI nucleotide database via BioPython library [@biopython; @ncbi_entrez]. These data are subsequently processed by the generative model to produce a structured clinical interpretation.

**Input:** Valid TaxID or organism name as recorded in NCBI.
**Output:** Clinical interpretation text printed to standard output.

### Portuguese and English

Bio-J.A.R.V.I.S. supports multilingual output, allowing users to specify American English or Brazilian Portuguese through optional language flags. English is used as the default language when no flag is provided.

**Input:** `--language EN` or `--language PT`
**Output:** Clinical interpretation text in the selected language.

### Output and Format

Generated interpretations may be saved to a file using an output flag to downstream bioinformatics pipelines. If only a filename is provided, the system saves the output as a JSON file by default, using the TaxID as the key and the generated text as the value. Output format may also be explicitly defined as JSON or plain text.

**Input:** `--output`; optional `--format` (`json` or `txt`)
**Output:** File saved at the specified location in the chosen or default format.

### Generative AI Provider

Bio-J.A.R.V.I.S. allows users to select between two generative AI providers: AWS Bedrock and Google Gemini. Because clinical reporting requires low variability and high factual consistency, the system supports models configured for deterministic behavior and reduced creative variance, following best practices in prompt engineering and inference control [@delavega2023temperature; @duarte2025systemprompts].

**Input:** `--provider` followed by `aws` or `gemini`
**Output:** Clinical interpretation generated using the selected model.

For aws provider, the amazon.nova-micro-v1:0 model is used. For gemini provider, the gemini-2.5-flash model is used.

## State of the field

Clinical metagenomics has substantially transformed infectious disease diagnostics by enabling
the simultaneous detection of multiple pathogens directly from biological samples. Despite
these advances, interpretation of metagenomic results remains a critical bottleneck,
particularly in culture-negative infections, rare or emerging pathogens, and complex clinical
scenarios [@chiu2019clinical]. The generation of clinically meaningful interpretative text often
requires extensive manual effort and specialized expertise, as illustrated by diagnostic
experiences involving arenavirus and hantavirus infections
[@jcm_hantavirus_2020; @cmr_arenavirus_2024].

Additionally, the increasing volume of sequencing data has heightened the need for fast,
standardized, and reproducible interpretations. Although significant progress has been made
in sequencing technologies and bioinformatics pipelines, the absence of open-source tools
capable of automatically converting taxonomic outputs into clinically oriented narratives has
limited widespread implementation in routine diagnostics.

Bio-J.A.R.V.I.S. addresses this gap by functioning as a downstream generative AI–based
microservice that transforms validated organism information into structured clinical
interpretations. The system incorporates previously authored clinician-reviewed texts to guide
model behavior, producing summaries that are clear, consistent, and aligned with clinical
reporting practices. By reducing manual workload and enhancing interpretative
standardization, Bio-J.A.R.V.I.S. supports operational efficiency and contributes to broader
adoption of metagenomics in infectious disease diagnostics.

## Code availability

The full source code for Bio-J.A.R.V.I.S., including documentation and example usage, is openly available on GitHub at
[https://github.com/omicsintellab/Bio-J.A.R.V.I.S](https://github.com/omicsintellab/Bio-J.A.R.V.I.S)

## Data availability

Bio-J.A.R.V.I.S. includes curated CSV files containing organism metadata and clinician-authored interpretative texts used to inform the prompting strategy of the generative model. These datasets are publicly available within the project’s GitHub repository.

In addition, the tool retrieves organism information from publicly accessible NCBI resources, including NCBI Entrez and the NCBI Taxonomy database via ETE4, and from Viral Zone datasets, ensuring full reproducibility of the workflow.

## Acknowledgements

This project was funded by the São Paulo Research Foundation (FAPESP) through an undergraduate research scholarship. The work was supported by the Instituto Israelita de Ensino e Pesquisa Albert Einstein (IIEPAE/SBIBAE), São Paulo, Brazil, and supervised by Professor Deyvid E. Amgarten.

## References
