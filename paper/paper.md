---
title: "BIO-J.A.R.V.I.S.: Automated Clinical Interpretation for Metagenomic Reports"
tags:
  - python
  - metagenomics
  - bioinformatics
authors:
  - name: Gustavo Bezerra de Andrade
    orcid: 0009-0007-2705-9466
    affiliation: 1
  - name: Deyvid Emanuel Amgarten
    orcid: 0000-0002-2612-5990
    affiliation: 2
affiliations:
  - name: Instituto Israelita de Ensino e Pesquisa Albert Einstein (IIEPAE/SBIBAE), São Paulo, Brazil
    index: 1
  - name: Genesis Genomics, São Paulo, Brazil
    index: 2
date: "2025-12-09"
bibliography: paper.bib
---
# Summary

Clinical metagenomics is an emerging approach that enables the identification of pathogens directly from raw patient samples, eliminating the need for microbial culture or targeted molecular assays. As this methodology becomes increasingly common in clinical and laboratory settings, there is a growing demand for tools that support the standardized and reproducible interpretation of resulting data.

Here we present Bio-J.A.R.V.I.S., a standalone Python application designed to automate the generation of clinical interpretations from taxonomic identifications produced by metagenomic workflows. The system integrates generative artificial intelligence models with bioinformatics libraries, enabling retrieval of taxonomic information, summarization of relevant organism characteristics, and generation of consistent, accessible clinical text. Bio-J.A.R.V.I.S. was evaluated through A/B testing with physicians and clinical analysts, demonstrating high acceptance and significant potential to streamline diagnostic workflows.

# Statement of need

Clinical metagenomics has substantially transformed infectious disease diagnostics by enabling the simultaneous detection of multiple pathogens directly from biological samples. Despite these advances, interpretation of metagenomic results remains a critical bottleneck—particularly in culture-negative infections, rare or emerging pathogens, and complex clinical scenarios. The generation of clinically meaningful interpretative text often requires extensive manual effort and specialized expertise, as illustrated by episodes within our group involving the identification of arenavirus and hantavirus infections.

Additionally, the increasing volume of sequencing data has heightened the need for fast, standardized, and reproducible interpretations. Although significant progress has been made in sequencing technologies and bioinformatics pipelines, the absence of open-source tools capable of automatically converting taxonomic outputs into clinically oriented narratives has limited widespread implementation in routine diagnostics.

Bio-J.A.R.V.I.S. addresses this gap by functioning as a downstream generative AI–based microservice that transforms validated organism information into structured clinical interpretations. The system incorporates previously authored clinician-reviewed texts to guide model behavior, producing summaries that are clear, consistent, and aligned with clinical reporting practices. By reducing manual workload and enhancing interpretative standardization, Bio-J.A.R.V.I.S. supports operational efficiency and contributes to broader adoption of metagenomics in infectious disease diagnostics.

# Evaluation and validation

Bio-J.A.R.V.I.S. was evaluated using an exploratory A/B testing framework conducted by the authors. The study compared pairs of automatically generated clinical interpretations derived from identical taxonomic inputs but different prompt formulations.

Initial statistical analysis was performed using global and pairwise chi-square tests to assess differences in prompt preference. The global chi-square test did not reveal a statistically significant difference between prompts (χ² = 1.83, p = 0.61), and none of the pairwise comparisons reached significance at the 0.05 level. These results indicate that, under frequentist hypothesis testing, the prompts are largely comparable in terms of user preference, with small observed effect sizes (global Cohen’s w = 0.14).

Given the limited sample size and the exploratory nature of prompt optimization, additional Bayesian modeling was applied to better characterize relative prompt performance. A Bradley–Terry model was used to estimate latent prompt strengths across all pairwise comparisons, followed by a Bayesian bootstrap analysis to estimate the probability of each prompt being the best-performing option. This analysis identified prompt 4 as the most likely best-performing variant, with a 72.9% probability of being optimal, despite the absence of statistically significant differences in classical hypothesis testing.

Taken together, these results suggest that while prompt variants are broadly similar in perceived quality, Bayesian analysis supports the selection of prompt 4 as the most promising formulation for clinical interpretation generation. This approach reflects a risk-aware decision strategy commonly adopted in applied clinical and computational settings, where practical relevance and probabilistic dominance are considered alongside formal statistical significance.

# Features

Bio-J.A.R.V.I.S. provides a set of command-line tools designed to automate the retrieval, interpretation, and generation of clinical text from metagenomic results:

- **taxid** and **organism_name**Bio-J.A.R.V.I.S. allows users to provide either a TaxID or an organism name, which is resolved against the NCBI taxonomy database using the ETE4 toolkit. Once the organism is identified, the system retrieves additional information from the NCBI nucleotide database through BioPython (Entrez). These data are processed by the generative model to produce a structured clinical interpretation.

  - **Input**: Valid TaxID or organism name as recorded in NCBI.
  - **Output**: Clinical interpretation text printed to stdout.
- **portuguese** and **english**Users may specify the output language of the generated interpretation through optional language flags. Bio-J.A.R.V.I.S. currently supports American English and Brazilian Portuguese. If no language flag is provided, English is used as the default.

  - **Input**: -eng (or --english) or -ptbr (or --portuguese).
  - **Output**: Clinical interpretation text in the selected language.
- **output** and **format**Users may save generated interpretations to a file using the output flag. If only a filename is provided (e.g., `name_here`), Bio-J.A.R.V.I.S. interprets it as the output file and saves a JSON by default, using the TaxID as the key and the generated text as the value. If a directory structure is included (e.g., `folder/archive_name`), the system automatically creates the directory if needed. Output format may be explicitly defined with the `-f` or `--format` flag (JSON or TXT). If no format is specified, JSON is used.

  - **Input**: -o or --output; optional -f or --format (json or txt).
  - **Output**: File saved at the specified location in the chosen or default format.
- **model**Bio-J.A.R.V.I.S. allows users to select among different generative AI models. Because clinical reporting requires low variability and high factual consistency, the system provides two additional models beyond the default (Amazon Nova Micro). Selection is performed via numeric identifiers.

  - **Input**: -m or --model followed by a model name: `deepsee` (for DeepSeek R1) or `claude` (for Claude 3.7 Sonnet).
  - **Output**: Clinical interpretation generated using the selected model.

# State of the field

Clinical metagenomics has advanced significantly over the past decade, driven by improvements in next-generation sequencing (NGS), the expansion of genomic databases such as NCBI, and a robust ecosystem of bioinformatics tools. Established solutions—including Kraken2, Centrifuge, MetaPhlAn, Kaiju, and IDseq—primarily focus on tasks such as taxonomic classification, genome assembly, variant detection, or quality control of sequencing data. These systems represent essential components of contemporary metagenomic workflows.

Despite these advances, current tools rarely address the interpretative stage of metagenomic diagnostics. Most platforms output taxa lists, abundance tables, or phylogenetic profiles but do not generate clinically oriented narratives that contextualize the relevance of detected organisms. Interpretation typically remains the responsibility of infectious disease specialists, microbiologists, or clinical analysts, who must consult external resources—literature databases, case reports, taxonomic repositories, and institutional guidelines—to produce comprehensive clinical summaries. This manual process is time-consuming, inconsistent across professionals, and increasingly impractical given rising sequencing throughput.

Artificial intelligence applications in microbiology have largely focused on predictive modeling, antimicrobial resistance inference, or phenotype–genotype association, with limited attention toward automating clinical interpretation. There is currently no widely adopted open-source tool that transforms taxonomic identifications into standardized clinical narratives using generative AI. Existing laboratory reporting systems performing similar tasks are typically proprietary, restricting broader access, reproducibility, and validation.

Bio-J.A.R.V.I.S. addresses this gap by operating downstream of existing metagenomic pipelines to generate consistent, explainable, and clinically relevant interpretative text. By integrating established bioinformatics libraries with generative models configured for low creativity and high factual precision, Bio-J.A.R.V.I.S. provides a reproducible, accessible, and open-source solution to a critical—but underrepresented—stage of metagenomic diagnostics.

# Code availability

The full source code for Bio-J.A.R.V.I.S., including documentation and example usage, is openly available on GitHub at:
**https://github.com/omicsintellab/Bio-J.A.R.V.I.S**

The repository contains installation instructions, command-line examples, and detailed guidance for executing the tool in a standalone environment. No dependencies beyond those listed in the repository are required, and the complete workflow can be reproduced directly from the provided source code.

# Data availability

Bio-J.A.R.V.I.S. includes three CSV files containing curated organism metadata and clinician-authored interpretative texts used to enrich the prompting strategy of the generative model. These datasets are publicly available within the project’s GitHub repository and can be accessed directly for inspection or extension.

In addition to the included datasets, Bio-J.A.R.V.I.S. retrieves organism information from publicly accessible NCBI resources—specifically NCBI Entrez (nucleotide database) and NCBI Taxonomy via ETE4. All external data used by the tool are openly available, ensuring full reproducibility of the workflow.

# Acknowledgements

This project was funded by the São Paulo Research Foundation (FAPESP) through an undergraduate research scholarship. The work was supported by the Instituto Israelita de Ensino e Pesquisa Albert Einstein (IIEPAE/SBIBAE), São Paulo, Brazil, and supervised by Professor Deyvid E. Amgarten, whose guidance was essential to the development of this project.

# References
