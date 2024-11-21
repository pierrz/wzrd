import typer
import simplemind as sm
import json
import os
from download_docx import download_and_read_docx
from config import cli_config
from enums import ConversationState, ConversationActor


def load_state():
    if os.path.exists(cli_config.STATE_FILE):
        with open(cli_config.STATE_FILE, 'r') as f:
            return json.load(f)
    # else:
    print("No state file found. Creating a new one.")
    return {ConversationState.resume_imported: False, ConversationState.messages: []}

def update_state(state):
    with open(cli_config.STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def get_conversation():
    state = load_state()
    conv = sm.create_conversation(
        llm_model=cli_config.LLM_NAME,
        llm_provider=cli_config.LLM_PROVIDER
    )
    
    # Restore previous messages if any
    for msg in state.get(ConversationState.messages, []):
        conv.add_message(msg[ConversationState.role], msg[ConversationState.content])
    
    return conv, state

app = typer.Typer()

@app.command()
def import_resume():
    conv, state = get_conversation()
    
    if not state[ConversationState.resume_imported]:
        cv_string = download_and_read_docx(cli_config.DATA_BUCKET, cli_config.DATA_SOURCE_KEY)
        message = (
            f"Here is the resume from a colleague: {cv_string}." \
            "Read it and then I'll ask you some question about it." \
            "Once you have fully ingested the resume, reply only :" \
            "'Ask me anything about <name_of_the_resume_author>'."
        )
        conv.add_message(ConversationActor.user.value, message)
        state[ConversationState.messages].append({ConversationState.role: ConversationActor.user, ConversationState.content: message})
        state[ConversationState.resume_imported] = True
        update_state(state)
    
    response = conv.send()
    state[ConversationState.messages].append({ConversationState.role: ConversationActor.assistant, ConversationState.content: response.text})
    update_state(state)
    print(response.text)

@app.command()
def ask_question(question: str):
    conv, state = get_conversation()
    
    if not state[ConversationState.resume_imported]:
        print("Please run 'import-resume' first to load the resume.")
        return
    
    conv.add_message(ConversationActor.user.value, question)
    state[ConversationState.messages].append({ConversationState.role: ConversationActor.user, ConversationState.content: question})
    response = conv.send()
    state[ConversationState.messages].append({ConversationState.role: ConversationActor.assistant, ConversationState.content: response.text})
    update_state(state)
    print(response.text)

@app.command()
def reset():
    """Reset the conversation state"""
    if os.path.exists(cli_config.STATE_FILE):
        os.remove(cli_config.STATE_FILE)
    print("Conversation state has been reset.")

if __name__ == "__main__":
    app()
