# Arquitectura del Modelo de Datos

Diseño lógico normalizado en 3FN (Tercera Forma Normal) para garantizar la integridad referencial y la consistencia en el ecosistema de datos.



[Image of relational database entity relationship diagram]


## Estructura de Capas

La arquitectura se segmenta funcionalmente para optimizar la trazabilidad y el mantenimiento:

| Capa | Tablas | Descripción |
| :--- | :--- | :--- |
| **Core** | `users`, `devices` | Gestión de identidad y control de acceso (KYC). |
| **Transactional** | `accounts`, `transactions` | Operaciones financieras con integridad estricta. |
| **Audit/Raw** | `audit_log`, `raw_data` | Registro de eventos críticos y persistencia externa. |

---

## Especificaciones de Diseño

### Implementación Técnica
* **Motor de Almacenamiento:** Uso de `InnoDB` para soporte completo de transacciones ACID, garantizando fiabilidad ante fallos.
* **Integridad Referencial:** Implementación de claves foráneas (`FOREIGN KEY`) con políticas `ON DELETE RESTRICT` para evitar transacciones huérfanas y preservar la lógica financiera.
* **Consistencia:** Definición de restricciones `UNIQUE` en campos críticos (como `email` y `codigo_iso`) para prevenir duplicidad de entidades.

### Filosofía del Esquema
El diseño prioriza el desacoplamiento de las entidades maestras respecto a los eventos transaccionales, lo que permite una escalabilidad vertical y horizontal eficiente al integrar nuevos servicios o catálogos sin comprometer la base de datos central.

---
[Volver al README principal](../README.md)
