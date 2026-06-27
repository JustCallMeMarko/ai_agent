# Introduction
When you're making any project and use git, we usually want to stage things fast so we usually do `git add .` which stages all files and folders, this is where `.gitignore` file comes in. 

#### What is the .gitignore file?
The .gitignore file makes you ignore files when you stage files. This helps you keep track of versions correctly and avoid tracking temporary cache files or sensitive data. Making .gitignore file from scratch is very hard for beginners unless they use a template, so thats why in this Tutorial we are going to make an agent that automates all of this.

#### What is an agent 
An agent is an AI that can observe a task, decide what to do next, and take actions to reach a goal. In this project, the agent will help generate a `.gitignore` file based on the files and tools used in your project.

# Creating the smart_gitignore_builder Agent
## 01 What you need to install

Before building the agent, install these packages:

```bash
pip install google-adk python-dotenv
```

`google-adk` helps you build the agent, and `python-dotenv` helps you manage environment variables safely.

## 02 Using the ADK

After installing the packages, create your agent by running the following command:

```bash
adk create git_agent
```
after that choose the following option when prompted
```bash
Choose a model for the root agent:
1. gemini-3.5-flash
2. Other models (fill later)
Choose model (1, 2): 1
1. Google AI
2. Vertex AI
3. Login with Google
Choose a backend (1, 2, 3): 1
```
after picking google ai you need to make an api key in googles ai studio and enter it

```bash
Enter Google API key: enter_your_key_here
```

## 03 Customizing our agent

When you initialized the agent, the ADK generated a basic template. But right now, our agent is basically a normal chatbot without tools. 

To turn it into a smart gitignore helper, we are going to make **two custom Python tools** and attach them to the `Agent` configuration.

Open `agent.py` and add the following code:

First, we need a tool that lets the agent inspect your active workspace. We'll use Python’s native `os` module to read the Current Working Directory (`os.getcwd()`). 

```python
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
```

In the code above we just made a tool named read_current_folder_contents that reads all files and folders inside the directory you ran the agent. Notice how theres a docstring it is there to guide our agent config on what our tool does.

```Python
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
```

The write_gitignore_file tool expects a paramater of rules_content where it lays down the rules line by line 

Now time to setup our agent config
1. model is the ai model you picked earlier and if you want to change it to another ai model then you can do so
2. name is basically the name of the agent
3. description is just the brief overview of what the agent does
4. instruction is the blueprint for your agent. It is the agents persona, rules, and boundaries that you give it to
5. tools are the literal hands or capabilities you give your agent
```Python 

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
```

## 04 Running our agent

The best part about using the Google ADK is that your agent isn't locked inside its directory. You can run it across any development folder on your computer.

### How to execute the run command
When using the `adk run` command, the CLI expects a **directory path**. It will look inside that folder and find your `agent.py` file automatically.

Open up your preferred terminal (PowerShell, Command Prompt, or Git Bash), navigate to your development folder where you want to create your `.gitignore`:

```bash
# 1. Navigate to your target development project folder or basically run a terminal on that directory
cd C:\Users\yourusername\Desktop\my-active-project

# 2. Execute adk run pointing to your agent's root folder directory
adk run "C:\Users\yourusername\your_path_folder_to_coding_agent"
```

Once it loads you can talk to the agent and create a gitignore

# Make It Your Own
Now that you understand how to give an agent hands, you can take this layout and build something completely different! 

Challenge yourself to take things further!

# Wrapping Up

Congrats! You created an ai agent that does gitignore file for you. Even though theres some gitignore templates out there in the internet, this just makes it customized to your project if you have a niche stack.