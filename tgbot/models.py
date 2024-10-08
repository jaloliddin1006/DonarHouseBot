from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class User(BaseModel):
    telegram_id = models.PositiveBigIntegerField(unique=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "telegram_users"


class BotAdmin(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            pass
        super(BotAdmin, self).save(*args, **kwargs)
        
    class Meta:
        db_table = "bot_admins"