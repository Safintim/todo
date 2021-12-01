from django.db import models


class CommonFields(models.Model):
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TaskList(CommonFields):
    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Список'
        verbose_name_plural = 'Списки'


class Task(CommonFields):
    description = models.TextField(null=True)
    list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
