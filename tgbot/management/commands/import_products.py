import json
from uuid import UUID
from django.core.management.base import BaseCommand
from tgbot.models import Category, Product
from django.db import transaction
import requests

from decimal import Decimal

BASE_URL = "https://api-ru.iiko.services"
organization_id = "7d69db4a-90ce-4eba-83e4-5c3a4eec4baf"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBcGlMb2dpbklkIjoiZGIzNWQ1Y2MtYTYzZi00NDBkLTg0NzktYzBiN2E3M2IxNzI1IiwibmJmIjoxNzM2MzM4MTQ0LCJleHAiOjE3MzYzNDE3NDQsImlhdCI6MTczNjMzODE0NCwiaXNzIjoiaWlrbyIsImF1ZCI6ImNsaWVudHMifQ.Xofdjix_f10Z6VDSYd3CxpSvgFAMNJZzadrUj7Q34AI"

class Command(BaseCommand):
    help = "Import categories into the database"
        
    def get_nomenclature(self):
        url = f"{BASE_URL}/api/1/nomenclature"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "organizationId": organization_id,
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
