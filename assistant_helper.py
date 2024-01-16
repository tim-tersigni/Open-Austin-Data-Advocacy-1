from openai import OpenAI
from dotenv import load_dotenv
import sys
import time

def start_run_on_thread(client, thread_id, assistant_id):
    """
    Starts a run on the given thread and returns the messages list

    :param client: OpenAI() client instance
    :param thread_id:
    :param assistant_id:
    """
    # Start a run on the thread
    run = client.beta.threads.runs.create(
      thread_id=thread_id,
      assistant_id=assistant_id
    )

    i = 0
    indicator = ['⠟','⠯','⠷','⠾','⠽','⠻']

    # Wait for the run to complete with an animated loading indicator
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        cur_indicator = indicator[i % 6]
        sys.stdout.write("\rAssistant Working" + cur_indicator + " ")
        sys.stdout.flush()
        i += 1

    # Clear the loading message
    sys.stdout.write("\rCompleted!          \n")
    sys.stdout.flush()

    # Retrieve and return messages
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    
    return messages

def create_openai_assistant(file_path, assistant_name, instructions):
    """
    Creates an OpenAI assistant using a specified file.

    :param file_path: Path to the file to be used with the assistant.
    :param assistant_name: Name for the assistant.
    :param instructions: Instructions for the assistant's behavior.
    :return: An instance of the OpenAI assistant.
    """
    # Load environment variables
    load_dotenv()

    # Initialize the OpenAI client
    client = OpenAI()

    # Upload the file
    with open(file_path, "rb") as file:
        uploaded_file = client.files.create(file=file, purpose='assistants')

    # Create the assistant
    assistant = client.beta.assistants.create(
        name=assistant_name,
        instructions=instructions,
        tools=[{"type": "code_interpreter"}],
        model="gpt-4-1106-preview",
        file_ids=[uploaded_file.id]
    )

    return assistant
