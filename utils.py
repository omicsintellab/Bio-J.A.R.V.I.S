from enum import Enum

def is_null(value):  
    """
    Validate if value is null or not.
    """   
    return value in [None, '', [], {}]

def set_prompt_text(information_dict, text_reference):
    """
    Prompt for IA.
    """
    prompt_text = (
           f"""
            You are an assistant specialized in clinical and microbiological reports about pathogens in clinical metagenomics.
            Your task is to write a test report in Brazilian Portuguese, in the formal and objective tone of medical literature.
            
            **Data Sourcing Strategy:**
            1. **Primary Source:** The structured data: {information_dict} must be used first.
            2. **Final Source Data:** The report must integrate the information from the primary source and, if found, the validated information from the secondary search.

            **Report Rules (Strictly Enforced):**
            1. Include only the information explicitly provided in the combined data source (Primary) or scientifically validated as general knowledge (e.g., taxonomic hierarchy).
            2. **STRICTLY PROHIBITED:** Never mention, imply, or discuss missing information. **Omit any topic for which specific, explicit data is not available **even after the secondary search.**
            3. **ABSOLUTE PROHIBITION ON NEGATION AND UNCERTAINTY:**
                * **NEVER** write phrases like "informação não está disponível," "desconhecido," "não há dados," "pesquisa adicional é necessária," "embora não existam dados," "pode causar," **or any phrasing that suggests the data was searched for and not found.**
                * **DO NOT** comment on the research process or the completeness of the data.
                * **DO NOT** use title.
            4. If data is still missing after the secondary search (e.g., disease, host, or transmission), **do not write about those topics at all; simply omit the topic entirely.**
            5. Do not infer, speculate, or generalize from related taxa, families, or genera.
                * For example, do not assume properties or pathogenicity based on taxonomic similarity.
            6. The text must be strictly factual, affirmative, and **free of any uncertainty or discussion about data availability.
                * The Acronym must be add, if it exists, this way: 'Organism Name(Acronym)'
            7. Write one or two continuous paragraphs, without bullet points or lists.
            8. Use {text_reference} as stylistic reference.
            
            Your goal is to produce a concise, coherent, and professional clinical report that reflects only the confirmed and explicit knowledge available — **the absence of information must be rendered invisible to the reader.**
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
