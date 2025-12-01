import argparse
from assistant import MetagenomicsAssistant
from aws_handler import AwsHandler
from utils import farwell_to_user

def parse_arguments():
    """
    Simple argument parser for TaxID or organism name input
    """
    parser = argparse.ArgumentParser(
        description='Generate clinical record from TaxID or organism name.'
    )
    parser.add_argument(
        '-tx', '--taxid', 
        help='Enter a valid TaxID to generate the clinical record'
    )
    parser.add_argument(
        '-n', '--organism_name', 
        help='Enter a valid organism name to generate the clinical report'
    )
    # parser.add_argument(
    #     '-md', '--model',
    #     help='Enter a valid model name to use.'         <-- comming soon
    # ) 
    parser.add_argument(
        '-ptbr', '--portuguese',
        action='store_true',
        help="Text It's going to be generated in brazilian portuguese. If not provided, text It's going to be generated in brazilian portuguese (default)"
    )
    parser.add_argument(
        '-eng', '--english',
        action='store_true',
        help="Text It's going to be generated in english. If not provided, text It's going to be generated in brazilian portuguese (default)"
    )
    
    args = parser.parse_args()
    
    # Validate that exactly one argument is provided
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
    
    # Initialize the assistant
    assistant = MetagenomicsAssistant(aws_handler=AwsHandler())
    
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
                print(f"Error: Could not find TaxID for organism '{organism_name}'\nPlease, enter a valid name or TaxID")
                return
            
            print(f"Found TaxID: {tax_id}")
        
        # Generate the clinical record
        if not args.english or args.portuguese:
            text_language = 'Brazilian Portuguese'
        elif args.english:
            text_language =  'English'
        else:
            text_language = 'Brazilian Portuguese'
        
        final_text = assistant.invoke_bedrock_model(tax_id, text_language)
        print(f'\nYour clinical record:\n\n{final_text}\n')
        farwell_to_user()
        
    except Exception as e:
        print(f"An error occurred: {e}")