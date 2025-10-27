import pandas as pd 
import os
from claude_llm import claude_llm

def check_curation(gene, dox_claim,drug_abbr, drug_full_name):

    print(f"Checking gene: {gene}, drug: {drug_abbr}")
    

    drug_names=[drug_abbr, drug_full_name]
    prompt = f"""You are an expert in biomedical literature analysis, specializing in gene-drug interactions and drug resistance mechanisms.

    Analyze the following sentence from scientific literature: "{dox_claim}"

    Perform three independent checks:

    1. **Gene Presence**: Determine if the gene '{gene}' (or its standard symbols/aliases) is explicitly mentioned in the sentence. Respond with YES if present, NO otherwise. Consider only direct mentions; do not infer from context.

    2. **Drug Presence**: Determine if any of the drug names {drug_names} (or their standard abbreviations/aliases) are explicitly mentioned in the sentence. Respond with YES if at least one is present, NO otherwise. Consider only direct mentions; do not infer from context.

    3. **Resistance Claim**: Determine if the sentence claims that the gene '{gene}' is involved in drug resistance to the mentioned drug(s). Base this strictly on the following evidence criteria for a YES response (all must align with resistance, not sensitivity):
    - Overexpression, activation, or upregulation of '{gene}' leads to or is associated with drug resistance.
    - Silencing, downregulation, knockout, or loss-of-function of '{gene}' leads to or is associated with drug sensitivity (implying '{gene}' promotes resistance).
    - Pharmacological inhibition of '{gene}' (using a specific inhibitor targeting the gene product) leads to drug sensitivity (implying '{gene}' promotes resistance).
    - Ectopic/artificial overexpression of '{gene}' leads to drug resistance.

    Respond with YES only if the sentence provides direct evidence matching one or more of these criteria for resistance involvement. Respond with NO if:
    - The claim is about sensitivity without implying resistance.
    - There is upregulation of '{gene}' solely in response to drug treatment (e.g., adaptive response), as this does not prove causal involvement in resistance.
    - The sentence discusses unrelated mechanisms, correlations without causation, or opposite effects.

    Think step-by-step for the resistance claim, but keep your reasoning concise (1-2 sentences max).

    Output your response in this exact JSON format, with no additional text:
    {{
        "gene_present": "YES" or "NO",
        "drug_present": "YES" or "NO",
        "resistance_claim": "YES" or "NO"
    }}
    """

    response = claude_llm(prompt)
    print(response)
    return (response['gene_present'], response['drug_present'], response['resistance_claim'])





df = pd.read_excel("October_55_Protein_Formatted_NEW.xlsx")

df[["gene_present", "drug_present", "resistance_claim"]] = df.apply(
                                                            lambda x: check_curation(
                                                                x["Official Gene Name"], 
                                                                x["Exact line claiming drug resistance"],
                                                                x["Drug"],
                                                                x["Drug Full Name"],
                                                            ), 
                                                            axis=1, 
                                                            result_type="expand"
                                                        )


df.to_excel("curation_check_result.xlsx", index=False)


