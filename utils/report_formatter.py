def generate_report_from_data(data):
    cards_data = data.get('data', {}).get('cards', [])

    if not cards_data:
        return "Отчет недоступен."

    report = "Отчет о товарах:\n\n"

    total_sales_sum = 0
    total_commission = 0
    total_discounts = 0
    total_payment_system_commission = 0
    total_logistics_cost = 0
    total_storage_cost = 0
    total_units_sold = 0

    for idx, card in enumerate(cards_data, 1):
        nmID = card.get('nmID', 'Не указан')
        vendorCode = card.get('vendorCode', 'Не указан')
        brandName = card.get('brandName', 'Не указан')
        price = card.get('price', 'Не указана')
        quantity = card.get('quantity', 'Не указано')

        stats = card.get('statistics', {})
        selected_period = stats.get('selectedPeriod', {})
        previous_period = stats.get('previousPeriod', {})

        report += f"Товар {idx}:\n"
        report += f"  - ID: {nmID}\n"
        report += f"  - Код: {vendorCode}\n"
        report += f"  - Бренд: {brandName}\n"
        report += f"  - Цена: {price}\n"
        report += f"  - Количество: {quantity}\n"

        orders_sum_rub = selected_period.get('ordersSumRub', 0)
        buyouts_sum_rub = selected_period.get('buyoutsSumRub', 0)
        discounts_sum_rub = selected_period.get('cancelSumRub', 0)
        commission_percentage = 0.15
        payment_system_commission_percentage = 0.02
        logistics_cost_percentage = 0.05


        total_sales_sum += buyouts_sum_rub
        total_commission += buyouts_sum_rub * commission_percentage
        total_discounts += discounts_sum_rub
        total_payment_system_commission += buyouts_sum_rub * payment_system_commission_percentage
        total_logistics_cost += buyouts_sum_rub * logistics_cost_percentage
        total_units_sold += selected_period.get('buyoutsCount', 0)
        avg_price = buyouts_sum_rub / selected_period.get('buyoutsCount', 1) if selected_period.get('buyoutsCount',
                                                                                                    0) > 0 else 0

        report += f"\nСтатистика за выбранный период ({selected_period.get('begin')} - {selected_period.get('end')}):\n"
        report += f"  - Сумма заказов: {orders_sum_rub} руб\n"
        report += f"  - Сумма выкупов: {buyouts_sum_rub} руб\n"
        report += f"  - Сумма скидок: {discounts_sum_rub} руб\n"
        report += f"  - Комиссия Wildberries: {buyouts_sum_rub * commission_percentage} руб\n"
        report += f"  - Комиссия эквайринга: {buyouts_sum_rub * payment_system_commission_percentage} руб\n"
        report += f"  - Стоимость логистики: {buyouts_sum_rub * logistics_cost_percentage} руб\n"

        report += f"  - Количество проданных единиц: {selected_period.get('buyoutsCount', 0)}\n"
        report += f"  - Средняя цена продажи: {avg_price} руб\n"

        report += "\n"

    report += "\nОбщие показатели по всем товарам:\n"
    report += f"  - Общая сумма продаж: {total_sales_sum} руб\n"
    report += f"  - Общая комиссия Wildberries: {total_commission} руб\n"
    report += f"  - Общие скидки Wildberries: {total_discounts} руб\n"
    report += f"  - Общая комиссия эквайринга: {total_payment_system_commission} руб\n"
    report += f"  - Общая стоимость логистики: {total_logistics_cost} руб\n"
    report += f"  - Общая стоимость хранения: {total_storage_cost} руб\n"
    report += f"  - Всего проданных единиц: {total_units_sold}\n"

    return report
