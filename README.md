
# 🧬 BIO - J.A.R.V.I.S

**Just an Artificial Reasoning and Very Interpretative System**

BIO - J.A.R.V.I.S is a bioinformatics tool designed to generate **clinical records effortlessly — as simple as breathing.**

---

## 🚀 Quick Start

Let’s get you up and running!

1. **Clone this repository** and open the project directory.
2. **Create a virtual environment** to keep your dependencies clean:

   ```bash
   python3 -m venv venv

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

> 💡 BIO-J.A.R.V.I.S requires a Unix-based operating system (Linux or macOS) due to library dependencies.

---

## 🔐 AWS Setup

BIO - J.A.R.V.I.S uses **AWS Bedrock services** and supports **two authentication methods** that coexist without breaking each other.

### Option 1 — Environment-based authentication (default)

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

> ℹ️ This behaves exactly as before and requires no CLI changes.

---

### Option 2 — CLI-based authentication using `--api-key` (new)

For quick local testing or demos, you can now **optionally provide an AWS Bedrock Bearer Token directly via the CLI**, without configuring AWS credentials beforehand.

```bash
python3 bio_jarvis.py -tx 2697049 --api-key ABCDEFGHIJKLMNOP...
```

#### How it works

* If `--api-key` is provided:

  * The value is stored as `AWS_BEARER_TOKEN_BEDROCK` in `.env`
  * Authentication uses the provided key
* If `--api-key` is **not** provided:

  * The tool falls back to existing `.env` or AWS credentials
* No existing authentication flow is broken

> ⚠️ If the provided API key is invalid, BIO - J.A.R.V.I.S will automatically fall back to any valid AWS credentials already configured.

---

## 🧠 Running BIO-J.A.R.V.I.S

Once everything’s set up, activate your virtual environment if it’s not already running:

```bash
source venv/bin/activate
```

Run using a **TaxID**:

```bash
python3 bio_jarvis.py -tx 2697049
```

Run using an **organism name**:

```bash
python3 bio_jarvis.py -n "Severe acute respiratory syndrome coronavirus 2"
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

Automated tests are powered by `pytest` and focus on the AWS Bedrock integration layer so you can verify critical behavior without live AWS credentials.

1. Activate your virtual environment.
2. Install dependencies (only required once): `pip install -r requirements.txt`
3. Run the suite:

   ```bash
   pytest
   ```

The mocked tests confirm that prompt payloads are built correctly and that Bedrock responses are parsed safely, including error handling for malformed responses.

* `tests/test_aws_handler.py` validates Bedrock request payloads and response parsing.
* `tests/test_assistant.py` checks assistant wiring and organism metadata handling.
* All tests run automatically via GitHub Actions on every push and pull request.

---

## 🧩 Dependencies

BIO - J.A.R.V.I.S runs on **Python 3**, so make sure you have it installed and up to date:
👉 [Download Python 3](https://www.python.org/downloads/)

### Required Python libraries:

* [ETE4 Toolkit](https://jorgebotas.github.io/ete4-documentation/)
* [BioPython (Entrez module)](https://biopython.org/docs/1.76/api/Bio.Entrez.html)
* [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
* [Python-dotenv](https://pypi.org/project/python-dotenv/)
* [Pandas](https://pandas.pydata.org/)

---

## 🧾 Main Script

**`bio_jarvis.py`** — Core entry point for running the system.

---

## 🧬 About the Project

This tool was developed as part of an **undergraduate research project** at the
**Albert Einstein Israelite Faculty of Health Sciences, São Paulo, Brazil.**

---

## 🧑‍💻 Author

**[Gustavo Bezerra](https://github.com/BizerraGuU)**

For bugs, suggestions, or improvements, contact:
📩 **[deyvid.amgarten@usp.br](mailto:deyvid.amgarten@usp.br)**

---

## 📚 Reference and Citation

> Coming soon

---

## 🧾 Changelog

**BIO - J.A.R.V.I.S v1.1 — December 2025**

* Added optional CLI-based authentication via `--api-key`
* Preserved full backward compatibility with `.env`-based AWS credentials
* Improved usability for local testing and demos

---

## ⚖️ License

This project is licensed under the MIT License.

```

