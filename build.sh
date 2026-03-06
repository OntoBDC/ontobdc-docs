#!/bin/bash
set -e

# Configuration
PAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_SRC="${PAGE_DIR}/../ontobdc-wip/docs"
DOCS_DEST="${PAGE_DIR}/docs"

echo "Building documentation..."
echo "Source: ${DOCS_SRC}"
echo "Destination: ${DOCS_DEST}"

# Clean destination (but keep assets if needed, here we clean all)
rm -rf "${DOCS_DEST}"
mkdir -p "${DOCS_DEST}"

# Copy documentation
cp -r "${DOCS_SRC}/"* "${DOCS_DEST}/"

# Ensure index.md exists
if [ ! -f "${DOCS_DEST}/index.md" ]; then
    echo "# OntoBDC Documentation" > "${DOCS_DEST}/index.md"
    echo "Welcome to OntoBDC documentation." >> "${DOCS_DEST}/index.md"
fi

# You can add dynamic generation scripts here
# Example: Generate CLI reference

echo "Documentation content updated successfully."
