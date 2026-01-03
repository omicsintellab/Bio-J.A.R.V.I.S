import os
import json
from pathlib import Path

ENV_PATH = Path(".env")


def write_env_var(key: str, value: str):
    """
    Create or update a variable inside .env file.
    If .env does not exist, it will be created.
    """
    env_vars = {}

    if ENV_PATH.exists():
        with ENV_PATH.open("r") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.strip().split("=", 1)
                    env_vars[k] = v

    env_vars[key] = value

    with ENV_PATH.open("w") as f:
        for k, v in env_vars.items():
            f.write(f"{k}={v}\n")

def is_null(value):  
    """
    Validate if value is null or not.
    """   
    return value in [None, '', [], {}]

def save_output(output_path, tax_id, content, file_type="json"):
    file_type = file_type.lower().lstrip(".")

    directory = os.path.dirname(output_path)
    archive_name = os.path.basename(output_path)

    if directory:
        os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, f"{archive_name}.{file_type}") if directory else f"{archive_name}.{file_type}"

    if file_type == "json":
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = {}
        else:
            existing_data = {}

        existing_data[str(tax_id)] = content

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)

    elif file_type == "txt":
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"{tax_id}: {content}\n")

    else:
        raise ValueError("Unsupported file type. Use 'json' or 'txt'.")


def set_prompt_text(information_dict, text_reference, language):
    """
    Prompt for IA.
    """
    prompt_text = (
           f"""
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
        )
    return prompt_text

def farwell_to_user():
    print('''
    ████████╗██╗  ██╗ █████╗ ███╗   ██╗██╗  ██╗    ██╗   ██╗ ██████╗ ██╗   ██╗
    ╚══██╔══╝██║  ██║██╔══██╗████╗  ██║██║ ██╔╝    ╚██╗ ██╔╝██╔═══██╗██║   ██║
       ██║   ███████║███████║██╔██╗ ██║█████╔╝      ╚████╔╝ ██║   ██║██║   ██║
       ██║   ██╔══██║██╔══██║██║╚██╗██║██╔═██╗       ╚██╔╝  ██║   ██║██║   ██║
       ██║   ██║  ██║██║  ██║██║ ╚████║██║  ██╗       ██║   ╚██████╔╝╚██████╔╝
       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ 
                                                                               
    ╔═══════════════════════════════════════════════════════════════════╗
                    🧪 THANK YOU FOR USING BIO-J.A.R.V.I.S! 🧪              
                      🔬 See you in the next discovery! 🔬              
    ╚═══════════════════════════════════════════════════════════════════╝
    ''')
