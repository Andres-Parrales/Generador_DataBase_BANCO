Markdown
# 🚀 NeoBank V2.0: Core Transaccional de Alto Rendimiento

Sistema de banca digital simulada construido para gestionar grandes volúmenes de datos transaccionales con integridad referencial estricta y analítica avanzada.

![Status](https://img.shields.io/badge/Status-Optimized-brightgreen)
![Dataset](https://img.shields.io/badge/Scale-150K+_Transactions-blue)
![Stack](https://img.shields.io/badge/Stack-Python|SQLAlchemy|MySQL-red)

## 📌 Resumen Ejecutivo
NeoBank V2.0 es un pipeline de ingeniería de datos diseñado para simular un entorno bancario real. El proyecto integra una **Capa Transaccional (OLTP)** blindada contra inconsistencias y una **Capa Analítica (OLAP)** para el reporte de métricas financieras.

## ⚡ Stack Tecnológico
* **Orquestación:** Python 3.x.
* **Persistencia:** MySQL 8.0 (InnoDB).
* **Transformación:** Pandas & NumPy para procesamiento vectorizado.
* **ORM:** SQLAlchemy (Gestión de sesiones y transacciones).
* **Fake Data:** Generación sintética de alta fidelidad con `Faker`.

## 🛠️ Despliegue Técnico
1. **Dependencias:** `pip install pandas sqlalchemy pymysql faker tqdm numpy`
2. **Setup DB:** Ejecuta `SOURCE SCHEMA/schema_db_bank.sql;` en MySQL.
3. **Configuración:** Edita `ETL/generador_DB_banco.py` con tus credenciales:
   ```python
   USER = "root"; PASSWORD = "tu_password"; DB = "BancoDB"
