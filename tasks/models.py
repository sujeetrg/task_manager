from django.db import models


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    priority = models.TextField(null=True, blank=True)
    status = models.TextField(null=True, blank=True)
    due_date = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Task {self.id} - {self.title}"

    class Meta:
        db_table = "task_manager_tasks"
        managed = True
