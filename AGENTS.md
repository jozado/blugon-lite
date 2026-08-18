## Imágenes
Nunca llames `read` sobre archivos de imagen (*.png, *.jpg, *.jpeg, *.gif, *.webp, *.svg).
Si una tarea requiere ver una imagen, delega el análisis al subagente `vision-analyst`
con la herramienta `task` (subagent_type: vision-analyst) pasándole la ruta exacta del archivo.
Si `vision-analyst` falla por error de conexión del modelo, reintenta la misma tarea con
el subagente de respaldo `vision-analyst-fallback` (subagent_type: vision-analyst-fallback).

## Idioma / Language
El usuario se comunica en español: respóndele siempre en español.
Redacta en español todas las preguntas e interacciones con el usuario (la herramienta `question`, las decision pages de serve-question, confirmaciones y respuestas).

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
  - NOT worth running: changes inside folders listed in `.graphifyignore` (they produce zero nodes, so `graphify update` reports "No code-graph topology changes").
