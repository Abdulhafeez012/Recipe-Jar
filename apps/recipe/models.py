from django.db import models
from django.contrib.auth.models import User




class RecipeJarUser(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)
    phone_number = models.CharField(max_length=100, null=True)
    weight = models.FloatField(null=True)
    height = models.FloatField(null=True)
    selected_shopping_list = models.CharField(max_length=150, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

