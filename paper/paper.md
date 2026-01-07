---
title: "Bio-J.A.R.V.I.S.: LLM-based clinical interpretation text generation for metagenomics grounded in public reference databases"

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

date: "2026-01-07"
bibliography: paper.bib
---
## Summary

Clinical metagenomics (mNGS) has emerged as a powerful approach for infectious disease diagnostics, enabling unbiased identification of pathogens directly from raw patient samples without the need for microbial culture or targeted molecular assays. Over the past decade, this methodology has transitioned from a primarily research-driven technique to an increasingly adopted clinical practice, supported by advances in next-generation sequencing technologies (NGS) and curated genomic reference databases.

As mNGS becomes more widely implemented in routine diagnostic settings, there is a growing demand for tools that support standardized, reproducible, and clinically interpretable reporting of results. Here we present **Bio-J.A.R.V.I.S.**, a standalone Python application designed to automate the generation of clinical interpretations from taxonomic identifications produced by metagenomic bioinformatics workflows. The system integrates generative artificial intelligence features with established bioinformatics libraries, enabling automated retrieval of trusted information, summarization of relevant organism characteristics, and generation of consistent, accessible clinical text suitable for diagnostic reporting.

Bio-J.A.R.V.I.S. was evaluated through structured A/B testing with physicians and clinical analysts, demonstrating high user acceptance and substantial potential to streamline interpretative workflows in clinical metagenomics. Given the clinical context in which Bio-J.A.R.V.I.S. is used, we rely on reliable, publicly available reference databases ([NCBI](https://www.ncbi.nlm.nih.gov/) and [ViralZone](https://viralzone.expasy.org/)) as trusted knowledge sources from which organism-level information is retrieved. During testing, the following attributes were identified as the most consistently useful and well accepted: organism name, disease,modes of transmission, hosts, genome size, family, genus, and acronym (when available).


## Statement of need

Clinical metagenomics (mNGS) has substantially transformed infectious disease diagnostics by enabling the simultaneous detection of multiple pathogens directly from biological samples. Despite these advances, interpretation of metagenomic results remains a critical bottleneck, particularly in culture-negative infections, rare or emerging pathogens, and complex clinical scenarios [@chiu2019clinical]. In practice, translating a taxonomic identification into a concise, clinically oriented narrative still requires substantial manual effort and domain expertise, as illustrated by our diagnostic experiences with arenavirus and hantavirus infections [@jcm_hantavirus_2020; @cmr_arenavirus_2024].

Bio-J.A.R.V.I.S. was developed to streamline this downstream interpretive step by automatically generating standardized clinical interpretation text from taxonomic identifications. The tool retrieves organism metadata from public reference databases ([NCBI](https://www.ncbi.nlm.nih.gov/) and [ViralZone](https://viralzone.expasy.org/)) and combines these facts with clinician-authored example texts to guide generation through structured prompting. To support clinical reporting requirements, Bio-J.A.R.V.I.S. is designed to minimize variability and prioritize factual consistency while producing clear and reproducible interpretations that can be integrated into routine diagnostic workflows.

## Features

Bio-J.A.R.V.I.S. provides a command-line tool designed to automate the retrieval, interpretation, and generation of clinical text from metagenomic results.

### TaxID and Organism Name as Input

Users may provide either a NCBI standardized TaxID or an organism name, which is resolved against the NCBI Taxonomy database using the ETE4 toolkit [@ete4]. Once the organism is identified, the system retrieves additional information from the NCBI nucleotide database via BioPython and Entrez libraries [@biopython; @ncbi_entrez]. These data are subsequently processed by the LLM foundation model to produce a structured clinical interpretation.

**Input:** Valid TaxID or organism name as standardized by NCBI.
**Output:** Clinical interpretation text printed to standard output.

### Portuguese and English Text Generation

Bio-J.A.R.V.I.S. supports multilingual output, allowing users to specify American English or Brazilian Portuguese through optional language flags. English is used as the default language when no flag is provided.

**Input:** `--language EN` or `--language PT`
**Output:** Clinical interpretation text in the selected language.

### Output and Format Options

Generated interpretations may be saved to a file using an output flag to downstream bioinformatics pipelines. If only a filename is provided, the system saves the output as a JSON file by default, using the TaxID as the key and the generated text as the value. Output format may also be explicitly defined as JSON or plain text.

**Input:** `--output`; optional `--format` (`json` or `txt`)
**Output:** File saved at the specified location in the chosen or default format.

### Generative AI Provider

Bio-J.A.R.V.I.S. allows users to select between two generative AI providers: [AWS Bedrock](https://aws.amazon.com/bedrock/) and [Google Gemini](https://aistudio.google.com/). Because clinical reporting requires low variability and high factual consistency, the system supports models configured for deterministic behavior and reduced creative variance, following best practices in prompt engineering and feedback from users [@delavega2023temperature; @duarte2025systemprompts].

**Input:** `--provider` followed by `aws` or `gemini`
**Output:** Clinical interpretation generated using the selected model.

For aws provider, the amazon.nova-micro-v1:0 model is used. For gemini provider, the gemini-2.5-flash model is used. Models will be updated as new versions are released.

## State of the field

Current clinical metagenomics workflows and software ecosystems have largely focused on sequencing, quality control, taxonomic classification, and result summarization (e.g., lists of detected organisms and abundance tables). While these components are essential, they typically do not address the final-mile challenge of producing clinician-oriented interpretive narratives that contextualize an organism for reporting and decision support [@chiu2019clinical]. As a result, many laboratories still rely on manual, expert-driven writing to transform taxonomic outputs into standardized text suitable for clinical communication.

Additionally, the increasing volume of sequencing data has increased the need for fast,
standardized, and reproducible interpretations. Although significant progress has been made
in sequencing technologies and bioinformatics pipelines, the absence of open-source tools
capable of automatically converting taxonomic outputs into clinically oriented narratives has
limited widespread implementation in routine diagnostics.

Recent progress in large language models has created an opportunity to automate narrative generation; however, clinical reporting demands grounded outputs, transparent provenance of organism facts, and controlled variability to reduce the risk of inconsistent or misleading language. Bio-J.A.R.V.I.S. positions itself as a downstream interpretation layer that bridges this gap by grounding generation in public reference databases and by using structured prompting anchored in clinician-authored examples. In doing so, it complements existing metagenomic pipelines rather than replacing them, providing a reproducible mechanism to convert validated taxonomic findings into consistent, clinically aligned interpretation text.

Thus, Bio-J.A.R.V.I.S. performs the generation of a concise text that conveys informative value by using reliable knowledge from public databases (e.g., NCBI) about the identified organisms (based on their name or taxonomic identifier). As observed through interviews and a prior textual analysis, it was found that, for the generated text to be coherent with existing texts, it needed—whenever available—to include data/references for the following organism-related information: organism name, disease, modes of transmission, hosts, genome size, family, genus, and acronym (when available). A scheme of the information used to generate the text is shown in the figure below.

![Application Flowchart](../docs/application_flowchart.png)

Bio-J.A.R.V.I.S. addresses this gap by functioning as a downstream generative AI–based
microservice that transforms validated organism information into structured clinical
interpretations. The system incorporates previously authored clinician-reviewed texts to guide
model behavior, producing summaries that are clear, consistent, and aligned with clinical
reporting practices. By reducing manual workload and enhancing interpretative
standardization, Bio-J.A.R.V.I.S. supports operational efficiency and contributes to broader
adoption of metagenomics in infectious disease diagnostics.

## Code availability

The full source code for Bio-J.A.R.V.I.S., including documentation and example usage, is openly available on GitHub at
[https://github.com/omicsintellab/Bio-J.A.R.V.I.S](https://github.com/omicsintellab/Bio-J.A.R.V.I.S).
And it is also possible to use Bio-J.A.R.V.I.S. in a Web application, using the parameters available in the code as documented in the repository. Available at: [https://biojarvis.omicsintel.com/](https://biojarvis.omicsintel.com/)

## Data availability

Bio-J.A.R.V.I.S. includes curated CSV files containing organism metadata and clinician-authored interpretative texts used to inform the prompting strategy of the generative model. These datasets are publicly available within the project’s GitHub repository.

In addition, the tool retrieves organism information from publicly accessible NCBI resources, including NCBI Entrez and the NCBI Taxonomy database via ETE4, and from Viral Zone datasets, ensuring full reproducibility of the workflow.

## Acknowledgements

This study was financed, in part, by the São Paulo Research Foundation (FAPESP), Brasil. Process Number #2024/17790-9. We thank physicians, clinical analysts, and students for their valuable input and feedback. We also thank the Clinical Laboratory of the Hospital Albert Einstein for their support.

## References
