import stripe

from drf_hw.settings import STRIPE_API_KEY
from lms.models import Course

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(course):
    """Создание продукта в Stripe."""

    return stripe.Product.create(name=course.title)


def create_stripe_price(amount, course):
    """Создание цены в Stripe."""

    product = create_stripe_product(course)

    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product=product.id,
    )


def create_stripe_session(price):
    """Создание сессии в Stripe."""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )

    return session.get("id"), session.get("url")
