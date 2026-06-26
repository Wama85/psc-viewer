import os
import io
import re
import json

from flask import Flask, render_template, request, redirect, session, url_for
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = Flask(__name__)
app.secret_key = "code_viewer_clave_segura_123"

# Local:
BASE_PATH = ""

# En cPanel, si tu app está en /codeviewer, usa:
# BASE_PATH = "/codeviewer"

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
CLIENT_SECRETS_FILE = "credentials.json"


@app.route("/")
def inicio():
    conectado = "credentials" in session

    return render_template(
        "inicio.html",
        conectado=conectado,
        login_url=f"{BASE_PATH}/login",
        viewer_url=f"{BASE_PATH}/viewer",
        base_path=BASE_PATH
    )


@app.route("/login")
def login():
    redirect_uri = url_for("oauth2callback", _external=True)

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )

    session["state"] = state
    session["code_verifier"] = flow.code_verifier

    return redirect(authorization_url)


@app.route("/oauth2callback")
def oauth2callback():
    redirect_uri = url_for("oauth2callback", _external=True)

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=session.get("state"),
        redirect_uri=redirect_uri
    )

    flow.code_verifier = session.get("code_verifier")
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    session["credentials"] = credentials_to_dict(credentials)

    return redirect(f"{BASE_PATH}/viewer")


@app.route("/viewer")
def viewer():
    if "credentials" not in session:
        return redirect(f"{BASE_PATH}/login")

    entrada = request.args.get("url") or request.args.get("fileId")
    file_id = None

    if entrada:
        file_id = extraer_file_id(entrada)

    state = request.args.get("state")

    if state:
        try:
            state_data = json.loads(state)
            ids = state_data.get("ids", [])

            if ids:
                file_id = ids[0]

        except Exception as e:
            print("Error leyendo state:", e)

    nombre_usuario = "usuario"
    nombre_archivo = ""
    codigo = ""
    lenguaje = "txt"
    mensaje = "Bienvenido. Pega una URL de Google Drive™ y presiona Mostrar."

    credentials = Credentials(**session["credentials"])
    service = build("drive", "v3", credentials=credentials)

    try:
        about = service.about().get(
            fields="user(displayName,emailAddress)"
        ).execute()

        user = about.get("user", {})
        nombre_usuario = (
            user.get("displayName")
            or user.get("emailAddress")
            or "usuario"
        )

    except Exception:
        pass

    if file_id:
        try:
            metadata = service.files().get(
                fileId=file_id,
                fields="name,mimeType"
            ).execute()

            nombre_archivo = metadata.get("name", "archivo")
            codigo = descargar_archivo_drive(service, file_id)
            lenguaje = detectar_lenguaje(nombre_archivo)
            mensaje = None

            session["credentials"] = credentials_to_dict(credentials)

        except Exception as e:
            mensaje = f"No se pudo leer el archivo: {str(e)}"

    return render_template(
        "viewer.html",
        nombre_usuario=nombre_usuario,
        nombre_archivo=nombre_archivo,
        codigo=codigo,
        lenguaje=lenguaje,
        mensaje=mensaje,
        base_path=BASE_PATH
    )


def extraer_file_id(valor):
    if not valor:
        return None

    if "/" not in valor and "http" not in valor:
        return valor

    patrones = [
        r"/file/d/([a-zA-Z0-9_-]+)",
        r"id=([a-zA-Z0-9_-]+)"
    ]

    for patron in patrones:
        match = re.search(patron, valor)

        if match:
            return match.group(1)

    return None


def descargar_archivo_drive(service, file_id):
    request_drive = service.files().get_media(fileId=file_id)
    archivo_memoria = io.BytesIO()

    downloader = MediaIoBaseDownload(archivo_memoria, request_drive)

    terminado = False

    while not terminado:
        status, terminado = downloader.next_chunk()

    contenido_bytes = archivo_memoria.getvalue()

    return decodificar_texto(contenido_bytes)


def decodificar_texto(contenido_bytes):
    codificaciones = [
        "utf-8",
        "utf-8-sig",
        "cp1252",
        "latin-1"
    ]

    for codificacion in codificaciones:
        try:
            return contenido_bytes.decode(codificacion)
        except UnicodeDecodeError:
            pass

    return contenido_bytes.decode("latin-1", errors="replace")


def detectar_lenguaje(nombre_archivo):
    nombre = nombre_archivo.lower()

    if nombre.endswith(".psc"):
        return "psc"

    if nombre.endswith((".cpp", ".cxx", ".cc", ".hpp", ".h")):
        return "cpp"

    if nombre.endswith(".c"):
        return "c"

    if nombre.endswith(".py"):
        return "python"

    if nombre.endswith(".java"):
        return "java"

    if nombre.endswith(".js"):
        return "javascript"

    if nombre.endswith(".html") or nombre.endswith(".htm"):
        return "html"

    if nombre.endswith(".css"):
        return "css"

    if nombre.endswith(".php"):
        return "php"

    if nombre.endswith(".sql"):
        return "sql"

    if nombre.endswith(".json"):
        return "json"

    if nombre.endswith(".xml"):
        return "xml"

    if nombre.endswith(".txt"):
        return "txt"

    return "txt"


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )