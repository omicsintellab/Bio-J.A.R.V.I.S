from Bio import Entrez

# ID from AWS MODEL: Amazon Nova Micro
MODEL_ID_1 = "amazon.nova-micro-v1:0"
MODEL_ID_GEMINI = "gemini-2.5-flash"

# Default e-mail to access NCBI with biopython
DEFAULT_EMAIL = Entrez.email = "email@email.com"

# File Paths
OLD_REPORTS_PATH = "./files/old_reports.pkl"
DATA_PATH = "./files/data_for_biojarvis.csv"
ACRONYMS_PATH = "./files/acronyms.csv"

# Prompt Template
PROMPT_TEMPLATE = """
            You are an assistant specialized in clinical and microbiological reports about pathogens in clinical metagenomics.
            Your task is to write a test report in {language}, in the formal and objective tone of medical literature.
            
            **Data Sourcing Strategy:**
            1. **Primary Source:** The structured data: {information_dict} must be used first.
            2. **Secondary Source (Internal Knowledge):** If specific fields (Disease, Transmission, Hosts) are missing from the primary source, **YOU MUST** use your own internal expert knowledge to complete the report, provided the information is scientifically established.

            **Report Rules (Strictly Enforced):**
            1. Include the information provided in the primary source. If clinical details are missing there, valid scientific knowledge of the organism should be used to describe its pathogenicity, transmission, and hosts.
            2. **STRICTLY PROHIBITED:** Never mention, imply, or discuss missing information.
            3. **ABSOLUTE PROHIBITION ON NEGATION AND UNCERTAINTY:**
                * **NEVER** write phrases like "information not available," "unknown," "no data," "further research needed," "although no data exists," "may cause," **or any phrasing that suggests the data was searched for and not found.**
                * **DO NOT** comment on the research process or the completeness of the data.
                * **DO NOT** use title.
            4. If data is still missing (e.g., organism is novel or poorly described even in scientific literature), then omit the topic entirely.
            5. Do not infer, speculate, or generalize from related taxa unless scientifically accurate for the specific organism (e.g., "Like other members of the genus...").
            6. The text must be strictly factual, affirmative, and **free of any uncertainty or discussion about data availability.**
                * The Acronym must be add, if it exists, this way: 'Organism Name(Acronym)'
            7. Write one or two continuous paragraphs, without bullet points or lists.
            8. Use {text_reference} as stylistic reference.
            9. When citing the number of base pairs or nucleotides, say it is an "approximate" number.
            
            Your goal is to produce a concise, coherent, and professional clinical report that reflects confirmed scientific knowledge — **the absence of information (if any remaining) must be rendered invisible to the reader.**
            """
