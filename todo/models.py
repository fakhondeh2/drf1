from django.db import models

# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.IntegerField(default=1)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}/{self.is_done}"


    class Meta:
        db_table = "todos"

