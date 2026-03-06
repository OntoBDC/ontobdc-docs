# 🚀 OntoBDC (Ontology-Based Data Capabilities)

| Categoría  | Badges |
|------------|--------|
| Licencia   | [![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE) |
| Python     | [![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/) |
| Estándares | [![Frictionless](https://img.shields.io/badge/frictionless-data-black)](https://frictionlessdata.io/) [![RO-Crate](https://img.shields.io/badge/RO--Crate-1.1-green)](https://www.researchobject.org/ro-crate/) |
| Estado     | [![Sismic](https://img.shields.io/badge/statecharts-sismic-blue)](https://sismic.readthedocs.io/) |
| Estado     | [![Status](https://img.shields.io/badge/status-active-success)]() |

**OntoBDC** (Ontology-Based Data Capabilities) es un runtime orientado a capabilities para la ejecución de operaciones de datos conscientes de ontología en datasets portables. Cierra la brecha entre el almacenamiento de datos estático y la ejecución semántica dinámica.

Cuando los datos son descritos por **RO-Crate** y **Frictionless Data Packages**, se vuelven autodescriptivos. OntoBDC aprovecha estos metadatos para descubrir y ejecutar automáticamente **Capabilities** (operaciones) disponibles y relevantes para el contexto de los datos.

Use OntoBDC para gestionar el ciclo de vida de sus proyectos de datos. El runtime orquesta **L1 Capabilities** (Descubrimiento), **L2 Actions** (Transformación) y **L3 Use Cases** (Transiciones de Estado), manteniendo una columna vertebral rigurosa de **Event Sourcing** (System Crate).

**Índice**

- [Enfoque del Proyecto](#enfoque-del-proyecto)
- [Principios](#principios)
- [Arquitectura](#arquitectura)
- [Comenzando](#comenzando)
- [Instalación](#instalacion)
- [Enlaces Útiles](#enlaces-utiles)
- [Open Source](#open-source)
- [Contribuyendo](#contribuyendo)
- [¿Quién usa OntoBDC?](#quien-usa-ontobdc)

## 🎯 Enfoque del Proyecto

OntoBDC funciona mejor con **proyectos de datos descentralizados y portables**. A diferencia de los sistemas monolíticos que bloquean datos en bases de datos específicas, OntoBDC asume que los datos viven en paquetes portables (Zip/Carpeta/WEB/API/FTP) que pueden moverse entre almacenamiento local, nube y dispositivos de borde sin perder significado semántico o capacidad operativa.

OntoBDC se usa comúnmente para:

- **Estandarizar** el intercambio de datos entre diversas disciplinas de ingeniería (BIM, GIS, Documentos).
- **Ejecutar** operaciones conscientes del contexto (ej: "Extraer Entidades de PDF", "Validar Modelo IFC") sin pipelines hardcoded.
- **Rastrear** cada modificación en el historial de un proyecto a través de un registro de eventos inmutable (System Crate).

## 💡 Principios

- **Semántico**: Los datos no son solo bytes; tienen significado definido por ontologías y metadados (RO-Crate).
- **Modular**: Capabilities son plugins aislados. Puede agregar nuevas operaciones sin cambiar el runtime principal.
- **Portable**: Todo el runtime y el paquete de datos son independientes. Ejecute en una laptop, servidor o dentro de un contenedor.
- **Event-Sourced**: El estado se deriva de una secuencia de eventos, garantizando auditoría y depuración "time-travel".

## 🏗️ Arquitectura

OntoBDC se construye sobre tres pilares:

1.  **Capa Física**: [Frictionless Data Package](https://frictionlessdata.io/) para organización de archivos.
2.  **Capa de Contexto**: [RO-Crate](https://www.researchobject.org/ro-crate/) para metadados semánticos y relaciones.
3.  **Capa de Sistema**: **System Crate** para event sourcing y memoria operativa, implementando una **Máquina de Estados Finitos (FSM)** robusta.

El **Capability Runtime** une estas capas, resolviendo dinámicamente qué herramientas (estrategias CLI) se aplican al estado actual de los datos.

## ⚡ Capabilities

Capabilities son las unidades centrales de ejecución en OntoBDC. Se categorizan en tres niveles de poder y responsabilidad, garantizando seguridad y claridad para agentes autónomos:

| Nivel | Nombre | Alcance y Poder | ¿Efectos Secundarios? | Ejemplo |
| :--- | :--- | :--- | :--- | :--- |
| **L1** | **Capability** | **Solo Lectura / Descubrimiento.** Interfaz pura para consultar el entorno. | **NO.** Debe ser idempotente y segura para reintentar infinitas veces. | `list_documents`, `get_file_content`, `check_syntax`. |
| **L2** | **Action** | **Transformación / Creación.** Toma datos de entrada y produce nuevos datos/archivos sin cambiar la lógica de estado del negocio. | **Solo Local.** Puede crear/escribir archivos pero no avanza el estado del flujo de trabajo. | `unzip_file`, `convert_pdf_to_png`, `generate_ro_crate_json`. |
| **L3** | **Use Case** | **Transición de Estado.** Orquesta L1 y L2 para mover el proceso de negocios adelante. | **SÍ.** Cambia la "verdad" del sistema. | `process_chat_folder` (Bruto -> Procesado), `publish_dataset`. |

Esta estructura permite control granular sobre lo que un agente puede hacer, separando "sentir" (L1) de "hacer" (L2) y "decidir" (L3).

## 📦 Instalación

OntoBDC se despliega típicamente vía pip. Instálelo para comenzar a usar la CLI:

```bash
pip install ontobdc

# Después de la instalación, puede ejecutar la CLI así:
ontobdc --help
```

## 🔗 Enlaces Útiles

| Recurso | Enlace |
|----------|------|
| 📘 Documentación | <a href="https://docs.ontobdc.org" target="_blank">docs.ontobdc.org</a> |
| 🐙 GitHub | <a href="https://github.com/OntoBDC" target="_blank">github.com/OntoBDC</a> |
| 📦 PyPI | <a href="https://pypi.org/project/ontobdc" target="_blank">pypi.org/project/ontobdc</a> |

## ❤️ Open Source

OntoBDC es una iniciativa libre y de código abierto, licenciada bajo la **Licencia Apache 2.0**.
Creemos en el poder del desarrollo impulsado por la comunidad para resolver desafíos complejos de interoperabilidad de datos.

## 🤝 Contribuyendo

OntoBDC es una iniciativa abierta. ¡Las contribuciones son bienvenidas!

## 🏢 ¿Quién usa OntoBDC?

OntoBDC es el motor central detrás de **InfoBIM**, impulsando la interoperabilidad de datos semánticos para proyectos de ingeniería complejos.

---
<p align="center">Orgullosamente desarrollado en Brasil 🇧🇷</p>
