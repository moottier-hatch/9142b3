from django.contrib.auth.middleware import get_user
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from django.db.models import Q
from messenger_backend.models import Conversation, Message
from online_users import online_users
from rest_framework.views import APIView


class Messages(APIView):
    """expects {recipientId, text, conversationId } in body (conversationId will be null if no conversation exists yet)"""

    def post(self, request):
        try:
            user = get_user(request)

            if user.is_anonymous:
                return HttpResponse(status=401)

            sender_id = user.id
            body = request.data
            conversation_id = body.get("conversationId")
            text = body.get("text")
            recipient_id = body.get("recipientId")
            sender = body.get("sender")
            isRead = body.get("isRead")

            # if we already know conversation id, we can save time and just add it to message and return
            if conversation_id:
                conversation = Conversation.objects.filter(id=conversation_id).first()
                message = Message(
                    senderId=sender_id, text=text, conversation=conversation, isRead=isRead,
                )
                message.save()
                message_json = message.to_dict()
                return JsonResponse({"message": message_json, "sender": body["sender"]})

            # if we don't have conversation id, find a conversation to m       ake sure it doesn't already exist
            conversation = Conversation.find_conversation(sender_id, recipient_id)
            if not conversation:
                # create conversation
                conversation = Conversation(user1_id=sender_id, user2_id=recipient_id)
                conversation.save()

                if sender and sender["id"] in online_users:
                    sender["online"] = True

            message = Message(senderId=sender_id, text=text, conversation=conversation, isRead=isRead)
            message.save()
            message_json = message.to_dict()
            return JsonResponse({"message": message_json, "sender": sender})
        except Exception as e:
            return HttpResponse(status=500)

    def patch(self, request):
        """update existing messages via PATCH
        currently only sets isRead flag; no mechanism for updating text/sender/etc
        """
        try:
            user = get_user(request)
            
            if user.is_anonymous:
                return HttpResponse(status=401)

            # TODO: only allow authorized users (users in the convo)
            user_id = user.id
            # FIXME: uncomment when convoId is in data
            # convo_id = request.data['convoId']
            # if not len(Conversation.objects.filter((Q(user1=user_id) | Q(user2=user_id)) & Q(pk=convo_id))):
            if not len(Conversation.objects.filter(Q(user1=user_id) | Q(user2=user_id))):
                return HttpResponse(status=401)

            message_ids = [msg['id'] for msg in request.data]
            updated = []
            with transaction.atomic():
                messages = Message.objects.\
                    select_for_update().\
                    filter(pk__in=message_ids).\
                    exclude(isRead=True)

                updated = messages
                for message in messages:
                    message.isRead = True
                
                n = Message.objects.bulk_update(messages, ['isRead'])
                
            updated_json = [
                msg.to_dict() 
                for msg in updated
            ]
            return JsonResponse({"messages" : updated_json})
        except Exception as e:
            return HttpResponse(status=500)