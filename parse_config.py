# parse_config.py

import argparse
from typing import Optional
from assistant import MetagenomicsAssistant
from aws_handler import AwsHandler
from utils import farwell_to_user, save_output


# ------------------------------------------------------------------
# Argument parsing
# ------------------------------------------------------------------

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a clinical report from a TaxID or organism name."
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "-tx", "--taxid",
        help="NCBI TaxID of the organism"
    )
    input_group.add_argument(
        "-n", "--organism-name",
        dest="organism_name",
        help="Scientific name of the organism"
    )

    parser.add_argument(
        "-m", "--model",
        choices=["amazon", "openai", "claude", "gemma"],
        default="amazon",
        help="LLM model to be used (default: amazon)"
    )

    parser.add_argument(
        "-l", "--language",
        choices=["english", "portuguese"],
        default="english",
        help="Output language (default: english)"
    )

    parser.add_argument(
        "-o", "--output",
        help="Directory path to save the output file"
    )

    parser.add_argument(
        "-f", "--format",
        choices=["json", "txt"],
        default="json",
        help="Output file format (default: json)"
    )

    return parser.parse_args()


# ------------------------------------------------------------------
# Main handler
# ------------------------------------------------------------------

def run_cli() -> None:
    args = parse_arguments()

    assistant = MetagenomicsAssistant(aws_handler=AwsHandler())

    try:
        tax_id: Optional[str]

        if args.taxid:
            tax_id = args.taxid
            print(f"▶ Generating report for TaxID: {tax_id}")
        else:
            print(f"▶ Resolving TaxID for organism: {args.organism_name}")
            tax_id = assistant.get_organism_tax_id(args.organism_name)

            if not tax_id:
                raise ValueError(
                    f"Could not resolve TaxID for organism '{args.organism_name}'"
                )

            print(f"✔ Found TaxID: {tax_id}")

        # ------------------------------------------------------------------
        # Model dispatch
        # ------------------------------------------------------------------

        model_dispatch = {
            "amazon": assistant.generate_with_nova,
            "openai": assistant.generate_with_openai,
            "claude": assistant.generate_with_claude,
            "gemma": assistant.generate_with_gemma,
        }

        generate_fn = model_dispatch[args.model]
        final_text = generate_fn(tax_id=int(tax_id), language=args.language)

        # ------------------------------------------------------------------
        # Output
        # ------------------------------------------------------------------

        if args.output:
            save_output(
                output_path=args.output,
                tax_id=tax_id,
                content=final_text,
                file_format=args.format,
            )

        print("\n📄 Generated clinical report:\n")
        print(final_text)
        farwell_to_user()

    except Exception as exc:
        print(f"\n❌ Error: {exc}\n")