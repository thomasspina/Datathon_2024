from src.models import bedrock_agent

def create_financial_report(symbol, stats): 
    prompt = f"""1 - Provide a 3 line summary with important information about the company : {symbol}.
        2 - next i would like you to lightly comment on this data and include the quality of the stock with usiing Chiffre d'affaires, marge brute, flux de trésorerie libre, dette nette, bénéfice (avant intérêts,
        impôts, dépréciations et amortissements), bénéfice par action found in these stats : 
        {stats}"""
    
    response = bedrock_agent.ask_claude(
            prompt
            )
    
    file_name = f"Report_{symbol}.txt"
    with open(file_name, "w") as text_file:
        print(prompt, file=text_file)
        print(response, file=text_file)

    return response, file_name