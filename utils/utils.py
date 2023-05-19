from allauth.socialaccount.models import SocialAccount

def get_user_info(request):
    user_info = {}
    if request.user.is_authenticated:
        try:
            extra_data = SocialAccount.objects.get(user=request.user).extra_data
            user_info["picture"] = extra_data["picture"]
            user_info["name"] = extra_data["name"]
        except:
            pass
    return user_info
