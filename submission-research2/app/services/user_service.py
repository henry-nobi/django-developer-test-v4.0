from app.models.user import User
from app.models.user_profile import UserProfile
from django.db import transaction
from django.utils.translation import gettext as _

class UserService:
    @staticmethod
    def change_password(user, old_password, new_password):
        """
        Change user's password
        Returns True if password was changed successfully, False otherwise
        """
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return True
        return False

    @staticmethod
    def create_user(email, password, **extra_fields):
        user = User.objects.create_user(email=email, password=password)
        
        # Create user profile if company and display_name are provided
        company = extra_fields.get('company')
        display_name = extra_fields.get('display_name')
        if company and display_name:
            UserProfile.objects.create(
                user=user,
                company=company,
                display_name=display_name,
                avatar=extra_fields.get('avatar'),
                default_language=extra_fields.get('default_language', 'en'),
                is_primary=extra_fields.get('is_primary', True),
                is_active=extra_fields.get('is_active', True)
            )
        return user

    @staticmethod
    def get_user(user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None

    @staticmethod
    def update_user(user_id, **extra_fields):
        try:
            user = User.objects.get(pk=user_id)
            for key, value in extra_fields.items():
                setattr(user, key, value)
            user.save()
            return user
        except User.DoesNotExist:
            return None

    @staticmethod
    def delete_user(user_id):
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False

    @staticmethod
    def update_user_profile(user_id, **profile_data):
        try:
            user = User.objects.get(pk=user_id)
            profile = user.active_profile
            
            if profile:
                for key, value in profile_data.items():
                    setattr(profile, key, value)
                profile.save()
                return profile
            return None
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_email(email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user_profiles(user_id):
        """
        Get all profiles for a user
        """
        try:
            user = User.objects.get(pk=user_id)
            return user.profiles.all().order_by('-is_primary', '-created_at')
        except User.DoesNotExist:
            raise Exception(_("User not found"))

    @staticmethod
    def switch_active_profile(user_id, profile_id):
        """
        Switch the active profile for a user
        Returns True if successful, False otherwise
        """
        try:
            user = User.objects.get(pk=user_id)
            new_active_profile = user.profiles.get(pk=profile_id)
            
            # Verify the profile belongs to the user
            if new_active_profile.user_id != user_id:
                raise Exception(_("Profile does not belong to user"))
            
            # Begin transaction
            with transaction.atomic():
                # Set all profiles to not primary
                user.profiles.all().update(is_primary=False)
                
                # Set the selected profile as primary
                new_active_profile.is_primary = True
                new_active_profile.save()
                
            return True
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            return False
        except Exception as e:
            print(f"Error switching profile: {str(e)}")
            return False