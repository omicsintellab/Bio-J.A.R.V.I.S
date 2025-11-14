

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

> 💡 BIO-J.A.R.V.I.S requires a Unix-based operating system (Linux or macOS) due to library dependencies.

---

## 🔐 AWS Setup

This project uses **AWS Bedrock services**, so you’ll need to configure your credentials.

1. In the root directory, **create a file** named `.env`.
2. Paste your BEDROCK_API_KEY and AWS_DEFAULT_REGION into it, like so:

   ```bash
   BEDROCK_API_KEY='...'
   AWS_DEFAULT_REGION=us-east-1 
   ```

> Make sure to use a long-term ***BEDROCK_API_KEY*** so you only need to set it once.

---

## 🧠 Running BIO-J.A.R.V.I.S

Once everything’s set up, activate your virtual environment if it’s not already running:

```bash
source venv/bin/activate
```

Then, simply run:

```bash
python3 bio_jarvis.py -tx 2697049
```

This runs the script using a **TaxID**.
If you prefer to run it by **organism name**, use:

```bash
python3 bio_jarvis.py -n "Severe acute respiratory syndrome coronavirus 2"
```

> ⚠️ Make sure the organism name you enter is spelled correctly!

---

## 🧩 Dependencies

BIO-J.A.R.V.I.S runs on **Python 3**, so make sure you have it installed and up to date:
👉 [Download Python 3](https://www.python.org/downloads/)

### Required Python libraries:

* [ETE4 Toolkit](https://jorgebotas.github.io/ete4-documentation/)
* [BioPython (Entrez module)](https://biopython.org/docs/1.76/api/Bio.Entrez.html)
* [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
* [Python-dotenv](https://pypi.org/project/python-dotenv/)
* [Pandas](https://pandas.pydata.org/)

> Click on the library names to view their documentation.
---

## 🧾 Main Script

**`bio_jarvis.py`** – This is the core script that runs the entire system.

---

## 🧬 About the Project

This tool was developed as part of my **undergraduate research project** conducted at the
**Albert Einstein Israelite Faculty of Health Sciences, São Paulo, Brazil.**

---

## 🧑‍💻 Author

**[Gustavo Bezerra](https://github.com/BizerraGuU)**

For bugs, suggestions, or improvements, please reach out to:
📩 **[deyvid.amgarten@usp.br](mailto:deyvid.amgarten@usp.br)**

---

## 📚 Reference and Citation

> Coming soon

---

## 🧾 Changelog

**BIO - J.A.R.V.I.S v1.0 — December 2025**

* Initial release
* For feedback or issues, feel free to get in touch!

---

## ⚖️ License

> Coming soon
