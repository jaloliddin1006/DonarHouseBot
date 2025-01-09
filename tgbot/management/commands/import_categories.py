from uuid import UUID
from django.conf import settings
from django.core.management.base import BaseCommand
from tgbot.bot.handlers.users.iiko_integration import get_token
from tgbot.models import Category
from django.db import transaction
import requests



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
                        "name_ru": ctg["name"],
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
