async def handle_sales_report(data):
    if not data:
        return "Данные по продажам отсутствуют."

    report = "📊 **Отчет по продажам**:\n"
    total_sales = 0
    total_commission = 0
    total_items = len(data)

    report += f"Всего товаров в отчете: {total_items}\n\n"

    for item in data:
        product_name = item.get("brand", "Не указано")
        price_with_disc = item.get("priceWithDisc", 0)
        total_price = item.get("totalPrice", 0)
        commission = total_price * 0.15  # 15% комиссия к примеру

        total_sales += total_price
        total_commission += commission

        report += f"Товар: {product_name}\n"
        report += f"  - Цена со скидкой: {price_with_disc} руб\n"
        report += f"  - Общая цена: {total_price} руб\n"
        report += f"  - Комиссия (15%): {commission:.2f} руб\n"
        report += "-" * 40 + "\n"

    report += f"\n🔹 **Общие данные**:\n"
    report += f"  - **Общая сумма продаж**: {total_sales} руб\n"
    report += f"  - **Общая комиссия**: {total_commission:.2f} руб\n"
    report += f"  - **Чистая прибыль** (после комиссии): {total_sales - total_commission:.2f} руб\n"

    return report



async def handle_stocks_report(data):
    if not data:
        return "Данные по товарам отсутствуют."

    report = "📦 **Отчет по наличию товаров**:\n"
    total_items = len(data)
    total_value = 0
    total_discounted_value = 0

    report += f"Всего товаров в отчете: {total_items}\n\n"

    for item in data:
        product_name = item.get("brand", "Не указано")
        category = item.get("category", "Не указана")
        subject = item.get("subject", "Не указано")
        price = item.get("Price", 0)
        quantity_full = item.get("quantityFull", 0)
        quantity_in_way = item.get("inWayToClient", 0)
        quantity_from_client = item.get("inWayFromClient", 0)
        total_value_for_product = price * quantity_full

        total_value += total_value_for_product
        total_discounted_value += total_value_for_product * (1 - item.get("Discount", 0) / 100)

        report += f"**Товар**: {product_name} ({category}, {subject})\n"
        report += f"  - Цена за единицу: {price} руб\n"
        report += f"  - Количество в наличии: {quantity_full} шт\n"
        report += f"  - Количество в пути к клиенту: {quantity_in_way} шт\n"
        report += f"  - Количество в пути от клиента: {quantity_from_client} шт\n"
        report += f"  - Общая стоимость товара: {total_value_for_product} руб\n"
        report += "-" * 40 + "\n"

    report += f"\n🔹 **Общие данные**:\n"
    report += f"  - **Общая стоимость всех товаров в наличии**: {total_value} руб\n"
    report += f"  - **Общая стоимость со скидками**: {total_discounted_value:.2f} руб\n"

    return report


async def handle_incomes_report(data):
    if not data:
        return "Данные о поступлении товаров отсутствуют."

    report = "📦 **Отчет по поступлению товаров**:\n"
    total_items = len(data)
    total_quantity = 0

    report += f"Всего поступлений в отчете: {total_items}\n\n"

    for item in data:
        product_name = item.get("supplierArticle", "Не указано")
        quantity = item.get("quantity", 0)
        warehouse = item.get("warehouseName", "Не указан")
        total_price = item.get("totalPrice", 0)
        status = item.get("status", "Не указан")
        date = item.get("date", "Не указана")
        last_change_date = item.get("lastChangeDate", "Не указана")
        date_close = item.get("dateClose", "Не указана")

        total_quantity += quantity

        report += f"**Поступление товара**: {product_name}\n"
        report += f"  - Количество поступивших единиц: {quantity} шт\n"
        report += f"  - Стоимость товара: {total_price} руб\n"
        report += f"  - Склад: {warehouse}\n"
        report += f"  - Статус: {status}\n"
        report += f"  - Дата поступления: {date}\n"
        report += f"  - Последнее изменение: {last_change_date}\n"
        report += f"  - Дата закрытия: {date_close}\n"
        report += "-" * 40 + "\n"

    report += f"\n🔹 **Общие данные**:\n"
    report += f"  - **Общее количество поступивших товаров**: {total_quantity} шт\n"

    return report


async def handle_orders_report(data):
    if not data:
        return "Данные по заказам отсутствуют."

    report = "📦 **Отчет по заказам**:\n"
    total_orders = len(data)
    total_sales = 0
    total_commission = 0
    canceled_orders = 0

    report += f"Всего заказов в отчете: {total_orders}\n\n"

    for item in data:
        order_number = item.get("incomeID", "Не указан")
        product_name = item.get("brand", "Не указано")
        total_price = item.get("totalPrice", 0)
        commission = total_price * 0.15  # Пример 15% комиссия
        is_cancel = item.get("isCancel", False)
        cancel_date = item.get("cancelDate", "Не указана")
        order_type = item.get("orderType", "Не указан")
        status = item.get("status", "Не указан")
        warehouse = item.get("warehouseName", "Не указан")
        date = item.get("date", "Не указана")

        total_sales += total_price
        total_commission += commission

        if is_cancel:
            canceled_orders += total_price
            report += f"❌ **Отменено** (Номер заказа: {order_number})\n"
            report += f"  - Дата отмены: {cancel_date}\n"
            report += f"  - Статус: {status}\n"
            report += f"  - Склад: {warehouse}\n"
            report += f"  - Цена заказа: {total_price} руб\n"
            report += "-" * 40 + "\n"
        else:
            report += f"**Заказ №{order_number}** ({order_type})\n"
            report += f"  - Товар: {product_name}\n"
            report += f"  - Общая сумма: {total_price} руб\n"
            report += f"  - Комиссия (15%): {commission:.2f} руб\n"
            report += f"  - Статус: {status}\n"
            report += f"  - Склад: {warehouse}\n"
            report += f"  - Дата заказа: {date}\n"
            report += "-" * 40 + "\n"

    report += f"\n🔹 **Общие данные**:\n"
    report += f"  - **Общая сумма всех заказов**: {total_sales} руб\n"
    report += f"  - **Общая комиссия**: {total_commission:.2f} руб\n"
    report += f"  - **Общая сумма отмененных заказов**: {canceled_orders} руб\n"
    report += f"  - **Чистая прибыль (после отмен)**: {total_sales - total_commission - canceled_orders:.2f} руб\n"

    return report


async def handle_reportDetailByPeriod(data):
    if not data:
        return "Детализированные данные отсутствуют."
    report = "Детализированный отчет по периодам:\n"

    for item in data:
        report += f"Период: {item.get('date', 'Не указан')} - Продажи: {item.get('totalPrice', 'Не указана')} руб\n"
    return report
