from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.pages"

    def ready(self):
        # Override admin_black RegistrationForm with our custom one,
        # since admin_black is still using the old "auth.User"
        # instead of get_user_model() or settings.AUTH_USER_MODEL
        from admin_black import views, forms
        from .forms import CustomRegistrationForm

        forms.RegistrationForm = CustomRegistrationForm
        views.RegistrationForm = CustomRegistrationForm
