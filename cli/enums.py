"""
Module dedicated to all Enum objects
"""

from enum import Enum


class ValueEnum(str, Enum):
    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value == value:
                return member
        return super()._missing_(value)


class ConversationState(ValueEnum):
    resume_imported = "resume_imported"
    messages = "messages"
    role = "role"
    content = "content"


class ConversationActor(ValueEnum):
    user: str = "user"
    assistant: str = "assistant"
