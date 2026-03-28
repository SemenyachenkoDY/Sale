import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from datetime import datetime

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

DATA_PATH = os.getenv("DATA_PATH", "/data/WA_Fn-UseC_-HR-Employee-Attrition.csv")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "/output/chart.png")

if not os.path.exists(os.path.dirname(DATA_PATH)) and not DATA_PATH.startswith('/'):
    DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'WA_Fn-UseC_-HR-Employee-Attrition.csv'))
    OUTPUT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output', 'chart.png'))

print("=" * 60)
print("  IBM HR ANALYTICS — Линия тренда удовлетворенности сотрудников")
print("=" * 60)

os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

if not os.path.exists(DATA_PATH):
    print(f"[!] Файл {DATA_PATH} не найден.")
    
    try:
        import kaggle
        print("[!] Скачиваю с Kaggle...")
        kaggle.api.dataset_download_files(
            'pavansubhasht/ibm-hr-analytics-attrition-dataset',
            path=os.path.dirname(DATA_PATH),
            unzip=True
        )
        print(f"[✓] Данные загружены в {os.path.dirname(DATA_PATH)}")
    except ImportError:
        print("[!] Библиотека kaggle не установлена. Создаю тестовые данные...")
        
        np.random.seed(42)
        n_employees = 1470
        current_year = datetime.now().year
        
        df_test = pd.DataFrame({
            'YearsAtCompany': np.random.randint(0, 20, n_employees),
            'JobSatisfaction': np.random.randint(1, 5, n_employees),
            'EnvironmentSatisfaction': np.random.randint(1, 5, n_employees),
            'RelationshipSatisfaction': np.random.randint(1, 5, n_employees),
        })
        
        df_test['hire_date'] = pd.to_datetime(
            pd.Series([f"{current_year - y}/01/01" for y in df_test['YearsAtCompany']])
        )
        
        df_test['satisfaction_level'] = df_test[['JobSatisfaction', 'EnvironmentSatisfaction', 'RelationshipSatisfaction']].mean(axis=1) / 4
        
        df = df_test
        print(f"[✓] Создано {len(df)} тестовых записей")
        
    except Exception as e:
        print(f"[!] Ошибка загрузки: {e}")
        print("[!] Создаю минимальные тестовые данные...")
        
        np.random.seed(42)
        dates = pd.date_range(start='2015-01-01', end='2025-01-01', freq='MS')
        df = pd.DataFrame({
            'hire_date': np.random.choice(dates, 500),
            'satisfaction_level': np.random.uniform(0.3, 0.9, 500)
        })
        print(f"[✓] Создано {len(df)} тестовых записей")

if 'df' not in locals():
    df = pd.read_csv(DATA_PATH)
    print(f"\n[✓] Датасет загружен: {DATA_PATH}")
    print(f"[✓] Количество записей: {len(df)}")
    print(f"[✓] Количество признаков: {len(df.columns)}")
    
    if 'YearsAtCompany' in df.columns and 'hire_date' not in df.columns:
        current_year = datetime.now().year
        df['hire_date'] = pd.to_datetime(
            pd.Series([f"{current_year - y}/01/01" for y in df['YearsAtCompany']])
        )
        print(f"[✓] Создана колонка hire_date на основе YearsAtCompany")
    
    df['hire_date'] = pd.to_datetime(df['hire_date'])
    
    satisfaction_cols = []
    if 'JobSatisfaction' in df.columns:
        satisfaction_cols.append('JobSatisfaction')
    if 'EnvironmentSatisfaction' in df.columns:
        satisfaction_cols.append('EnvironmentSatisfaction')
    if 'RelationshipSatisfaction' in df.columns:
        satisfaction_cols.append('RelationshipSatisfaction')
    
    if satisfaction_cols:
        df['satisfaction_level'] = df[satisfaction_cols].mean(axis=1) / 4
        print(f"[✓] Создан индекс удовлетворенности на основе: {', '.join(satisfaction_cols)}")
    else:
        df['satisfaction_level'] = np.random.uniform(0.3, 0.9, len(df))
        print(f"[!] Использованы случайные данные для удовлетворенности")

time_series = df.resample('M', on='hire_date')['satisfaction_level'].mean().round(3)

print("\n── Динамика удовлетворенности сотрудников ────────────────")
print(f"Период: {time_series.index.min().strftime('%Y-%m')} - {time_series.index.max().strftime('%Y-%m')}")
print(time_series.tail(10).to_string())

plt.figure(figsize=(14, 8))

x_numeric = np.arange(len(time_series))
y_values = time_series.values

if len(time_series) > 1:
    coeffs = np.polyfit(x_numeric, y_values, 1)
    poly = np.poly1d(coeffs)
    trend_line = poly(x_numeric)
    
    plt.plot(time_series.index, trend_line, 
             color='#e74c3c', linewidth=4, linestyle='-', 
             label='ПРЯМАЯ ЛИНИЯ ТРЕНДА', zorder=10)
    
    std_error = np.std(y_values - trend_line)
    plt.fill_between(time_series.index, 
                     trend_line - std_error, 
                     trend_line + std_error, 
                     alpha=0.2, color='#e74c3c', zorder=5,
                     label='Коридор отклонений')
    
    plt.scatter(time_series.index, time_series.values, 
                color='#3498db', s=40, alpha=0.5, 
                label='Фактические значения', zorder=1)
    
    slope = coeffs[0]
    intercept = coeffs[1]
    
    print(f"\n📈 АНАЛИТИКА ТРЕНДА:")
    print(f"   Уравнение: y = {slope:.4f}·x + {intercept:.4f}")
    print(f"   Наклон: {slope:.4f} — {'возрастает' if slope > 0 else 'убывает' if slope < 0 else 'стабилен'}")
    
    first_val = trend_line[0]
    last_val = trend_line[-1]
    change = last_val - first_val
    change_percent = (change / first_val) * 100 if first_val != 0 else 0
    
    if slope > 0.001:
        trend_icon = "📈"
        trend_text = "ВОСХОДЯЩИЙ"
        trend_color = '#27ae60'
    elif slope < -0.001:
        trend_icon = "📉"
        trend_text = "НИСХОДЯЩИЙ"
        trend_color = '#e74c3c'
    else:
        trend_icon = "➡️"
        trend_text = "СТАБИЛЬНЫЙ"
        trend_color = '#f39c12'
    
    print(f"   Направление: {trend_icon} {trend_text}")
    print(f"   Изменение: {change:+.4f} ({change_percent:+.1f}%)")
    print(f"   Начальное: {first_val:.4f}")
    print(f"   Конечное: {last_val:.4f}")
    
    equation_text = f"y = {slope:.3f}·x + {intercept:.3f}"
    plt.annotate(f'{trend_icon} {equation_text}\nИзменение: {change:+.3f} ({change_percent:+.0f}%)',
                 xy=(0.02, 0.95), xycoords='axes fraction',
                 fontsize=11, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.4", facecolor='white', alpha=0.9, edgecolor=trend_color),
                 color=trend_color)

plt.title('IBM HR Analytics: Тренд удовлетворенности сотрудников', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Дата приема на работу', fontsize=12)
plt.ylabel('Средний уровень удовлетворенности (0-1)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.3, zorder=0)
plt.xticks(rotation=45)
plt.legend(loc='best', fontsize=10, framealpha=0.9)

if len(time_series) > 1:
    plt.text(time_series.index[-1], trend_line[-1], 
             f'  {trend_line[-1]:.3f}', 
             fontsize=10, fontweight='bold', color='#e74c3c',
             verticalalignment='center')
    plt.text(time_series.index[0], trend_line[0], 
             f'{trend_line[0]:.3f}  ', 
             fontsize=10, fontweight='bold', color='#e74c3c',
             horizontalalignment='right', verticalalignment='center')

plt.tight_layout()

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
plt.savefig(OUTPUT_PATH, dpi=150, bbox_inches='tight')
plt.close()

print(f"\n[✓] График сохранен: {OUTPUT_PATH}")
print("=" * 60)
