# SPEC006: Documentation Internationalization Strategy

## Context

The OntoBDC documentation requires support for multiple languages (English, Portuguese, Spanish) with a specific URL structure preference:
- **Root (`/`)**: Should act as a router/redirector based on user browser language.
- **English (`/en/`)**: Explicit path for English content.
- **Portuguese (`/pt/`)**: Explicit path for Portuguese content.
- **Spanish (`/es/`)**: Explicit path for Spanish content.

Standard configuration of `mkdocs-static-i18n` forces the **default language** to be served at the root (`/`), which conflicts with the requirement of having English content isolated at `/en/`.

## The Challenge

When `docs_structure: folder` is used:
1.  One language must be marked as `default: true`.
2.  The content of the default language is moved to the root (`site/`) during the build.
3.  Non-default languages are built into their respective subdirectories (`site/pt/`, `site/es/`).

If English is set as default, it occupies `/`, making `/en/` a 404 error. If English is set as non-default, no language occupies `/`, potentially causing 404s at the root unless a separate strategy is employed.

## The Solution: "Redirect-as-Default" Pattern

To achieve the desired structure, we implement a "fake" default language responsible solely for redirection.

### 1. Language Configuration

We introduce a utility locale (`en_US`) to serve as the default, while keeping the actual English content (`en`) as a secondary language.

**`mkdocs.yml`**:
```yaml
plugins:
  - i18n:
      docs_structure: folder
      languages:
        - locale: en      # Actual English content
          name: English
          default: false  # Builds to /en/
        - locale: pt
          name: Português
        - locale: es
          name: Español
        - locale: en_US   # Redirector
          name: Redirect
          default: true   # Builds to /
          build: true
```

### 2. Root Redirection Script

The content for the `en_US` locale (located at `page/docs/en_US/index.md`) contains only a client-side redirection script:

```html
<script>
  var lang = navigator.language || navigator.userLanguage;
  if (lang.startsWith('pt')) {
    window.location.href = "./pt/";
  } else if (lang.startsWith('es')) {
    window.location.href = "./es/";
  } else {
    window.location.href = "./en/";
  }
</script>
```

### 3. Theme Override for Utility Locale

The *Material for MkDocs* theme attempts to load translation assets based on the locale code. Since `en_US` is treated as a distinct locale but shares the English base, the theme fails to find `partials/languages/en_US.html`.

To fix this, we implement a template override that proxies the macros from the standard `en` template.

**File**: `page/overrides/partials/languages/en_US.html`
```jinja2
{% import "partials/languages/en.html" as en %}
{% macro t(key) %}{{ en.t(key) }}{% endmacro %}
```

This ensures that the build process for the root redirector does not crash due to missing Jinja2 macros (`t` function).

## Resulting Structure

| URL Path | Content | Source |
|----------|---------|--------|
| `/` | Redirection Script | `docs/en_US/index.md` |
| `/en/` | English Docs | `docs/en/index.md` |
| `/pt/` | Portuguese Docs | `docs/pt/index.md` |
| `/es/` | Spanish Docs | `docs/es/index.md` |

This strategy successfully decouples the "default language" concept from the "English content" concept, satisfying the routing requirements.
