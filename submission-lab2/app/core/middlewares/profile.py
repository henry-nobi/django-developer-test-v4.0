from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class UserProfileMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                # Get profile_id from header
                profile_id = request.headers.get('X-Profile-Id')
                
                if profile_id:
                    # Get specific profile by ID
                    user_profile = request.user.profiles.get(id=profile_id)
                else:
                    # Fallback to primary profile if no profile_id in header
                    user_profile = request.user.profiles.get(is_primary=True)
                
                user_language = user_profile.default_language
                translation.activate(user_language)
                request.LANGUAGE_CODE = user_language
                
                # Store the current profile in request for later use
                request.current_profile = user_profile
                
            except Exception as e:
                logger.warning(f"Failed to set user language: {str(e)}")
                translation.activate(settings.LANGUAGE_CODE)
                request.LANGUAGE_CODE = settings.LANGUAGE_CODE
                request.current_profile = None
        else:
            translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = settings.LANGUAGE_CODE
            request.current_profile = None 