from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import Context
from django.template.loader import render_to_string

from store.models import Cart, BookOrder


@receiver(post_save, sender=Cart)
def adjust_stock(sender, instance, **kwards):
    if not instance.active:
        orders = BookOrder.objects.filter(cart=instance)
        for order in orders:
            book = order.book
            book.stock -= order.quantity
            book.save()

        # thanks email
        subject = 'Thanks ...'
        from_email = 'some@gmail.com'
        to_email = [instance.email]

        email_context = Context({
            'username': instance.user.username,
            'orders': orders
        })

        text_content = render_to_string('email/purchase_email.txt', email_context)
        html_content = render_to_string('email/purchase_email.html', email_context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
