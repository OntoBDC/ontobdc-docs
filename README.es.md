# 🚀 OntoBDC (Ontology-Based Data Capabilities)

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/OntoBDC/ontobdc-core/blob/main/LICENSE) [![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/) [![RO-Crate](https://img.shields.io/badge/RO--Crate-1.1-green)](https://www.researchobject.org/ro-crate/) [![Status](https://img.shields.io/badge/status-active-success)](https://github.com/OntoBDC)

**OntoBDC** (Ontology-Based Data Capabilities) es una arquitectura orientada al dominio y un runtime de capacidades para ejecutar operaciones de datos con conciencia ontológica sobre conjuntos de datos portátiles.

Cuando los datos se describen con **RO-Crate**, se vuelven auto-descriptivos. OntoBDC aprovecha esta metadata para descubrir y ejecutar automáticamente operaciones relevantes al contexto.

Usa OntoBDC para gestionar el ciclo de vida de proyectos de datos de ingeniería. El runtime orquesta **L1 Queries** (Descubrimiento), **L2 Actions** (Transformación) y **L3 Use Cases** (Transiciones de estado) para proporcionar flujos reproducibles y auditables.

**Contenido**

- [Enfoque del proyecto](#enfoque-del-proyecto)
- [Principios](#principios)
- [Arquitectura](#arquitectura)
- [Capacidades](#capacidades)
- [Primeros pasos](#primeros-pasos)
- [Entity Framework](#entity-framework)
- [Enlaces útiles](#enlaces-útiles)
- [Código abierto](#código-abierto)
- [Contribuir](#contribuir)
- [¿Quién usa OntoBDC?](#quién-usa-ontobdc)

## Enfoque del proyecto

OntoBDC funciona mejor con **proyectos de datos portátiles y descentralizados**. En lugar de bloquear los datos en sistemas monolíticos, OntoBDC asume que los datos viven en paquetes portátiles (Zip/Carpeta/Almacenamiento local) que pueden moverse entre entornos sin perder significado semántico ni capacidad operacional.

## Principios

- **Semántico**: Los datos tienen significado definido por ontologías y metadata (RO-Crate).
- **Modular**: Queries/Actions son plugins aislados. Puedes agregar nuevas operaciones sin cambiar el núcleo.
- **Portátil**: Ejecuta en laptop, servidor o contenedor.

## Arquitectura

OntoBDC se apoya en una capa semántica central:

1. **Context Layer**: [RO-Crate](https://www.researchobject.org/ro-crate/) para metadata y relaciones.

El **Capability Runtime** conecta estas capas y resuelve dinámicamente qué estrategias de CLI aplican al estado actual.

## Capacidades

| Nivel | Nombre | Alcance y poder | ¿Efectos secundarios? | Ejemplo |
| :--- | :--- | :--- | :--- | :--- |
| **L1** | **Query** | **Solo lectura / Descubrimiento.** Interfaz para consultar el entorno. | **NO.** Debe ser idempotente y segura para reintentos. | `list_documents`, `get_file_content`, `check_syntax`. |
| **L2** | **Action** | **Transformación / Creación.** Produce nuevos datos/archivos sin cambiar la lógica de estado. | **Solo local.** Puede crear/escribir archivos sin avanzar estado. | `unzip_file`, `convert_pdf_to_png`, `generate_ro_crate_json`. |
| **L3** | **Use Case** | **Transición de estado.** Orquesta L1 y L2 para avanzar el proceso. | **SÍ.** Cambia la “verdad” del sistema. | `process_chat_folder`, `publish_dataset`. |

## Primeros pasos

Requiere Python 3.11+ y pip:

```bash
pip install ontobdc
```

Inicializa el contexto del proyecto:

```bash
ontobdc init
```

Ejecuta queries/capacidades de forma interactiva:

```bash
ontobdc run
```

Valida los datos y aplica reparaciones cuando sea posible:

```bash
ontobdc check --repair
```

## Entity Framework

Entity Framework es una estructura local para gestionar **Entities** (ELOFs) y sus archivos de fachada ontológica en `.__ontobdc__/ontology/entity/`, indexados por `.__ontobdc__/entity.rdf`.

Habilitar:

```bash
ontobdc entity --enable true
```

Crear y listar:

```bash
ontobdc entity --create org.example.my_entity
ontobdc entity --list
```

Deshabilitar y limpiar todo:

```bash
ontobdc entity --enable false
ontobdc entity --purge
```

## Enlaces útiles

| Recurso | Link |
|----------|------|
| 📘 Documentación | <a href="https://docs.ontobdc.org" target="_blank">docs.ontobdc.org</a> |
| 🐙 GitHub | <a href="https://github.com/OntoBDC" target="_blank">github.com/OntoBDC</a> |
| 📦 PyPI | <a href="https://pypi.org/project/ontobdc" target="_blank">pypi.org/project/ontobdc</a> |

## Código abierto

OntoBDC es open-source bajo licencia **Apache 2.0**.

## Contribuir

Contribuciones vía PRs e issues en GitHub son bienvenidas.

## ¿Quién usa OntoBDC?

OntoBDC es el núcleo de **InfoBIM**, impulsando interoperabilidad semántica para proyectos complejos de ingeniería.

---
<p align="center">Proudly developed in Brazil 🇧🇷</p>
