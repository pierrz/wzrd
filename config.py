from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LLM_PROVIDER: str = "anthropic"
    LLM_NAME: str = "claude-3-5-sonnet-20241022"
    S3_BUCKET: str
    S3_KEY: str
    ANTHROPIC_API_KEY: str
    OPENAI_API_KEY: str
    STATE_FILE: str = "conversation_state.json"

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

cli_config = Settings()
