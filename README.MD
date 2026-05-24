# PSC Viewer

Visor online para archivos `.psc` de PSeInt usando Python + Flask y Google Drive API.

Permite:

- Abrir archivos `.psc` directamente desde Google Drive.
- Mostrar pseudocódigo sin descargar el archivo.
- Resaltar sintaxis automáticamente.
- Integrarse posteriormente con Google Classroom y Google Workspace Marketplace.

---

# Vista previa

El usuario pega una URL de Google Drive:

```txt
https://drive.google.com/file/d/FILE_ID/view
```

Y el sistema:

1. Extrae el `fileId`
2. Descarga el archivo desde Google Drive
3. Renderiza el contenido online

---

# Tecnologías

- Python
- Flask
- Google Drive API
- OAuth 2.0
- HTML
- CSS
- JavaScript

---

# Estructura del proyecto

```txt
psc-viewer/
│
├── app.py
├── requirements.txt
├── credentials.json
├── .gitignore
│
├── templates/
│   └── viewer.html
│
└── static/
    └── style.css
```

---

# Instalación

## 1. Clonar proyecto

```bash
git clone https://github.com/TU_USUARIO/psc-viewer.git
```

---

## 2. Entrar a la carpeta

```bash
cd psc-viewer
```

---

## 3. Crear entorno virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Configuración Google Cloud

## 1. Crear proyecto

Ir a:

https://console.cloud.google.com/

---

## 2. Activar APIs

Activar:

- Google Drive API

---

## 3. Crear OAuth Client ID

Tipo:

```txt
Web application
```

---

## 4. Configurar URLs

### Authorized JavaScript origins

```txt
http://127.0.0.1:5000
```

### Authorized redirect URIs

```txt
http://127.0.0.1:5000/oauth2callback
```

---

## 5. Descargar credenciales

Descargar:

```txt
credentials.json
```

y colocarlo en la raíz del proyecto.

---

# Usuarios de prueba

En:

```txt
OAuth consent screen
```

Agregar los correos permitidos para pruebas.

---

# Ejecutar proyecto

```bash
python app.py
```

Abrir:

```txt
http://127.0.0.1:5000
```

---

# Cómo usar

1. Iniciar sesión con Google.
2. Copiar URL del archivo `.psc` desde Google Drive.
3. Pegar URL.
4. Presionar:

```txt
Mostrar
```

---

# Ejemplo de URL válida

```txt
https://drive.google.com/file/d/1xvjQzOSeyAWBQCk7ZNbUrpra6Mpo8t0b/view
```

---

# Características actuales

- Login Google OAuth
- Lectura de archivos desde Drive
- Syntax Highlight
- Soporte UTF-8 y Latin-1
- Interfaz web

---

# Próximas mejoras

- Numeración de líneas
- Editor tipo VSCode
- Tema oscuro/claro
- Integración con Google Classroom
- Marketplace Google Workspace
- Conversor PSC → Python
- Ejecución online
- IA para análisis de pseudocódigo

---

# Licencia

MIT License