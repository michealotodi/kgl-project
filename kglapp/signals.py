# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models import UserProfile

# # Signal to create or update the user profile when a user is saved
# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     # Create a user profile if one doesn't exist
#     if created:
#         UserProfile.objects.create(user=instance)
#     else:
#         # Ensure that the user profile exists before trying to save it
#         if hasattr(instance, 'userprofile'):
#             instance.userprofile.save()
#         else:
#             # If no userprofile exists, create one
#             UserProfile.objects.create(user=instance)
