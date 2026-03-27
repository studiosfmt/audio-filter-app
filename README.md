# 🔊 Audio Filter App - Deployment Guide

Este proyecto está listo para ser desplegado en **Streamlit Community Cloud**. Sigue estos pasos:

## 🚀 Pasos para el Despliegue

1.  **Sube el código a GitHub**: Crea un repositorio (puedes llamarlo `audio-filter-app`) y sube todos los archivos de esta carpeta.
2.  **Inicia sesión en Streamlit Cloud**: Ve a [share.streamlit.io](https://share.streamlit.io/) e inicia sesión con tu cuenta de GitHub.
3.  **Crea una nueva App**:
    *   Haz clic en el botón **"New app"**.
    *   Selecciona tu repositorio: `tu-usuario/audio-filter-app`.
    *   Rama (Main file path): `app.py`.
4.  **¡Despliega!**: Haz clic en **"Deploy!"**. Streamlit instalará automáticamente las librerías de `requirements.txt` y los paquetes de sistema en `packages.txt`.

## 🛠️ Notas de Configuración
- El archivo `.streamlit/config.toml` ya contiene el tema visual oscuro para que se vea profesional desde el primer momento.
- `packages.txt` asegura que las librerías de procesamiento de audio funcionen correctamente en el servidor.

---
*Desarrollado con ❤️ para el procesamiento de audio.*
