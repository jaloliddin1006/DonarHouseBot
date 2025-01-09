
from tgbot.models import Order, AccessToken, OrderItem
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
import requests
from asgiref.sync import sync_to_async
from uuid import UUID


def get_token():
    token = AccessToken.objects.last()
    
    if not token or (timezone.now() - token.created_at) > timedelta(minutes=50):
        url = f"{settings.IIKO_BASE_URL}/access_token"
        response = requests.post(url, json={"apiLogin": settings.IIKO_API_KEY})
        print(response.text)
        print(url)
        print(settings.IIKO_API_KEY)
        if response.status_code != 200:
            
            raise ValueError(f"==||== API KEY incorrect: {response.text} ==||== ")

        token_data = response.json()
        token = AccessToken.objects.create(token=token_data.get("token"))
    
    return token


def create_iiko_delivery_order(
    TOKEN,
    organization_id,
    terminal_group_id,
    order_type,
    customer_phone,
    customer_name,
    customer_address,
    latitude,
    longitude,
    items,
    comment=None
):
    url = settings.IIKO_BASE_URL + "/deliveries/create"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    # Buyurtma ma'lumotlari
    payload = {
        "organizationId": organization_id,
        "terminalGroupId": terminal_group_id,
        "createOrderSettings": {
            "transportToFrontTimeout": 0,
            "checkStopList": False
        },
        "order": {
            "phone": customer_phone,
            "customer": {
                "name": customer_name
            },
            "orderServiceType": order_type, # "DeliveryByCourier" "DeliveryByClient"
            "deliveryPoint": {
                "coordinates": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "address": {
                    "street": {
                        "name": customer_address,
                        "city": "Toshkent"
                    },
                    "house": "None",
                    "type": "legacy"
                },
                "comment": customer_address
            },
            "comment": comment,
            "items": items 
        }
    }

    # So'rov yuboramiz
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    # Javobni tekshiramiz
    if response.status_code == 200:
        return {
            "code": response.status_code,
            "data": response.json()
        }
   
    return {
        "code": response.status_code,
        "data": response.json()
    }



async def create_order(order: Order):
    products = await sync_to_async(list)(OrderItem.objects.get_iiko_info(order.id))
    items = []
    for item in products:
        items.append(
            {
                "type": "Product",
                "amount": item['quantity'],
                "productId": str(item['product__uuid']),
                "comment": "Bot orqali qilingan buyurtma"
            }
        )
    print(items)
    
    if not order.branch:
        terminal_id = settings.TERMINAL_GROUP_ID_1
    else: 
        terminal_id = order.branch.terminal_id
        
    order_type = order.delivery
    customer_phone = order.phone
    customer_name = order.full_name
    customer_address = order.address
    longitude = order.longitude
    latitude = order.latitude
    comment = order.addention
    TOKEN = await sync_to_async(get_token)()
    response = await sync_to_async(create_iiko_delivery_order)(
        TOKEN = TOKEN,
        organization_id=settings.IIKO_ORGANIZATION_ID,
        terminal_group_id=terminal_id,
        order_type=order_type,
        customer_phone=customer_phone,
        customer_name=customer_name,
        customer_address=customer_address,
        latitude=latitude,
        longitude=longitude,
        items=items,
        comment=comment
    )
    order.iiko_order_id = response.get("data").get("orderInfo").get("id")
    await order.asave()
    return response
    
    

# print("==//=="*15)

# time.sleep(3)

# ###########################  delivery retrieves ###########################

# # Funksiya: Buyurtma ma'lumotlarini olish
async def get_delivery_info_by_id(order_ids):
    url = f"{settings.IIKO_BASE_URL}/deliveries/by_id"
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json"
    }

    payload = {
        "organizationId": settings.ORGANIZATION_ID,
        "orderIds": order_ids
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

    if response.status_code == 200:
        return {
            "code": response.status_code,
            "data": response.json()
        }
    else:
        return {
            "code": response.status_code,
            "data": response.json()
        }



# order_ids = [order_id]

# # Funksiyani chaqirish
# response = get_delivery_by_id(
#     ORGANIZATION_ID,
#     order_ids,
# )

# # Javobni chop etish
# print(response)
