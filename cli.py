import typer
import simplemind as sm
from docx_reader import read_docx_to_string
from download_docx import download_and_read_docx
from config import cli_config


def init_conversation():

    conv = sm.create_conversation(
                llm_model=cli_config.LLM_NAME,
                llm_provider=cli_config.LLM_PROVIDER
            )
    # cv_string = download_and_read_docx(cli_config.S3_BUCKET, cli_config.S3_KEY)
    # conv.add_message(
    #         "user", 
    #         f"Here is the resume from a colleague: {cv_string}." \
    #         "Can you read it and then I'll ask you some questions about it." \
    #         "Once you have fully ingested the resume, just reply: " \
    #         "'I am ready to discuss the life and achievements of <name_of_the_resume_author>.'")

    return conv

app = typer.Typer()


@app.command()
def import_resume():
    conv = init_conversation()
    cv_string = download_and_read_docx(cli_config.S3_BUCKET, cli_config.S3_KEY)
    conv.add_message(
            "user", 
            f"Here is the resume from a colleague: {cv_string}." \
            "Can you read it and then I'll ask you some questions about it." \
            "Once you have fully ingested the resume, just reply: " \
            "'I am ready to discuss the life and achievements of <name_of_the_resume_author>.'")
    response = conv.send()
    print(response.text)
    return conv


@app.command()
def ask_question(question: str):
    conv.add_message("user", question)
    response = conv.send()
    print(response.text)


if __name__ == "__main__":
    # conv = init_conversation()
    conv = import_resume()
    app()
