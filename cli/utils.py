import json
from pathlib import Path

import simplemind as sm
from config import cli_config
from enums import ConversationActor, ConversationState


def load_state():
    if Path(cli_config.STATE_FILE).exists():
        with open(cli_config.STATE_FILE, "r") as f:
            return json.load(f)
    print("No state file found. Creating a new one.")
    return {
        ConversationState.resume_imported: False,
        ConversationState.messages: [],
    }


def update_state(state):
    with open(cli_config.STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def get_conversation():
    state = load_state()
    conv = sm.create_conversation(
        llm_model=cli_config.LLM_NAME, llm_provider=cli_config.LLM_PROVIDER
    )

    # Restore previous messages if any
    for msg in state.get(ConversationState.messages, []):
        conv.add_message(
            msg[ConversationState.role], msg[ConversationState.content]
        )

    return conv, state


def prepare_init_message(conv, state, cv_string):
    message = (
        f"Here is the resume from a colleague: {cv_string}."
        "Read it and then I'll ask you some question about it."
        "Once you have fully ingested the resume, reply only :"
        "'Ask me anything about <name_of_the_resume_author>'."
    )
    conv.add_message(ConversationActor.user.value, message)
    state[ConversationState.messages].append(
        {
            ConversationState.role: ConversationActor.user,
            ConversationState.content: message,
        }
    )
    state[ConversationState.resume_imported] = True
    update_state(state)


def get_init_response(conv, state):
    response = conv.send()
    state[ConversationState.messages].append(
        {
            ConversationState.role: ConversationActor.assistant,
            ConversationState.content: response.text,
        }
    )
    update_state(state)
    print(response.text)
