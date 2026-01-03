import argparse
import os
from assistant import MetagenomicsAssistant
from aws_handler import AwsHandler
from gemini_handler import GeminiHandler
from utils import farwell_to_user, save_output, write_env_var


def parse_arguments():
    """
    Simple argument parser for TaxID or organism name input
    """
    parser = argparse.ArgumentParser(
        description="Generate clinical record from TaxID or organism name."
    )
    parser.add_argument(
        "-tx", "--taxid", help="Enter a valid TaxID to generate the clinical record"
    )
    parser.add_argument(
        "-n",
        "--organism_name",
        help="Enter a valid organism name to generate the clinical report",
    )
    parser.add_argument("-out", "--output", help="Enter a valid path to save text.")
    parser.add_argument(
        "-f",
        "--format",
        choices=["json", "txt"],
        default="json",
        help="Output file format (json or txt). Default is json.",
    )
    parser.add_argument(
        "-l",
        "--language",
        choices=["EN", "PT"],
        default="EN",
        help="Language for the generated report (EN=English, PT=Brazilian Portuguese). Default is EN.",
    )
    parser.add_argument(
        "-key", "--api-key", help="API Key for the chosen provider (saved to .env)"
    )
    parser.add_argument(
        "-p",
        "--provider",
        choices=["aws", "gemini"],
        default="aws",
        help="LLM provider to use (default: aws)",
    )

    parser.add_argument(
        "--update-db",
        action="store_true",
        help="Update the local NCBI taxonomy database",
    )

    args = parser.parse_args()

    # Check for update-db first
    if args.update_db:
        return args

    # Validate that exactly one argument is provided (if not updating db)
    if not args.taxid and not args.organism_name:
        parser.error("You must provide either --taxid or --organism_name")

    if args.taxid and args.organism_name:
        parser.error("Please provide only one of --taxid or --organism_name, not both")

    return args


def parse_handle():
    """
    Function to handle command line execution
    """
    # Parse command line arguments
    args = parse_arguments()

    if args.api_key:
        if args.provider == "gemini":
            write_env_var("GEMINI_API_KEY", args.api_key)
        else:
            write_env_var("AWS_BEARER_TOKEN_BEDROCK", args.api_key)

    # Instantiate handler based on provider
    if args.provider == "gemini":
        handler = GeminiHandler()
    else:
        handler = AwsHandler()

    # Initialize the assistant
    assistant = MetagenomicsAssistant(llm_handler=handler)

    if args.update_db:
        print("Updating NCBI taxonomy database. This might take a few minutes...")
        assistant.ncbi.update_taxonomy_database()
        print("Database updated successfully!")
        return

    try:
        # Determine input type and process
        if args.taxid:
            tax_id = args.taxid
            print(f"Generating clinical record for TaxID: {tax_id}")
        else:  # args.organism_name
            organism_name = args.organism_name
            print(f"Generating clinical record for organism: {organism_name}")
            tax_id = assistant.get_organism_tax_id(organism_name)

            if not tax_id:
                print(
                    f"Error: Could not find TaxID for organism '{organism_name}'\nPlease, enter a valid name or TaxID"
                )
                return

            print(f"Found TaxID: {tax_id}")

        if args.language == "PT":
            text_language = "Brazilian Portuguese"
        else:
            text_language = "English"

        # Generate the clinical record
        final_text = assistant.generate_report(tax_id, text_language)

        if args.output:
            save_output(args.output, tax_id, final_text, args.format)

        print(f"\nYour clinical record:\n\n{final_text}\n")
        farwell_to_user()

    except Exception as e:
        print(f"An error occurred: {e}")
