from pathlib import Path

# Get the current directory where prompts.py is located
current_dir = Path(__file__).parent

def get_board_of_directors_prompt(n):
    file_path = current_dir / f"board_of_directors_prompt{n}.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        return ''.join(file.readlines())
    
def get_top_shareholders_prompt(n):
    file_path = current_dir / f"top_shareholders_prompt{n}.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        return ''.join(file.readlines())