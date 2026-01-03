import os
import json
from pathlib import Path

from pathlib import Path
from constants import PROMPT_TEMPLATE

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


def is_null(value: any) -> bool:
    """
    Validate if value is null or not.
    """
    return value in [None, "", [], {}]


def save_output(
    output_path: str, tax_id: str | int, content: str, file_type: str = "json"
) -> None:
    file_type = file_type.lower().lstrip(".")

    directory = os.path.dirname(output_path)
    archive_name = os.path.basename(output_path)

    if directory:
        os.makedirs(directory, exist_ok=True)

    file_path = (
        os.path.join(directory, f"{archive_name}.{file_type}")
        if directory
        else f"{archive_name}.{file_type}"
    )

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


def set_prompt_text(
    information_dict: dict, text_reference: list[str], language: str
) -> str:
    """
    Prompt for IA.
    """
    prompt_text = PROMPT_TEMPLATE.format(
        language=language,
        information_dict=information_dict,
        text_reference=text_reference,
    )
    return prompt_text


def farwell_to_user():
    print(
        """
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
    """
    )
