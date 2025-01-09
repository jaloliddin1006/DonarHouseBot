import requests

productId = "28437f20-7303-440d-a8ca-afde01732b7e"
customer_id="f8990000-6beb-ac1f-e366-08dd2e876d32"
API_KEY = "b391a9a839ed47fe87f65390acf50741"

import time
import uuid

# API bazaviy ma'lumotlari
API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBcGlMb2dpbklkIjoiZGIzNWQ1Y2MtYTYzZi00NDBkLTg0NzktYzBiN2E3M2IxNzI1IiwibmJmIjoxNzM2NDM4MzUyLCJleHAiOjE3MzY0NDE5NTIsImlhdCI6MTczNjQzODM1MiwiaXNzIjoiaWlrbyIsImF1ZCI6ImNsaWVudHMifQ.oWIenT53fYzo1XAwOejUblbdvLfB_VD5WL78bMnptJQ"
BASE_URL = "https://api-ru.iiko.services/api/1"

ORGANIZATION_ID = "7d69db4a-90ce-4eba-83e4-5c3a4eec4baf"
TERMINAL_GROUP_ID = "90cf7ac5-7d2c-070a-0189-637b206e0064"



########################## get access token ############################
def get_access_token(api_key):
    url = f"{BASE_URL}/api/1/access_token"
    response = requests.post(url, json={"apiLogin": api_key})
    response.raise_for_status()
    return response.json().get("token")

# access_token = get_access_token(API_KEY)


########################## get order types ############################

def get_order_types():
    url = f"{BASE_URL}/deliveries/order_types"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "organizationIds": [
            ORGANIZATION_ID
        ]
    }

    # So'rov yuborish
    response = requests.post(url, json=payload, headers=headers)
    
    # Javobni qaytarish
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

# Funksiyani chaqirish
# result = get_order_types()

# # Javobni chop etish
# print(result)


ORDER_TYPES = [
{'id': '5b1508f9-fe5b-d6af-cb8d-043af587d5c2', 'name': 'Доставка самовывоз', 'orderServiceType': 'DeliveryPickUp', 'isDeleted': False, 'externalRevision': 0, 'isDefault': True},

{'id': '76067ea3-356f-eb93-9d14-1fa00d082c4e', 'name': 'Доставка курьером', 'orderServiceType': 'DeliveryByCourier', 'isDeleted': False, 'externalRevision': 0, 'isDefault': True},

{'id': 'bbbef4dc-5a02-7ea3-81d3-826f4e8bb3e0', 'name': 'Обычный заказ', 'orderServiceType': 'Common', 'isDeleted': False, 'externalRevision': 0, 'isDefault': False}
]


#######################################  payment types ########################################

def get_payment_types(organization_id):
    url = f"{BASE_URL}/payment_types"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "organizationIds": [organization_id]
    }

    # So'rov yuborish
    response = requests.post(url, json=payload, headers=headers)
    
    # Javobni qaytarish
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

# result = get_payment_types(ORGANIZATION_ID)

# # Javobni chop etish
# print(result)

PAYMENT_TYPE_CASH_ID = "09322f46-578a-d210-add7-eec222a08871"















################################# create order ########################################



# Buyurtma yaratish uchun funktsiya
def create_order(order_type_id, customer_phone, customer_name, items):
    url = f"{BASE_URL}/order/create"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Buyurtma ma'lumotlari
    payload = {
    "organizationId": ORGANIZATION_ID,
    "terminalGroupId": TERMINAL_GROUP_ID,
    "order": {
        "phone": customer_phone,
        "customer": {
            "phone": customer_phone,
            "name": customer_name
        },
        "items": items,  # Mahsulotlar ro'yxati
        "orderTypeId": order_type_id,  # "Обычный заказ" (Common)
        "comment": "Test order via API. to'liq buyurtma uchun tayyorlandi. Iltimos, tayyorlab qo'ymanglar."
    }
}
    
    # So'rov yuboramiz
    response = requests.post(url, json=payload, headers=headers)
    print(response.status_code)
    
    # Javobni qaytaramiz
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

# Mahsulotlar ro'yxati (namuna)
items = [
    {
        "productId": productId,  # Mahsulot IDsi
        "amount": 2,                     # Miqdor
        "price": 10500,                  # Narx (so'mda)
        "type": "Product",                # Mahsulot turi
        "comment": "__TEST__. bot orqali zakaz, test uchun product buyurtma qilindi. Tayyorlab qo'ymanglar."
    }
]

# Buyurtma yaratish (Delivery turi uchun)
# result = create_order(
#     order_type_id=ORDER_TYPES[1]["id"],
#     customer_phone="+998900001122",
#     customer_name="Jaloliddin",
#     items=items
# )

# # Javobni ko'rsatamiz
# print(result)

# order_id = result.get("orderInfo").get("id")
# order_id = "9d3df77c-bf43-492a-b798-e235a1ed0f06"






#################################### order detail id ########################################
time.sleep(2)


# Buyurtma ma'lumotlarini olish uchun funksiya
def get_order_by_id(organization_id, order_ids=None):
    url = f"{BASE_URL}/order/by_id"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "organizationIds": [organization_id],
        "orderIds": order_ids,
    }

    # So'rov yuborish
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}


# order_ids = [order_id] 

# result = get_order_by_id(ORGANIZATION_ID, order_ids=order_ids)

# # # Javobni chop etish
# print(result)







####################################### delivery order create #################################3

import requests
import uuid

# API sozlamalari
# BASE_URL = "https://api-ru.iiko.services/api/1/deliveries/create"

# Buyurtma yaratish funktsiyasi
def create_delivery_order(
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
    url = BASE_URL + "/deliveries/create"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
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
                        "name": "Chilonzor ko'chasi",
                        "city": "Toshkent"
                    },
                    "house": "126 a",
                    "type": "legacy"
                },
                "comment": "Mijoz manzili, eshik tagida tursin"
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
        return response.json()
    else:
        return {
            "error": response.status_code,
            "message": response.text
        }


# Mahsulotlar ro'yxati (namuna)
items = [
    {
        "type": "Product",
        "amount": 20,
        "productId": productId,
        "comment": "Test uchun yaratilgan buyurtma"
    }
]

# Mijoz ma'lumotlari
# organization_id = "7bc05553-4b68-44e8-b7bc-37be63c6d9e9"
# terminal_group_id = "4fab19a5-203c-4bf5-94eb-f572aa8b117b"
# order_type_id = "c21c7b56-cdb7-4141-bc14-77df36146699"
customer_phone = "+998900001122"
customer_name = "Jaloliddin"
customer_address = "Toshkent, Chilonzor tumani, 12-uy"
latitude = 41.2995
longitude = 69.2401
comment = "Test buyurtma. Zakaz tayyorlanmasin!"

# Buyurtma yaratish
response = create_delivery_order(
    ORGANIZATION_ID,
    TERMINAL_GROUP_ID,
    ORDER_TYPES[1]["orderServiceType"],
    customer_phone,
    customer_name,
    customer_address,
    latitude,
    longitude,
    items,
    comment
)

# Javobni chop etamiz
# print(response)



order_id = response.get("orderInfo").get("id")




print("==//=="*15)

time.sleep(3)

###########################  delivery retrieves ###########################

# Funksiya: Buyurtma ma'lumotlarini olish
def get_delivery_by_id(organization_id, order_ids):
    url = f"{BASE_URL}/deliveries/by_id"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    # So'rov JSON ma'lumotlari
    payload = {
        "organizationId": organization_id,
        "orderIds": order_ids
    }

    # So'rov yuborish
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    # Javobni tekshirish
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": response.status_code,
            "message": response.text
        }



order_ids = [order_id]

# Funksiyani chaqirish
response = get_delivery_by_id(
    ORGANIZATION_ID,
    order_ids,
)

# Javobni chop etish
print(response)
