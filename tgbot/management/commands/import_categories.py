import json
from uuid import UUID
from django.core.management.base import BaseCommand
from tgbot.models import Category
from django.db import transaction
import requests


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
        # Kategoriyalarni bazaga qo'shish
        with transaction.atomic():
            categories = {}  # Parentni saqlash uchun dict
            for ctg in nomenclature.get("groups", []):
                 # Parentni aniqlash
                parent = None
                if ctg.get("parentGroup"):
                    try:
                        parent = Category.objects.get(uuid=UUID(ctg["parentGroup"]))
                    except Category.DoesNotExist:
                        print(f"Parent topilmadi: {ctg['parentGroup']}")
                        continue

                # Kategoriya yaratish yoki yangilash
                category, created = Category.objects.update_or_create(
                    uuid=UUID(ctg["id"]),
                    defaults={
                        "order": ctg["order"],
                        "name": ctg["name"],
                        "description": ctg.get("description"),
                        "parent": parent,
                        "image": "categories/background.png"
                    },
                )
                if created:
                    print(f"Kategoriya yaratildi: {category.name}")
                else:
                    print(f"Kategoriya yangilandi: {category.name}")
                action = "Created" if created else "Updated"
                self.stdout.write(f"{action} category: {category.name}")

        self.stdout.write("All categories imported successfully.")
