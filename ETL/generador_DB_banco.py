# -*- coding: utf-8 -*-
import random
import time
import json
import urllib.parse
from datetime import timedelta
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from faker import Faker
from tqdm import tqdm

# ==========================================
# 1. CONFIGURACIÓN BASE
# ==========================================
USER = "root"
PASSWORD = "Cualquiera1"  # <-- REEMPLAZA CON TU CONTRASEÑA
HOST = "localhost"
DB = "BancoDB"  # Apuntando a tu base de datos correcta

NUM_USERS = 5000         
NUM_DEVICES = 8000       
NUM_ACCOUNTS = 7000     
NUM_TRANSACTIONS = 150000 

db_encoded = urllib.parse.quote_plus(DB)
try:
    engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{db_encoded}")
    pd.read_sql("SELECT 1", engine)
except Exception as e:
    print(f"❌ Error de conexión. Verifica que MySQL esté corriendo y BancoDB exista.\nDetalles: {e}")
    exit(1)

fake = Faker(['es_ES', 'es_MX', 'es_CO', 'en_US'])
Faker.seed(42)
np.random.seed(42)

df_tx_global = None

# ==========================================
# 2. CATÁLOGOS REALISTAS
# ==========================================

NOMBRES_HOMBRE = [
    "Mateo", "Santiago", "Alejandro", "Leonardo", "Daniel", "Sebastián", "Nicolás", "Samuel", 
    "David", "Diego", "Carlos", "Javier", "Andrés", "Juan Pablo", "Luis", "Gabriel", "Fernando", 
    "Martín", "Joaquín", "Emiliano", "Tomás", "Lucas", "Felipe", "Camilo", "Esteban", "Miguel"
]

NOMBRES_MUJER = [
    "Sofía", "Valentina", "Isabella", "Camila", "Mariana", "Victoria", "Martina", "Daniela", 
    "Lucía", "Catalina", "Valeria", "María José", "Samantha", "Juliana", "Andrea", "Sara", 
    "Gabriela", "Natalia", "Paula", "Laura", "Alejandra", "Carolina", "Diana", "Ana María"
]

APELLIDOS = [
    "Rodríguez", "Martínez", "García", "Gómez", "López", "González", "Pérez", "Sánchez", 
    "Ramírez", "Torres", "Flores", "Díaz", "Vásquez", "Cruz", "Morales", "Ortiz", "Gutiérrez", 
    "Chávez", "Ruiz", "Álvarez", "Fernández", "Jiménez", "Mendoza", "Castillo", "Rojas"
]

CATALOGO_DISPOSITIVOS = [
    ("Mobile", "Apple", "iPhone 13", "iOS"), ("Mobile", "Apple", "iPhone 14 Pro", "iOS"),
    ("Tablet", "Apple", "iPad Pro 12.9", "iOS"), ("Desktop", "Apple", "MacBook Pro", "macOS"),
    ("Mobile", "Samsung", "Galaxy S23", "Android"), ("Mobile", "Samsung", "Galaxy A54", "Android"),
    ("Tablet", "Samsung", "Galaxy Tab S9", "Android"), ("Desktop", "Samsung", "Galaxy Book3", "Windows"),
    ("Mobile", "Xiaomi", "Redmi Note 12", "Android"), ("Mobile", "Motorola", "Edge 40", "Android"),
    ("Desktop", "Lenovo", "ThinkPad T14", "Windows"), ("Desktop", "Dell", "XPS 13", "Windows")
]

def generar_telefono():
    """Genera números compactos sin espacios para respetar VARCHAR(15)"""
    opciones = [
        lambda: f"+573{random.randint(0,2)}{random.randint(0,9)}{random.randint(100,999)}{random.randint(1000,9999)}",
        lambda: f"+52{random.choice(['55', '81', '33'])}{random.randint(1000,9999)}{random.randint(1000,9999)}",
        lambda: f"+346{random.randint(0,9)}{random.randint(0,9)}{random.randint(10,99)}{random.randint(10,99)}{random.randint(10,99)}",
        lambda: f"+1{random.randint(200,999)}{random.randint(200,999)}{random.randint(1000,9999)}"
    ]
    return random.choices(opciones, weights=[0.5, 0.25, 0.1, 0.15])[0]()

# ==========================================
# 3. FUNCIONES DE CARGA (ETL BLINDADO)
# ==========================================

def f_monedas():
    monedas = [
        ("USD", "US Dollar", False), ("EUR", "Euro", False),
        ("GBP", "British Pound", False), ("JPY", "Japanese Yen", False),
        ("COP", "Peso Colombiano", False), ("MXN", "Peso Mexicano", False),
        ("BTC", "Bitcoin", True), ("ETH", "Ethereum", True), ("USDT", "Tether", True)
    ]
    pd.DataFrame(monedas, columns=["c_code", "c_name", "is_crypto"]).to_sql("currencies", engine, if_exists="append", index=False)

def f_tipos_transaccion():
    tipos = [
        ("Deposit", "Ingreso de dinero a la cuenta (+)", 1),
        ("Transfer In", "Transferencia recibida de un tercero (+)", 1),
        ("Withdrawal", "Retiro de efectivo (-)", -1),
        ("Payment", "Pago de servicios o comercio (-)", -1),
        ("Transfer Out", "Transferencia enviada a un tercero (-)", -1),
        ("Fee", "Comisión bancaria (-)", -1)
    ]
    df = pd.DataFrame([(t[0][:30], t[1][:250]) for t in tipos], columns=["t_name", "t_description"])
    df.to_sql("transactions_types", engine, if_exists="append", index=False)

def f_usuarios():
    usuarios = []
    emails_generados = set()
    
    for _ in range(NUM_USERS):
        f_date = fake.date_time_between(start_date="-3y", end_date="-1M")
        es_hombre = random.choice([True, False])
        primer_nombre = random.choice(NOMBRES_HOMBRE) if es_hombre else random.choice(NOMBRES_MUJER)
        apellido_paterno = random.choice(APELLIDOS)
        apellido_materno = random.choice(APELLIDOS)
        
        email = f"{primer_nombre.lower()}.{apellido_paterno.lower()}{random.randint(1,999)}@{fake.free_email_domain()}"
        email = email.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
        while email in emails_generados:
            email = f"{primer_nombre.lower()}.{apellido_paterno.lower()}{random.randint(1000,99999)}@{fake.free_email_domain()}"
        emails_generados.add(email)
        
        # Blindaje estricto de longitudes para evitar Crash 1406
        p_name = primer_nombre[:30]
        p_last = f"{apellido_paterno} {apellido_materno}"[:30]
        p_email = email[:55]
        p_phone = generar_telefono()[:15]
        
        usuarios.append([
            p_name, p_last, p_email, p_phone,
            np.random.choice(["ACTIVE", "INACTIVE"], p=[0.85, 0.15]), f_date, f_date + timedelta(days=random.randint(1, 30))
        ])
        
    df = pd.DataFrame(usuarios, columns=["first_name", "last_name", "gmail", "phone", "kyc_status", "created_at", "updated_at"])
    df.to_sql("users", engine, if_exists="append", index=False, chunksize=10000)

def f_dispositivos():
    df_u = pd.read_sql("SELECT user_id, created_at FROM users", engine)
    dispositivos = []
    
    for _ in range(NUM_DEVICES):
        u = df_u.sample(1).iloc[0]
        c_date = fake.date_time_between_dates(datetime_start=u["created_at"])
        _, marca, modelo, sistema = random.choice(CATALOGO_DISPOSITIVOS)
        
        device_name = f"{marca} {modelo}"[:45]
        os_name = sistema[:45]
        
        dispositivos.append([
            int(u["user_id"]), device_name, os_name,
            fake.date_time_between_dates(datetime_start=c_date), c_date
        ])
    pd.DataFrame(dispositivos, columns=["user_id", "device_type", "os", "last_login_at", "create_at"]).to_sql("user_device", engine, if_exists="append", index=False, chunksize=10000)

def f_cuentas():
    df_u = pd.read_sql("SELECT user_id, created_at FROM users", engine)
    df_c = pd.read_sql("SELECT currency_id FROM currencies", engine)
    cuentas = []
    
    for _ in range(NUM_ACCOUNTS):
        u = df_u.sample(1).iloc[0]
        curr = df_c.sample(1).iloc[0]
        cuentas.append([
            int(u["user_id"]), int(curr["currency_id"]), np.random.choice(["SAVINGS", "CHECKING", "CREDIT"], p=[0.6, 0.3, 0.1]),
            np.random.choice(["ACTIVE", "INACTIVE"], p=[0.9, 0.1]), fake.date_time_between_dates(datetime_start=u["created_at"])
        ])
    pd.DataFrame(cuentas, columns=["user_id", "currency_id", "account_type", "a_status", "create_at"]).to_sql("accounts", engine, if_exists="append", index=False, chunksize=10000)

def f_transacciones():
    global df_tx_global
    df_acc = pd.read_sql("SELECT account_id, currency_id, user_id, create_at FROM accounts", engine).to_dict('records')
    df_typ = pd.read_sql("SELECT transaction_type_id, t_name FROM transactions_types", engine)
    
    dict_signos = {"Deposit": 1, "Transfer In": 1, "Withdrawal": -1, "Payment": -1, "Transfer Out": -1, "Fee": -1}
    df_typ["signo"] = df_typ["t_name"].map(dict_signos)
    tipos_dict = df_typ.to_dict('records')
    
    montos = np.round(np.clip(np.random.lognormal(mean=4.0, sigma=1.5, size=NUM_TRANSACTIONS), 1.0, 999999.99), 2)
    
    txs = []
    for i in range(NUM_TRANSACTIONS):
        acc = random.choice(df_acc)
        typ = random.choice(tipos_dict)
        t_date = fake.date_time_between_dates(datetime_start=acc["create_at"])
        
        txs.append([
            int(acc["account_id"]), int(acc["user_id"]), int(typ["transaction_type_id"]), typ["t_name"], typ["signo"],
            float(montos[i]), int(acc["currency_id"]),
            np.random.choice(["COMPLETED", "PENDING", "FAILED", "REVERSED"], p=[0.85, 0.05, 0.08, 0.02]), t_date
        ])
        
    cols = ["account_id", "user_id", "transaction_type_id", "t_name", "signo", "amount", "currency_id", "t_status", "created_at"]
    df_tx_global = pd.DataFrame(txs, columns=cols)
    
    df_insert = df_tx_global[["account_id", "transaction_type_id", "amount", "currency_id", "t_status", "created_at"]]
    df_insert.to_sql("transactions", engine, if_exists="append", index=False, chunksize=15000)

def f_balances():
    df = df_tx_global[df_tx_global["t_status"] == "COMPLETED"].copy()
    df['impacto_real'] = df['amount'] * df['signo']
    
    balances = df.groupby('account_id')['impacto_real'].sum().reset_index()
    balances.rename(columns={'impacto_real': 'current_balance'}, inplace=True)
    balances['current_balance'] = np.round(balances['current_balance'], 2)
    
    df_todas = pd.read_sql("SELECT account_id FROM accounts", engine)
    final = pd.merge(df_todas, balances, on='account_id', how='left').fillna(0)
    final.to_sql("account_balances", engine, if_exists="append", index=False, chunksize=15000)

def f_auditoria_raw():
    audits, raws_tx, raws_ac = [], [], []
    for _ in range(int(NUM_TRANSACTIONS * 0.02)):
        audits.append([
            random.choice(["users", "accounts", "system_settings"])[:100], random.randint(1, NUM_USERS),
            random.choice(["UPDATE_KYC", "PASSWORD_RESET", "ACCOUNT_LOCKED"])[:50], random.randint(1, 50),
            fake.date_time_between("-1y", "now"), "OLD_STATE", "NEW_STATE"
        ])
    for _ in range(1000):
        raws_tx.append([json.dumps({"src": "API_EXT", "token": fake.uuid4()}), fake.date_time_between("-1M", "now")])
        raws_ac.append([json.dumps({"batch": fake.uuid4(), "status": "ok"}), fake.date_time_between("-1M", "now")])
        
    pd.DataFrame(audits, columns=["entity_name", "entity_id", "action", "performed_by", "performed_at", "old_value", "new_value"]).to_sql("audit_log", engine, if_exists="append", index=False, chunksize=15000)
    pd.DataFrame(raws_tx, columns=["raw_data", "insert_at"]).to_sql("transactions_raw", engine, if_exists="append", index=False)
    pd.DataFrame(raws_ac, columns=["raw_data", "insert_at"]).to_sql("accounts_raw", engine, if_exists="append", index=False)

def f_olap_snapshots():
    df = df_tx_global[df_tx_global["t_status"] == "COMPLETED"].copy()
    df['snapshot_date'] = df['created_at'].dt.date
    df['impacto_real'] = df['amount'] * df['signo']
    
    diario = df.groupby(['account_id', 'snapshot_date'])['impacto_real'].sum().reset_index()
    diario.sort_values(by=['account_id', 'snapshot_date'], inplace=True)
    
    diario['closing_balance'] = diario.groupby('account_id')['impacto_real'].cumsum()
    diario['closing_balance'] = np.round(diario['closing_balance'], 2)
    
    diario[['account_id', 'snapshot_date', 'closing_balance']].to_sql("daily_account_snapshots", engine, if_exists="append", index=False, chunksize=15000)

def f_olap_metrics():
    df = df_tx_global[df_tx_global["t_status"] == "COMPLETED"].copy()
    df['u_year_month'] = df['created_at'].dt.strftime('%Y-%m')
    
    mensual = df.groupby(['user_id', 'u_year_month']).agg(
        total_transactions=('amount', 'count'), total_volume=('amount', 'sum'), avg_transaction=('amount', 'mean')
    ).reset_index()
    
    mensual['total_volume'] = np.round(mensual['total_volume'], 2)
    mensual['avg_transaction'] = np.round(mensual['avg_transaction'], 2)
    mensual.to_sql("user_monthly_metrics", engine, if_exists="append", index=False, chunksize=15000)

# ==========================================
# 4. EJECUCIÓN ORDENADA
# ==========================================
pasos = [
    {"nombre": "Monedas", "fn": f_monedas}, {"nombre": "Tipos Transacción", "fn": f_tipos_transaccion},
    {"nombre": "Usuarios (KYC)", "fn": f_usuarios}, {"nombre": "Dispositivos (Logs)", "fn": f_dispositivos},
    {"nombre": "Cuentas Financieras", "fn": f_cuentas}, {"nombre": "Transacciones (Core)", "fn": f_transacciones},
    {"nombre": "Saldos Analíticos", "fn": f_balances}, {"nombre": "Auditoría y Data Raw", "fn": f_auditoria_raw},
    {"nombre": "OLAP: Snapshots Diarios", "fn": f_olap_snapshots}, {"nombre": "OLAP: Métricas Mes", "fn": f_olap_metrics}
]

print("\n🚀 INICIANDO MEGA-GENERADOR NEOBANK (BLINDADO)\n")
with tqdm(total=len(pasos), desc="Progreso ETL", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]") as pbar:
    for p in pasos:
        pbar.set_postfix_str(f"Procesando {p['nombre']}")
        start = time.time()
        try:
            p["fn"]()
            tqdm.write(f"✔ {p['nombre']} | {time.time()-start:.2f}s")
        except Exception as e:
            tqdm.write(f"❌ Fallo crítico en {p['nombre']}: {e}")
            break
        pbar.update(1)
print("\n✅ BASE DE DATOS POBLADA SIN ERRORES.")