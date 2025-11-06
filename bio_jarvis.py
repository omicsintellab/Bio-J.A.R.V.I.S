from assistant import MetagenomicsAssistant
from aws_handler import AwsHandler
from utils import get_integer_tax_id, greetings_to_user, farwell_to_user
import json

if __name__ == '__main__':
    bio_jarvis = MetagenomicsAssistant(aws_handler=AwsHandler())
    greetings_to_user()
    user_tax_id = get_integer_tax_id('Enter the Organism TaxID: ')
    organism_info =  bio_jarvis.set_organism_fields(user_tax_id)
    final_text = bio_jarvis.invoke_bedrock_model(user_tax_id)
    print(f'{final_text}\n{farwell_to_user()}')