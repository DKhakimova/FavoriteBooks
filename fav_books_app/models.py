from django.db import models
from log_reg_app.models import User

# Create your models here.

class BookManager(models.Manager):
    def validate(self, form_data):
        errors = {}
        if len(form_data['title']) < 1:
            errors["title"] = "Title is required"
        if len(form_data['description']) < 5:
            errors["description"] = "Description should be at least 5 characters"
        return errors

class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=450)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")

    objects=BookManager()