from django.contrib import admin

from .models import Conversation, ChatBox, Messages


# Register your models here.

class ConversationAdmin(admin.ModelAdmin):
    list_display = ("starter", "second_party", "date_created")
    list_filter = ("is_active",)


admin.site.register(ChatBox)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Messages)
