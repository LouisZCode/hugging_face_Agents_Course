"agent that tells me the time"

#import necessary libraries:
import datetime
import os
#already installed, no worries
import anthropic
#we need this to read the system prompt in prompts.yaml
import yaml

#without this, the .env files would not be charged here:
from dotenv import load_dotenv
load_dotenv()

#get the api key (or ask of one if not in .env)
if not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = input("please insert your Anthropic API key")

#setup the Anthropic client
client = anthropic.Anthropic()
#select the model to use: https://docs.anthropic.com/en/docs/about-claude/models
#I chose the cheapest first for testing:
haiku = "claude-3-haiku-20240307"


#we create the tool here:
#@Tool
def get_current_time_in_timezone(timezone: str) -> str:
#Indentation os also important here! the """ need to be in line...
    """Get the current time in the specified timezone.
    Args:
        timezone: The timezone name as a string (e.g., 'UTC', 'America/New_York', 'Europe/London')
    Returns:
        str: The current time formatted as a string in the specified timezone
    """
    try:
        local_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"
    

#we create a timezone_expert agent:   the template is here: https://docs.anthropic.com/en/docs/initial-setup

#We need to be able to read the xaml file and make it the system prompt:
with open("C:/Users/Admin/Desktop/Python Learning/AI_Agent_projects/Claude_Agent_1/prompts.yaml", 'r') as stream:    prompt_templates = yaml.safe_load(stream)
message = client.messages.create(
    model=haiku,
    max_tokens=100, #the quantity to respond tops. this case, needs little tokens
    temperature=0.1, #lower is more deterministic, higher is more "creative"
    #this is the system prompt: added to a new file prompts.py

    #also, be sure to not pass the whole yaml
    system=prompt_templates["system_prompt"],
    #the history of the chat, all discussed will be appended here, 
    # and read every time the agent wants to answer
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Why is the ocean salty?"
                }
            ]
        }
    ]
)
print(message.content)
