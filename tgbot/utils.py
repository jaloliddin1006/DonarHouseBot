from django.conf import settings
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderInsufficientPrivileges
from asgiref.sync import sync_to_async
from tgbot.models import BotAdmin


async def get_address(latitude, longitude):
    geolocator = Nominatim(user_agent="DonarHouseBot (jmamatmusayev@gmail.com)")
    try:
        # sync_to_async ishlatiladi, chunki geolocator.reverse sinxron metod
        location = await sync_to_async(geolocator.reverse)(f"{latitude}, {longitude}", language="en")
        return location.address if location else "Address not found"
    except (GeocoderTimedOut, GeocoderInsufficientPrivileges) as e:
        print(f"Error occurred: {e}")
        return "Could not retrieve address due to an error."
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Could not retrieve address due to an error."
    
    
async def get_admins():
    ADMINS = []
    ADMINS += settings.ADMINS

    BOT_ADMINS = await sync_to_async(
        lambda: list(BotAdmin.objects.filter(is_active=True).values_list('user__telegram_id', flat=True)),
        thread_sensitive=True
    )()
    ADMINS += BOT_ADMINS

    return ADMINS
