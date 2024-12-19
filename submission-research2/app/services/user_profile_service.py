from app.models.user_profile import UserProfile

class UserProfileService:
    @staticmethod
    def create_profile(user_id, company_id, display_name, **extra_fields):
        # If this profile is set as primary, set all other profiles for this user to non-primary
        if extra_fields.get('is_primary', False):
            UserProfile.objects.filter(user_id=user_id).update(is_primary=False)
            
        profile = UserProfile.objects.create(
            user_id=user_id,
            company_id=company_id,
            display_name=display_name,
            avatar=extra_fields.get('avatar'),
            default_language=extra_fields.get('default_language', 'en'),
            is_primary=extra_fields.get('is_primary', False),
            is_active=extra_fields.get('is_active', True)
        )
        return profile

    @staticmethod
    def get_profile(profile_id):
        try:
            return UserProfile.objects.get(pk=profile_id)
        except UserProfile.DoesNotExist:
            return None

    @staticmethod
    def update_profile(profile_id, **data):
        # If updating to make this profile primary, set all other profiles for this user to non-primary
        if data.get('is_primary', False):
            try:
                profile = UserProfile.objects.get(pk=profile_id)
                UserProfile.objects.filter(user_id=profile.user_id).update(is_primary=False)
            except UserProfile.DoesNotExist:
                return None
        try:
            profile = UserProfile.objects.get(pk=profile_id)
            for key, value in data.items():
                setattr(profile, key, value)
            profile.save()
            return profile
        except UserProfile.DoesNotExist:
            return None

    @staticmethod
    def delete_profile(profile_id):
        try:
            profile = UserProfile.objects.get(pk=profile_id)
            profile.delete()
            return True
        except UserProfile.DoesNotExist:
            return False

    @staticmethod
    def list_user_profiles(user_id):
        return UserProfile.objects.filter(user_id=user_id) 