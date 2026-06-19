Markdown
---

### 2. `SCHEMA/README.md`
*Aquí explicas la estructura con profundidad técnica.*

```markdown
# 📐 Arquitectura de Datos: Normalización y Relaciones

El esquema está diseñado bajo un modelo de **Normalización 3FN** para eliminar redundancias y garantizar la consistencia financiera.



### Estructura de Capas
* **Core Layer:** Gestión de usuarios y dispositivos con control de identidad (KYC).
* **Transactional Layer:** Tablas `accounts` y `transactions` con restricciones `ON DELETE RESTRICT`, blindando la trazabilidad de fondos.
* **Audit/Raw Layer:** Sistema de auditoría (`audit_log`) y almacenamiento de datos crudos (`raw_data`) para trazabilidad de eventos externos.

### Decisiones de Diseño
* **Motores:** Uso de `InnoDB` para soporte de transacciones ACID.
* **Constraints:** Implementación de `UNIQUE` y `FOREIGN KEY` estratégicas para asegurar la integridad referencial en toda la base de datos.
