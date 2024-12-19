from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.models import Token
from app.models.user import User
from app.services.email_service import EmailService
from django.conf import settings
import base64
from django.utils import timezone

class AuthService:
    @staticmethod
    def login_user(request, email, password):
        user = authenticate(username=email, password=password)
        if user and user.is_active:
            return user
        return None

    @staticmethod
    def create_auth_token(user):
        # Get or create a new token
        token, created = Token.objects.get_or_create(user=user)
        return token.key

    @staticmethod
    def logout_user(request):
        """
        Logs out user by:
        1. Deleting their auth token
        2. Logging them out of their session
        """
        try:
            # Delete the user's auth token if it exists
            if request.user.is_authenticated:
                Token.objects.filter(user=request.user).delete()
                
            # Import here to avoid circular import
            from django.contrib.auth import logout
            logout(request)
            
            return True
        except Exception as e:
            print(f"Error during logout: {str(e)}")
            return False

    @staticmethod
    def reset_password(email):
        try:
            user = User.objects.get(email=email)
            # Generate reset token
            encode_uid_bytes = user.pk.to_bytes((user.pk.bit_length() + 7) // 8 or 1, byteorder='big')
            encoded_uid = base64.urlsafe_b64encode(encode_uid_bytes).decode('utf-8')
            token = default_token_generator.make_token(user)
            # Create reset URL
            reset_url = f"{settings.FRONTEND_URL}/reset-password?uid={encoded_uid}&token={token}"
            # Send reset email
            EmailService.send_password_reset_email(user.email, reset_url)
            return True
        except User.DoesNotExist:
            return False

    @staticmethod
    def confirm_reset_password(uid, token, new_password):
        try:
            # Decode the user ID
            decoded_uid_bytes = base64.urlsafe_b64decode(uid)

            # Convert bytes back to integer
            user_id = int.from_bytes(decoded_uid_bytes, byteorder='big')
            user = User.objects.get(pk=user_id)
            
            # Verify the token
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return True
            return False
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return False