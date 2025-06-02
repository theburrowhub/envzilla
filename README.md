# envzilla

Envzilla es una herramienta de línea de comandos para administrar archivos `.env` de forma sencilla. Permite organizar, actualizar y cambiar entre diferentes configuraciones de entorno.

## Requisitos
- Python 3.11
- [uv](https://github.com/astral-sh/uv) para la gestión de paquetes

## Instalación rápida

```bash
make install
```

El comando anterior crea un entorno virtual en `.venv`, instala `uv` y todas las dependencias del proyecto en modo editable.

## Uso

Para ejecutar la herramienta desde el entorno virtual:

```bash
make run
```

### Comandos disponibles

Por ahora existe el comando `list`, que compara un archivo de plantilla
(por defecto `.env.dist` o `.env.template`) con el resto de archivos `.env`
del directorio y muestra una tabla con el estado de cada variable.
Se puede usar `--only-missing` para mostrar solo las variables que faltan o
que no tienen valor.

## Ejecutar pruebas

```bash
make test
```

## Colaborar
1. Haz un fork del repositorio y clona tu copia.
2. Crea una rama para tus cambios.
3. Ejecuta `make install` para preparar el entorno.
4. Realiza tus modificaciones y añade pruebas si es necesario.
5. Asegúrate de que `make test` se ejecuta sin errores.
6. Envía un pull request con una descripción clara de tus cambios.

Cualquier duda o mejora es bienvenida.
