from django.contrib import admin
from . import models

class PremiseDatabaseadmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "created_by")

class CommentDatabaseadmin(admin.ModelAdmin):
    list_display = ("id", "parent", "created_at")

class ReplyOnCommentDatabaseadmin(admin.ModelAdmin):
    list_display = ("id", "parent", "created_at")

admin.site.register(models.ReplyOnComment, ReplyOnCommentDatabaseadmin)
admin.site.register(models.Comment, CommentDatabaseadmin)
admin.site.register(models.Premise, PremiseDatabaseadmin)