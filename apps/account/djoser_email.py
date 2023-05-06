from djoser.email import (
    ActivationEmail,
    ConfirmationEmail,
    PasswordResetEmail,
    PasswordChangedConfirmationEmail,
    UsernameChangedConfirmationEmail,
    UsernameResetEmail,
)

from apps.notification.service import create_notification
from apps.notification.models import Notification


class MixinSendEmailNotification:

    def send(self, to, *args, **kwargs):
        self.render()

        user = self.context.get('user')

        notification = create_notification(
            recipient_email=to[0],
            subject=self.subject,
            message=self.body,
            html_message=self.html,
            group_notification=Notification.AUTH,
            user_id=user.id if user else None,
        )
        notification.send()


class ActivationEmailCustom(MixinSendEmailNotification, ActivationEmail):

    pass


class ConfirmationEmailCustom(MixinSendEmailNotification, ConfirmationEmail):
    pass


class PasswordResetEmailCustom(MixinSendEmailNotification, PasswordResetEmail):
    pass


class PasswordChangedConfirmationEmailCustom(MixinSendEmailNotification,
                                             PasswordChangedConfirmationEmail):
    pass


class UsernameChangedConfirmationEmailCustom(MixinSendEmailNotification,
                                             UsernameChangedConfirmationEmail):
    pass


class UsernameResetEmailCustom(MixinSendEmailNotification, UsernameResetEmail):
    pass
