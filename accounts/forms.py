from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# 커스텀한 UserCreationForm 정의
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields