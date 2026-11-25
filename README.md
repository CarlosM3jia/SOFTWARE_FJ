# SOFTWARE_FJ

Sistema integral de gestión de clientes, servicios y reservas para **Software FJ**.
Proyecto de la Fase 4 del curso Programación (213023) – UNAD.

Aplicación en Python orientada a objetos, **sin bases de datos**: los datos viven en
objetos y listas en memoria; los archivos se usan solo para el registro de eventos y errores.

## Ejecución

```bash
python main.py
```

Simula 15 operaciones (válidas e inválidas) y escribe todo en `logs/software_fj.log`.

Pruebas:
- `python pruebas/pruebas_generales.py` (sistema completo)
- `python -m pruebas.pruebas_clientes`, `python -m pruebas.pruebas_servicios` y `python -m pruebas.pruebas_reservas` (por módulo)

## Estructura

| Carpeta / archivo | Contenido |
|---|---|
| `main.py` | Integra los tres módulos y simula 15 operaciones |
| `modelos/` | `Entidad` (abstracta), `Cliente`, `GestorClientes` |
| `servicios/` | `Servicio` (abstracta), `ReservaSala`, `AlquilerEquipos`, `AsesoriaEspecializada` |
| `reservas/` | `Reserva` (confirmar, cancelar y calcular costo) y sus excepciones |
| `excepciones/` | Excepciones personalizadas de clientes |
| `utilidades/` | Logger que escribe en `logs/software_fj.log` |
| `pruebas/` | Pruebas generales y por módulo |
| `logs/` | Archivo de logs generado por la ejecución |

## Conceptos aplicados

- **Abstracción:** `Entidad` y `Servicio` son clases abstractas.
- **Herencia:** `Cliente` hereda de `Entidad`; los tres servicios heredan de `Servicio`.
- **Polimorfismo:** cada servicio sobrescribe `calcular_costo` y `obtener_descripcion`; la reserva los usa sin saber de qué tipo es el servicio.
- **Encapsulación:** atributos privados con propiedades y validaciones en `Cliente`.
- **Sobrecarga simulada:** parámetros opcionales (descuento, impuesto, seguro, bono).
- **Excepciones:** personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from ...`.

## Integrantes

- Carlos Mario Mejia Floréz
- Luis Carlos Salazar
- Kevin Duvan
- Karen Martínez
