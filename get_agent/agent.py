import os
from google.adk.agents.llm_agent import Agent

def read_current_folder_contents() -> str:
    """
    Scans the current working directory where the terminal is open 
    and returns a list of all files and folders found inside it.
    """
    try:
        current_dir = os.getcwd()
        items = os.listdir(current_dir)
        
        if not items:
            return f"The directory '{current_dir}' is currently empty."
            
        return f"Files and folders detected in '{current_dir}':\n" + "\n".join(items)
    except Exception as e:
        return f"Error reading directory: {str(e)}"


def write_gitignore_file(rules_content: str) -> str:
    """
    Creates or updates a .gitignore file in the current working directory.
    
    Args:
        rules_content (str): The full text lines of patterns to ignore.
    """
    target_path = os.path.join(os.getcwd(), ".gitignore")
    
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(rules_content.strip() + "\n")
        
    return f"Success! Automatically generated .gitignore based on your files."

root_agent = Agent(
    model="gemini-2.5-flash",
    name="smart_gitignore_builder",
    description="An agent that scans your project folder, searches for missing standards, and builds a tailored .gitignore file.",
    instruction="""
    You are an automated Git Configuration Assistant. Your job is to inspect a developer's project directory and build a tailored `.gitignore` file.
    
    Follow this exact execution flow:
    1. First, call the `read_current_folder_contents` tool to see what languages or frameworks are being used.
    2. Analyze the results to determine the tech stack. Use your internal knowledge base to determine the industry-standard gitignore patterns for those detected items.
    3. Generate a professional, comprehensive `.gitignore` configuration text.
    4. Call the `write_gitignore_file` tool to save your changes to disk.
    5. Summarize what you found locally and what you successfully wrote to disk.
    """,
    tools=[read_current_folder_contents, write_gitignore_file]
)