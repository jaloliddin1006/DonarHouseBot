from asgiref.sync import sync_to_async
from tgbot.bot.loader import bot, STICERS
from tgbot.models import Branch, User, Category, Product, Order, OrderItem


async def get_cart_items_text(orderItems: list, order: Order = None):
    # print(orderItems)
    # print(order)
    total_price = 0
    text = "Sizning savatingizda quidagilar mavjud: \n\n"
    for index, item in orderItems:
        text += f"""{STICERS[index]} <b> {item.get("product__name")}</b> dan\n """
        text += f"""  >  {item.get("quantity")} ta  x  {int(item.get("product__price"))} so'm => {item.get("total_price")} so'm\n\n"""
        total_price += item.get("total_price")
        
    text += f"<b>Jami: {total_price} so'm </b>\n\n"
    
    if order:
        text += "Buyurtma ma'lumotlari:\n\n"
        text += f"Buyurtma Raqami: <b>#{order.id}</b>\n"
        if order.delivery == 'pickup':
            branch = await sync_to_async(Branch.objects.get)(id=order.branch_id)
            
            text += f"Buyurtma turi: <b>Olib ketish</b>\n"
            text += f"Filial: <a href='{branch.location}'><b>{branch.name}</b></a>\n"
            text += f"Olib ketuvchi: <b>{order.full_name}</b>\n"
            text += f"Telefon raqam: <b>{order.phone}</b>\n"
        else:
            text += f"Buyurtma turi: <b>Yetkazib berish</b>\n"
            text += f"Qabul qiluvchi: <b>{order.full_name}</b>\n"
            text += f"Telefon raqam: <b>{order.phone}</b>\n"
            text += f"Manzil: <b>{order.address}</b>\n"
            text += f"Qo'shimcha: <b>{order.addention}</b>\n"
        if order.is_paid:
            text += "Buyurtma holati: <b>To'lov amalga oshirildi</b>"
        else:
            text += "Buyurtma holati: <b>To'lov kutilmoqda</b>"
    
    return text

