# Product Guidelines

## Estilo de Prosa y Documentación

- **Claridad ante todo**: La documentación debe ser concisa y directa
- **Ejemplos prácticos**: Incluir ejemplos de uso real en README
- **Comentarios mínimos**: El código debe ser autoexplicativo; solo comentar lógica compleja
- **Idioma**: Documentación en inglés para alcance global, comentarios en código en inglés

## Principios de Diseño

### Minimalismo Funcional
- Cada línea de código debe tener un propósito claro
- Eliminar duplicación y código muerto
- Preferir funciones pequeñas y específicas

### Compatibilidad
- Mantener compatibilidad con configuraciones existentes de blugon
- Los archivos gamma y config deben funcionar sin modificaciones
- Preservar la interfaz de línea de comandos para opciones soportadas

### Rendimiento
- Priorizar uso eficiente de memoria (< 8MB RAM)
- Minimizar llamadas al sistema
- Evitar dependencias innecesarias

## Principios de UX (Experiencia de Usuario)

### CLI First
- Mensajes de error claros y accionables
- Salida silenciosa por defecto (sin output innecesario)
- Códigos de salida significativos para scripting

### Configuración Sensata
- Valores por defecto que funcionen para la mayoría
- Documentación clara de opciones de configuración
- Ejemplos de configuración incluidos

## Estándares de Calidad

### Código
- Seguir PEP 8 para Python
- Backends en C deben seguir estándares de C moderno
- Nombres descriptivos para variables y funciones

### Testing
- Verificar funcionalidad básica manualmente
- Probar con diferentes configuraciones gamma
- Validar consumo de memoria

### Versionado
- Seguir versionado semántico (MAJOR.MINOR.PATCH)
- Documentar cambios en cada versión
- Mantener changelog

## Mantenibilidad

### Estructura del Código
- Separación clara entre lógica principal y backends
- Funciones puras cuando sea posible
- Manejo explícito de errores

### Documentación Técnica
- README debe incluir instalación, uso y ejemplos
- Comentar decisiones arquitectónicas importantes
- Mantener actualizada la página de manual (man page)
