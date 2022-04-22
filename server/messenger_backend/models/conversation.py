from django.db import models
from django.db.models import Q

from . import utils
from .user import User

class UserConversations(utils.CustomModel):
    """conversations for each user
    """
    userId = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="+"
    )
    conversationId = models.ForeignKey(
        "Conversation", on_delete=models.CASCADE, related_name="conversations"
    )
    
    class Meta:
        unique_together = ('userId', 'conversationId',)

class Conversation(utils.CustomModel):
    createdAt = models.DateTimeField(auto_now_add=True, db_index=True)
    updatedAt = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, through='UserConversations')


    # find a set of conversation given an iterable containing user Ids
    def find_conversation(users):
        # return a set of conversation or None if it doesn't exist
        try:
            return Conversation.objects.filter(UserConversations__pk__in=users)
        except Conversation.DoesNotExist:
            return None
