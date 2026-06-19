# ⚙️ Pipeline ETL V2.0: Optimización y Escala

Motor de transformación diseñado para manejar un ecosistema bancario completo.

## 📊 Métricas de Generación (Data Scale)
| Entidad | Volumen | Descripción |
| :--- | :--- | :--- |
| **Usuarios** | 5,000 | Perfiles únicos con KYC activo. |
| **Monedas** | 9 | Catálogo multi-divisa (Fiat y Cripto). |
| **Dispositivos** | 8,000 | Trazabilidad de accesos (Móvil, Web, Desktop). |
| **Cuentas** | 7,000 | Segmentación (Savings, Checking, Credit). |
| **Transacciones** | 150,000 | Distribución log-normal para simulaciones realistas. |

## ⚡ Optimización Técnica
* **Procesamiento:** Implementación de `chunking` (lotes de 15,000) para eficiencia en memoria RAM.
* **Integridad:** Ejecución jerárquica de 10 niveles para eliminar fallos de claves foráneas.
* **Blindaje:** Validación de tipos en origen para evitar errores `1406 (Data too long)`.

## 🎓 ¿Qué demuestro en este proyecto?
1. **Dominio de ETL:** Transformación de datos sintéticos a modelos listos para Business Intelligence.
2. **Ingeniería de Datos:** Gestión de entornos, orquestación y orquestación de bases de datos.
3. **Calidad de Datos:** Enfoque técnico en integridad referencial y ACID como pilares de sistemas financieros.