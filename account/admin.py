from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('username', 'is_staff', 'purchase_car', 'sale_car')
    list_filter = ('is_staff',)

    fieldsets = (  # 사용자 상세페이지에 나오는 값들 / 이름, 비밀번호 빼고 작성하지 않아도됨
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('purchase_car', 'sale_car')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    )

    add_fieldsets = (  # 사용자 생성 시 적을 값들
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
