from django.contrib.auth import get_user_model
from admin_black.forms import RegistrationForm as AdminBlackRegistrationForm

User = get_user_model()


class CustomRegistrationForm(AdminBlackRegistrationForm):
    """
    Base registration form to override the default admin_black's
    registration form.

    Need to swap the default "auth.User" model into get_user_model(),
    while retaining all the fields.
    """

    class Meta(AdminBlackRegistrationForm.Meta):
        model = User
        fields = AdminBlackRegistrationForm.Meta.fields  # keep all fields
