from Bio import Entrez

# ID from AWS MODEL: Amazon Nova Micro
MODEL_ID_1='amazon.nova-micro-v1:0'
# MODEL_ID_2='openai.gpt-oss-120b-1:0'                             <-- comming soon
# MODEL_ID_3='anthropic.claude-sonnet-4-5-20250929-v1:0'

# Default e-mail to access NCBI with biopython
DEFAULT_EMAIL= Entrez.email = 'email@email.com'
