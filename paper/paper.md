---
title: "BIO-J.A.R.V.I.S.: Automated Clinical Interpretation for Metagenomic Reports"

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

Clinical metagenomics has emerged as a powerful approach for infectious disease diagnostics, enabling unbiased identification of pathogens directly from raw patient samples without the need for microbial culture or targeted molecular assays. Over the past decade, this methodology has transitioned from a primarily research-driven technique to an increasingly adopted clinical practice, supported by advances in next-generation sequencing technologies, standardized laboratory workflows, and curated genomic reference databases.

As clinical metagenomics becomes more widely implemented in routine diagnostic settings, there is a growing demand for tools that support standardized, reproducible, and clinically interpretable reporting of results. Here we present  **Bio-J.A.R.V.I.S.** , a standalone Python application designed to automate the generation of clinical interpretations from taxonomic identifications produced by metagenomic workflows. The system integrates generative artificial intelligence models with established bioinformatics libraries, enabling automated retrieval of taxonomic information, summarization of relevant organism characteristics, and generation of consistent, accessible clinical text suitable for diagnostic reporting.

Bio-J.A.R.V.I.S. was evaluated through structured A/B testing with physicians and clinical analysts, demonstrating high user acceptance and substantial potential to streamline interpretative workflows in clinical metagenomics.

# Statement of need

Clinical metagenomics has substantially transformed infectious disease diagnostics by enabling the simultaneous detection of multiple pathogens directly from biological samples, particularly in cases where conventional culture-based or targeted molecular methods fail. Despite these advances, interpretation of metagenomic results remains a critical bottleneck in clinical implementation, especially in culture-negative infections, rare or emerging pathogens, and complex clinical scenarios requiring expert contextualization.

The generation of clinically meaningful interpretative text often requires extensive manual effort and specialized expertise. In practice, clinicians and laboratory specialists must synthesize information from diverse external sources, including taxonomic databases, primary literature, case reports, and institutional guidelines. This challenge is exemplified by real-world diagnostic scenarios such as arenavirus and hantavirus infections, where rapid access to accurate organism-specific clinical context is essential for patient management.

Additionally, the rapidly increasing volume of sequencing data produced by modern laboratories has intensified the need for fast, standardized, and reproducible interpretation strategies. Although sequencing technologies and upstream bioinformatics pipelines have matured considerably, there remains a lack of open-source tools capable of automatically converting taxonomic outputs into clinically oriented narratives suitable for diagnostic reporting.

Bio-J.A.R.V.I.S. addresses this gap by functioning as a downstream generative AI–based microservice that transforms validated organism information into structured clinical interpretations. The system incorporates clinician-authored and clinician-reviewed reference texts to guide model behavior, ensuring that generated summaries remain clear, consistent, and aligned with established clinical reporting practices. By reducing manual workload and improving interpretative standardization, Bio-J.A.R.V.I.S. supports operational efficiency and facilitates broader adoption of clinical metagenomics.

# Evaluation and validation

Bio-J.A.R.V.I.S. was evaluated using an exploratory A/B testing framework conducted by the authors, focusing on the comparative quality of automatically generated clinical interpretations. Pairs of interpretations were generated from identical taxonomic inputs using different prompt formulations and were independently assessed by physicians and clinical analysts.

Initial statistical analysis employed global and pairwise chi-square tests to assess differences in prompt preference. The global chi-square test did not identify statistically significant differences between prompts, and none of the pairwise comparisons reached significance at the 0.05 level, indicating broadly comparable performance across prompt variants with small observed effect sizes.

Given the limited sample size and the exploratory nature of prompt optimization, complementary Bayesian modeling was applied to better characterize relative prompt performance. A Bradley–Terry model was used to estimate latent prompt strengths across all pairwise comparisons, followed by Bayesian bootstrap analysis to estimate the probability of each prompt being the best-performing variant. This analysis identified one prompt formulation as the most likely optimal choice, despite the absence of statistically significant differences under frequentist hypothesis testing.

Taken together, these results support the use of probabilistic and Bayesian approaches for decision-making in applied clinical and computational settings, where practical relevance and robustness may be prioritized alongside formal statistical significance.

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

Clinical metagenomics has advanced rapidly over the past decade, driven by improvements in next-generation sequencing technologies, the expansion of genomic reference databases such as NCBI, and the development of robust bioinformatics tools. Widely adopted platforms—including Kraken2, Centrifuge, MetaPhlAn, Kaiju, and IDseq—primarily address upstream analytical tasks such as taxonomic classification, genome assembly, and quality control.

Despite these advances, most existing tools do not address the interpretative stage of metagenomic diagnostics. Outputs are typically limited to taxa lists or abundance tables, leaving clinical interpretation to domain experts who must manually synthesize information from disparate sources. This manual process is time-consuming, subject to inter-observer variability, and increasingly impractical given rising sequencing throughput.

While artificial intelligence has been applied to microbiology in areas such as antimicrobial resistance prediction and phenotype–genotype association, the use of generative foundation models for automated clinical interpretation remains limited. Existing systems with similar functionality are often proprietary, restricting transparency, reproducibility, and independent validation.

Bio-J.A.R.V.I.S. addresses this unmet need by operating downstream of existing metagenomic pipelines to generate consistent, explainable, and clinically relevant interpretative text. By integrating established bioinformatics libraries with generative models configured for low creativity and high factual precision, Bio-J.A.R.V.I.S. provides an open-source and reproducible solution to a critical but underrepresented stage of clinical metagenomic diagnostics.

# Code availability

The full source code for Bio-J.A.R.V.I.S., including documentation and example usage, is openly available on GitHub at [https://github.com/omicsintellab/Bio-J.A.R.V.I.S](). The repository contains installation instructions, command-line examples, and detailed guidance for executing the tool in a standalone environment.

# Data availability

Bio-J.A.R.V.I.S. includes curated CSV files containing organism metadata and clinician-authored interpretative texts used to inform the prompting strategy of the generative model. These datasets are publicly available within the project’s GitHub repository.

In addition, the tool retrieves organism information from publicly accessible NCBI resources, including NCBI Entrez and the NCBI Taxonomy database via ETE4, ensuring full reproducibility of the workflow.

# Acknowledgements

This project was funded by the São Paulo Research Foundation (FAPESP) through an undergraduate research scholarship. The work was supported by the Instituto Israelita de Ensino e Pesquisa Albert Einstein (IIEPAE/SBIBAE), São Paulo, Brazil, and supervised by Professor Deyvid E. Amgarten.

# References
