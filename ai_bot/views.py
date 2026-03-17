from django.shortcuts import render, redirect
from .models import Conversation, Message
import ollama


def chatBot(request):

    chat_id = request.GET.get("chat")
    new_chat = request.GET.get("new")
    delete_chat = request.GET.get("delete")

    # delete chat
    if delete_chat:
        Conversation.objects.filter(id=delete_chat).delete()
        return redirect("/")

    conversation = None
    messages = []

    # sidebar history
    conversations = Conversation.objects.all().order_by("-created_at")

    # NEW CHAT LOGIC
    if new_chat:

        last_chat = Conversation.objects.order_by("-created_at").first()

        if last_chat:
            has_messages = Message.objects.filter(conversation=last_chat).exists()

            # reuse if empty
            if not has_messages:
                return redirect(f"/?chat={last_chat.id}")

        # otherwise create new
        conversation = Conversation.objects.create(title="New Chat")
        return redirect(f"/?chat={conversation.id}")

    # load conversation
    if chat_id:
        try:
            conversation = Conversation.objects.get(id=chat_id)
            messages = Message.objects.filter(conversation=conversation).order_by("created_at")
        except Conversation.DoesNotExist:
            conversation = None

    # send message
    if request.method == "POST":

        user_message = request.POST.get("message")

        if user_message and user_message.strip():

            # create chat if none selected
            if not conversation:
                conversation = Conversation.objects.create(
                    title=user_message[:30]
                )
            else:
                # update title if still "New Chat"
                if conversation.title == "New Chat":
                    conversation.title = user_message[:30]
                    conversation.save()

            response = ollama.chat(
                model="llama3",
                messages=[{"role": "user", "content": user_message}]
            )

            bot_response = response["message"]["content"]

            Message.objects.create(
                conversation=conversation,
                user_message=user_message,
                bot_response=bot_response
            )

            return redirect(f"/?chat={conversation.id}")

    return render(
        request,
        "index.html",
        {
            "messages": messages,
            "conversations": conversations,
            "current_conversation": conversation
        }
    )