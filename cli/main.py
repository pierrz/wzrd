import os
from pathlib import Path

import typer
from config import cli_config
from download_docx import (
    import_docx_from_local_file,
    import_docx_from_s3,
    prepare_string_from_docx,
)
from enums import ConversationActor, ConversationState
from utils import (
    get_conversation,
    get_init_response,
    prepare_init_message,
    update_state,
)

app = typer.Typer()


@app.command()
def import_resume():
    """Import a resume from a S3 bucket, based on .env parameters"""
    conv, state = get_conversation()

    if not state[ConversationState.resume_imported]:
        document = import_docx_from_s3(
            cli_config.DATA_BUCKET, cli_config.DATA_SOURCE_KEY
        )
        cv_string = prepare_string_from_docx(document)
        prepare_init_message(conv, state, cv_string)

    get_init_response(conv, state)


@app.command()
def import_local_resume(filepath: str):
    """Import a resume from a local file"""
    conv, state = get_conversation()

    if not state[ConversationState.resume_imported]:
        document = import_docx_from_local_file(filepath)
        cv_string = prepare_string_from_docx(document)
        prepare_init_message(conv, state, cv_string)

    get_init_response(conv, state)


@app.command()
def ask_question(question: str):
    """Ask a question about the resume"""
    conv, state = get_conversation()

    if not state[ConversationState.resume_imported]:
        print("Please run 'import-resume' first to load the resume.")
        return

    conv.add_message(ConversationActor.user.value, question)
    state[ConversationState.messages].append(
        {
            ConversationState.role: ConversationActor.user,
            ConversationState.content: question,
        }
    )
    response = conv.send()
    state[ConversationState.messages].append(
        {
            ConversationState.role: ConversationActor.assistant,
            ConversationState.content: response.text,
        }
    )
    update_state(state)
    print(response.text)


@app.command()
def reset():
    """Reset the conversation state"""
    if Path(cli_config.STATE_FILE).exists():
        os.remove(cli_config.STATE_FILE)
    print("Conversation state has been reset.")


if __name__ == "__main__":
    app()
