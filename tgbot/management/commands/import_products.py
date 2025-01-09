from uuid import UUID
from django.conf import settings
from django.core.management.base import BaseCommand
from tgbot.bot.handlers.users.iiko_integration import get_token
from tgbot.models import Category, Product
from django.db import transaction
import requests

from decimal import Decimal


class Command(BaseCommand):
    help = "Import categories into the database"
        
    def get_nomenclature(self):
        url = f"{settings.IIKO_BASE_URL}/nomenclature"
        headers = {
            "Authorization": f"Bearer {get_token()}",
            "Content-Type": "application/json"
        }
        payload = {
            "organizationId": settings.IIKO_ORGANIZATION_ID,
            "startRevision": 0
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Xatoliklarni aniqlash uchun
        return response.json()

    def handle(self, *args, **kwargs):
       
        nomenclature = self.get_nomenclature()
        with transaction.atomic():
            for product in nomenclature.get("products", []):
                if not product["parentGroup"]:
                    continue
                current_price = product["sizePrices"][0]["price"]["currentPrice"]
                if not current_price:
                    continue
                category = Category.objects.get(uuid=UUID(product["parentGroup"]))
                

                # Mahsulotni yaratish yoki yangilash
                _, created = Product.objects.update_or_create(
                    uuid=UUID(product["id"]),
                    defaults={
                        "name": product["name"],
                        "name_ru": product["name"],
                        "code": product["code"],
                        "category": category,
                        "price": Decimal(current_price),
                        "description": product.get("description", ""),
                    }
                )
                print(f"Mahsulot saqlandi: {product['name']}")
                action = "Created" if created else "Updated"
                self.stdout.write(f"{action} category: {category.name}")

        self.stdout.write("All categories imported successfully.")
