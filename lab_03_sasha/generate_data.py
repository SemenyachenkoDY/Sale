import pandas as pd
import numpy as np

def generate_files():
    print("Начинаю генерацию файлов для ETL (Вариант 3)...")
    np.random.seed(42)
    num_rows = 100000    
    product_ids = np.arange(1, num_rows + 1)
    
    print(f"Генерация main_warehouse.csv ({num_rows} строк)...")
    warehouse_balances = np.random.randint(0, 1000, size=num_rows)
    
    df_csv = pd.DataFrame({
        'product_id': product_ids,
        'warehouse_balance': warehouse_balances
    })
    
    df_csv.to_csv('main_warehouse.csv', index=False, encoding='utf-8')
    print("Файл main_warehouse.csv успешно сохранен.")

    print(f"Генерация deliveries.xlsx ({num_rows} строк)...")
    # Генерируем случайное количество поставок
    delivery_qty = np.random.randint(10, 500, size=num_rows)
    
    df_excel = pd.DataFrame({
        'product_id': product_ids,
        'delivery_qty': delivery_qty
    })
    df_excel.to_excel('deliveries.xlsx', index=False)
    print("Файл deliveries.xlsx успешно сохранен.")
    
    print("Генерация завершена!")

if __name__ == "__main__":
    try:
        generate_files()
    except ModuleNotFoundError as e:
        print(f"Ошибка импорта. Убедитесь, что установлены pandas, numpy и openpyxl.\nВыполните: pip install pandas numpy openpyxl\n[{e}]")
