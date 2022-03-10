from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
# from .models import FriendRequest, FriendList

User = get_user_model()


class UserAdminCustom(UserAdmin):
    # ユーザー詳細
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'email',
                'password',
                'image',
                'introduction',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'name',
                'email',
                'password1',
                'password2',
                'image',
                'introduction',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

    # ユーザー一覧
    list_display = (
        'id',
        'name',
        'email',
        'is_active'
    )

    list_filter = ()
    list_display_links = ('id', 'name', 'email')
    # 検索
    search_fields = ('email',)
    # 順番
    ordering = ('id',)

# class FriendListAdmin(admin.ModelAdmin):
#     list_filter = ['user']
#     list_display = ['user']
#     search_fields = ['user']
#     readonly_fields = ['user']

#     class Meta:
#         model = FriendList

# class FriendRequestAdmin(admin.ModelAdmin):
# 	list_filter = ['sender', 'receiver']
# 	list_display = ['sender', 'receiver']
# 	search_fields = ['sender__user',  'sender__email', 'receiver__email', 'receiver__user']
# 	class Meta:
# 		model = FriendRequest

# admin.site.register(FriendList, FriendListAdmin)
# admin.site.register(FriendRequest, FriendRequestAdmin)


admin.site.register(User, UserAdminCustom)
