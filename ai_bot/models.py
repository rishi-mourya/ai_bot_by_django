# import Django base model class
from django.db import models


# this table represents a single chat session (like one conversation in ChatGPT)
class Conversation(models.Model):

    # title shown in sidebar (first user message usually)
    title = models.CharField(max_length=255)

    # timestamp when conversation was created
    created_at = models.DateTimeField(auto_now_add=True)

    # readable name in Django admin
    def __str__(self):
        return self.title


# this table stores every message inside a conversation
class Message(models.Model):

    # link message to conversation (one conversation can have many messages)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    # user message
    user_message = models.TextField()

    # AI response
    bot_response = models.TextField()

    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_message[:50]