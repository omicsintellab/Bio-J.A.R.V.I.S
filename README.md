# 🧬 BIO - J.A.R.V.I.S

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.00000/status.svg)](https://joss.theoj.org/papers/10.21105/joss.00000)

**Just an Artificial Reasoning and Very Interpretative System**

BIO - J.A.R.V.I.S is a bioinformatics tool designed to generate **clinical reports for metagenomics tests effortlessly.**

## 📄 Statement of Need

Clinical metagenomics enables the unbiased identification of pathogens directly from samples. However, interpreting these results requires navigating complex taxonomy and specialized medical knowledge. **BIO-J.A.R.V.I.S** bridges this gap by automating the retrieval of organism metadata from **[NCBI Genbank](https://www.ncbi.nlm.nih.gov/)** and utilizing **[Viral Zone](https://viralzone.expasy.org/)** as a trusted knowledge source to guide generative AI in producing standardized, clinically relevant interpretations. It is designed to streamline the workflow for clinical analysts and researchers who need reproducible and accessible reports from metagenomic data.

---

## 🚀 Quick Start

Let’s get you up and running!

1. **Clone this repository** and open the project directory.
2. **Create a virtual environment** to keep your dependencies clean:

   ```bash
   python3 -m venv venv
   ```

3. **Activate your virtual environment:**

   ```bash
   source venv/bin/activate
   ```

   You should now see something like this in your terminal:

   ```
   (venv) your@user Bio-J.A.R.V.I.S %
   ```
4. **Install all required dependencies:**

   ```bash
   pip3 install -r requirements.txt
   ```

   > **For Contributors**: If you want to run tests or contribute to the project, install development dependencies:
   > ```bash
   > pip3 install -r requirements-dev.txt
   > ```


> 💡 BIO-J.A.R.V.I.S requires a Unix-based operating system (Linux or macOS) due to library dependencies.

---

## 🔐 Model Setup

BIO - J.A.R.V.I.S uses **LLM services** (AWS Bedrock or Google Gemini) and supports **two authentication methods** that coexist without breaking each other.

### 1. AWS Bedrock (Default)

#### Option 1 — Environment-based authentication
This is the **existing and fully supported mechanism**.

1. In the root directory, create a file named `.env`.
2. Add your AWS credentials and region:

   ```bash
   AWS_ACCESS_KEY_ID="..."
   AWS_SECRET_ACCESS_KEY="..."
   AWS_DEFAULT_REGION="us-east-1"
   ```

Optional (if applicable):

```bash
AWS_PROFILE="your-profile"
```

#### Option 2 — CLI-based authentication using `--api-key`
For quick local testing or demos, you can provide an AWS Bedrock Bearer Token directly via the CLI.

```bash
python3 bio_jarvis.py -tx 2697049 --api-key ABCDEFGHIJKLMNOP...
```

---

### 2. Google Gemini

BIO-J.A.R.V.I.S also supports Google's Gemini models.

#### How to obtain a Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Click on **Create API key**.
3. Copy your API key.

#### Configuration
You can pass the API key via the CLI (which will save it to `.env` as `GEMINI_API_KEY`) or manually add it to `.env`:

```bash
GEMINI_API_KEY="your-gemini-api-key"
```

---

## 🧠 Running BIO-J.A.R.V.I.S

Once everything’s set up, activate your virtual environment:

```bash
source venv/bin/activate
```

### Using AWS Bedrock (Default)

Run using a **TaxID**:

```bash
python3 bio_jarvis.py -tx 2697049
```

Run using an **organism name**:

```bash
python3 bio_jarvis.py -n "Severe acute respiratory syndrome coronavirus 2"
```

### Using Google Gemini

To use Gemini, simply add the `--provider gemini` argument.

**First run (setting the key):**
```bash
python3 bio_jarvis.py -n "Escherichia coli" --provider gemini --api-key YOUR_GEMINI_KEY
```

**Subsequent runs:**
```bash
python3 bio_jarvis.py -n "Escherichia coli" --provider gemini
```

> ⚠️ Make sure the organism name you enter is spelled correctly!

---

## 📝 Saving the responses

If you want to save the generated response, you can specify the folder and the file name where the response will be saved, as well as its format.

1. Saving to a file in the root directory:

```bash
python3 bio_jarvis.py -tx 2697049 -o file_name
```

> The file **file_name** will be generated and the response will be saved as:
> **{ "taxid": "generated text" }** (JSON)

2. Saving to a file in a specified directory:

```bash
python3 bio_jarvis.py -tx 2697049 -o directory_name/file_name
```

> The file **file_name** will be generated inside **directory_name**, using:
> **{ "taxid": "generated text" }** (JSON)

---

## ✅ Running Tests

Automated tests are powered by `pytest`.

1. Activate your virtual environment.
2. Install dependencies (only required once): `pip install -r requirements.txt`
3. Run the suite:

   ```bash
   pytest
   ```

The suite covers the core logic and integrations with mocked external services:

* `tests/test_aws_handler.py` validates Bedrock request payloads and response parsing.
* `tests/test_gemini_handler.py` verifies the initialization and interaction with the Google GenAI SDK.
* `tests/test_assistant.py` checks the assistant's wiring, organism metadata handling, and provider-agnostic report generation.

---

## 🧩 Dependencies

BIO - J.A.R.V.I.S runs on **Python 3**, so make sure you have it installed and up to date:
👉 [Download Python 3](https://www.python.org/downloads/)

### Required Python libraries:

* [ETE4 Toolkit](https://jorgebotas.github.io/ete4-documentation/)
* [BioPython (Entrez module)](https://biopython.org/docs/1.76/api/Bio.Entrez.html)
* [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
* [Google Generative AI](https://pypi.org/project/google-generativeai/)
* [Python-dotenv](https://pypi.org/project/python-dotenv/)
* [Pandas](https://pandas.pydata.org/)

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and suggest improvements.

Please also note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

---

## 🧾 Main Script

**`bio_jarvis.py`** — Core entry point for running the system.

---

## 🧬 About the Project

This tool was developed as part of an **undergraduate research project** at the
**Albert Einstein Israelite Faculty of Health Sciences, São Paulo, Brazil.**

---

## 🧑‍💻 Author

**[Gustavo Bezerra](https://github.com/BeezzS)**

For bugs, suggestions, or improvements, contact:
📩 **[deyvid.emanuel@einstein.br](mailto:deyvid.emanuel@einstein.br)**

---

## 📚 Reference and Citation

If you use this software in your research, please cite our paper:

> Bezerra, G., & Amgarten, D. E. (2025). BIO-J.A.R.V.I.S.: Automated Clinical Interpretation for Metagenomic Reports. *Journal of Open Source Software (Submitted)*.

BibTeX:

```bibtex
@article{BioJarvis2025,
  author = {Gustavo Bezerra and Deyvid Emanuel Amgarten},
  title = {BIO-J.A.R.V.I.S.: Automated Clinical Interpretation for Metagenomic Reports},
  year = {2025},
  publisher = {Journal of Open Source Software},
  journal = {Journal of Open Source Software},
  url = {https://github.com/omicsintellab/Bio-J.A.R.V.I.S}
}
```

---

## 🧾 Changelog

**BIO - J.A.R.V.I.S v1.2 — January 2026**
* Added support for Google Gemini via `--provider gemini`
* Integrated Google Generative AI SDK
* Added support for API key management for Gemini

**BIO - J.A.R.V.I.S v1.1 — December 2025**

* Added optional CLI-based authentication via `--api-key`
* Preserved full backward compatibility with `.env`-based AWS credentials
* Improved usability for local testing and demos

---

## ⚖️ License

This project is licensed under the MIT License.
