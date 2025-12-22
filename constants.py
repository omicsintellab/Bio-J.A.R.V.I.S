# constants.py

# AWS Bedrock Model IDs
MODEL_ID_1 = "amazon.nova-micro-v1:0"  # Amazon Nova Micro
MODEL_ID_2 = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"  # Example OpenAI-style
MODEL_ID_3 = "anthropic.claude-3-5-sonnet-20241022-v2:0"  # Claude
MODEL_ID_4 = "google.gemma-2-2b-it-v1:0"  # Gemma

# NCBI Entrez email
DEFAULT_EMAIL = "your.email@example.com"  # Change to your email

# File paths
DATA_DIR = "./files"
OLD_REPORTS_FILE = "old_reports.csv"
BIOJARVIS_DATA_FILE = "data_for_biojarvis.csv"
ACRONYMS_FILE = "acronyms.csv"

# Default parameters
DEFAULT_MAX_TOKENS = 500
DEFAULT_TEMPERATURE = 0.1
DEFAULT_TOP_P = 0.1