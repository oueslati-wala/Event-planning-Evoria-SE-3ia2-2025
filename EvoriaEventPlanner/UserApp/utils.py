from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Generate a token for account activation.
    """

    pass


account_activation_token = AccountActivationTokenGenerator()
