from dataclasses import dataclass
from typing import List

from aiogram.types import LabeledPrice

from django.conf import settings


@dataclass
class Product:
    """
    https://core.telegram.org/bots/api#sendinvoice
    """
    title: str
    description: str
    start_parameter: str
    currency: str
    prices: List[LabeledPrice]
    provider_data: str = None
    photo_url: str = None
    photo_size: int = None
    photo_width: int = None
    photo_height: int = None
    need_name: bool = False
    need_phone_number: bool = False
    need_email: bool = False
    need_shipping_address: bool = False
    send_phone_number_to_provider: bool = False
    send_email_to_provider: bool = False
    is_flexible: bool = False
    # max_tip_amount: int = None
    # suggested_tip_amounts: List[int] = None,

    provider_token: str = settings.PAYMENT_TOKEN_CLICK

    def generate_invoice(self):
        return self.__dict__