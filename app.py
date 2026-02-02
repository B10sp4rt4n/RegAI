import os, json, time, pandas as pd, streamlit as st
from db import init_db, create_project, list_projects, create_session, list_sessions, add_message, get_messages

st.set_page_config(page_title="Chatbot Studio Personal", page_icon="🤖", layout="wide")
st.title("🤖 Chatbot Studio Personal — Proyectos y Prompts")

# ---- DB init (one time) ----
if not os.path.exists("chatbot_studio.sqlite"):
    init_db("schema.sql")

# ---- Sidebar: Config ----
st.sidebar.header("Configuración")
api_key = st.sidebar.text_input("OpenAI API Key", type="password", help="Se recomienda usar variable de entorno OPENAI_API_KEY.")
if not api_key:
    api_key = os.environ.get("OPENAI_API_KEY", "")

model = st.sidebar.text_input("Modelo", value="gpt-5")
temperature = st.sidebar.slider("Creatividad (temperature)", 0.0, 1.0, 0.2, 0.05)
reasoning_effort = st.sidebar.select_slider("Esfuerzo de razonamiento", options=["low","medium","high"], value="medium")

st.sidebar.caption("Tip: Guarda tu API key en OPENAI_API_KEY para no escribirla cada vez.")

# ---- Projects ----
st.subheader("1) Proyectos")
with st.form("new_project"):
    name = st.text_input("Nombre del proyecto", placeholder="Mi chatbot personal / Asistente ventas / Soporte interno")
    desc = st.text_area("Descripción", placeholder="Objetivo, tono, público, límites…")
    submitted = st.form_submit_button("Crear proyecto")
    if submitted and name:
        p = create_project(name, desc)
        st.success(f"Proyecto creado: {p['name']}")

projects = list_projects()
if not projects:
    st.info("Crea tu primer proyecto arriba.")
    st.stop()

proj_choice = st.selectbox("Selecciona proyecto", [f"{p['id']} — {p['name']}" for p in projects])
project_id = int(proj_choice.split(" — ")[0])

# ---- Sessions ----
st.subheader("2) Conversaciones")
with st.form("new_session"):
    title = st.text_input("Título de la conversación", placeholder="Exploración inicial / Pruebas de tono / FAQs")
    s_sub = st.form_submit_button("Crear conversación")
    if s_sub and title:
        s = create_session(project_id, title)
        st.success(f"Creada conversación: {s['title']} (id {s['id']})")

sessions = list_sessions(project_id)
if not sessions:
    st.info("Crea una conversación arriba.")
    st.stop()

sess_choice = st.selectbox("Selecciona conversación", [f"{s['id']} — {s['title']}" for s in sessions])
session_id = int(sess_choice.split(" — ")[0])

# ---- Prompt box ----
st.subheader("3) Prompt")
sys_role = st.text_area("System (opcional)", placeholder="Define reglas del chatbot, tono o políticas.", height=80)
user_prompt = st.text_area("User", placeholder="Escribe tu prompt para este chatbot.", height=160)

colA, colB = st.columns(2)
anonymize = colA.checkbox("Anonimizar (emails/teléfonos)", value=True)
save_only = colB.checkbox("Solo guardar (no enviar a LLM)", value=False)

def sanitize(txt: str) -> str:
    import re
    txt = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[REDACTED_EMAIL]", txt)
    txt = re.sub(r"\b\+?\d[\d\s\-().]{7,}\b", "[REDACTED_PHONE]", txt)
    return txt

if st.button("➤ Enviar / Guardar turno"):
    if sys_role.strip():
        add_message(session_id, "system", sys_role, {"kind":"role"})
    text_to_send = sanitize(user_prompt) if anonymize else user_prompt
    add_message(session_id, "user", text_to_send, {"temperature": temperature, "reasoning_effort": reasoning_effort})

    if not save_only:
        if not api_key:
            st.error("Falta OpenAI API Key. Configúrala en la barra lateral o en OPENAI_API_KEY.")
        else:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                t0 = time.time()
                resp = client.responses.create(
                    model=model,
                    input=text_to_send if not sys_role else f"SYSTEM:\n{sys_role}\n\nUSER:\n{text_to_send}",
                    temperature=temperature,
                    reasoning={"effort": reasoning_effort},
                )
                assistant_text = resp.output_text
                latency_ms = int((time.time() - t0)*1000)
                add_message(session_id, "assistant", assistant_text, {"model": model, "latency_ms": latency_ms})
                st.success("Respuesta recibida y guardada.")
            except Exception as e:
                st.error(f"Error llamando al modelo: {e}")

# ---- History ----
st.subheader("4) Historial")
rows = get_messages(session_id)
if rows:
    import pandas as pd
    df = pd.DataFrame([{
        "id": r["id"],
        "role": r["role"],
        "content": r["content"],
        "created_at": r["created_at"]
    } for r in rows])
    st.dataframe(df, use_container_width=True, height=320)

    # Export JSONL
    jsonl = "\n".join(json.dumps({"role": r["role"], "content": r["content"]}, ensure_ascii=False) for r in rows)
    st.download_button("Exportar JSONL", data=jsonl.encode("utf-8"), file_name=f"session_{session_id}.jsonl", mime="application/jsonl")
else:
    st.info("Sin mensajes todavía.")

st.caption("Tip: Usa 'Solo guardar' para preparar prompts sin gastar tokens; luego desmarca para probarlos.")