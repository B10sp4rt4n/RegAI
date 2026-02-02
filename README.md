# RegAI

> **Convierte las interacciones IA-humano en activos organizacionales auditables y reutilizables.**

RegAI es un sistema de memoria conversacional para equipos que trabajan con IA. A diferencia de ChatGPT o Claude donde las conversaciones se pierden, RegAI las convierte en conocimiento estructurado, inmutable y compartido.

---

## 🎯 Propuesta de Valor

| Característica | Beneficio |
|----------------|-----------|
| **Inmutabilidad** | Registro auditable que no se puede manipular. Compliance, legal, trazabilidad. |
| **Multiparticipante** | Los proyectos son del equipo, no de individuos. Conversaciones colaborativas con IA. |
| **Reconstrucción de contexto** | Meses después puedes entender POR QUÉ se tomaron decisiones. La IA retoma donde quedó. |
| **Consolidación de valor** | Las mejores interacciones no se pierden. Son activos de la organización. |

---

## 💡 Casos de Uso

- **Desarrollo de producto** — PM, diseñador y dev conversan CON la IA como participante
- **Due diligence** — "¿Cómo llegaron a esta decisión?" → Lee las conversaciones
- **Auditorías de IA** — Reguladores ven el proceso, no solo el resultado
- **Onboarding** — Nuevo empleado lee conversaciones pasadas, entiende contexto en horas
- **Propiedad intelectual** — Ideas generadas con IA documentadas y fechadas

---

## 🏗️ Arquitectura

```
Proyecto (ej: "Rediseño sistema de pagos")
│
├── Conversación: "Arquitectura inicial" (inmutable)
│   └── N turnos IA-humano → Decisiones documentadas
│
├── Conversación: "Revisión de seguridad" (inmutable)
│   └── N turnos → Vulnerabilidades identificadas
│
└── Conversación: "Sprint actual" (activa)
    └── La IA puede leer TODO el contexto anterior
```

---

## ⚡ Características Actuales

- ✅ Gestión de proyectos y conversaciones
- ✅ Persistencia en SQLite
- ✅ Anonimización automática (emails, teléfonos)
- ✅ Configuración de modelo, temperatura, reasoning effort
- ✅ System prompts personalizables
- ✅ Exportación a JSONL
- ✅ Modo "solo guardar" para preparar sin gastar tokens
- ✅ Historial completo visualizable

---

## 🚀 Instalación

```bash
# Clonar repositorio
git clone https://github.com/B10sp4rt4n/RegAI.git
cd RegAI

# Instalar dependencias
pip install streamlit pandas openai

# Configurar API key (opcional)
export OPENAI_API_KEY="tu-api-key"

# Ejecutar
streamlit run app.py
```

---

## 🗺️ Roadmap

### Fase 1 — Fundamentos
- [ ] Autenticación multiusuario
- [ ] Permisos por proyecto
- [ ] Reconstrucción de contexto conversacional

### Fase 2 — Colaboración
- [ ] Identificación de participantes por turno
- [ ] Notificaciones de actividad
- [ ] Comentarios en conversaciones

### Fase 3 — Inteligencia
- [ ] Búsqueda semántica entre conversaciones
- [ ] Resúmenes automáticos de sesiones
- [ ] Fork de conversaciones para explorar alternativas

### Fase 4 — Enterprise
- [ ] SSO / SAML
- [ ] Audit logs exportables
- [ ] Multi-modelo (Anthropic, local, Azure)

---

## 🆚 Diferenciación

| Herramienta | Qué hace | Limitación |
|-------------|----------|------------|
| ChatGPT | Conversaciones individuales | Se pierden, no son del equipo |
| Notion AI | Documentos con IA | No captura el proceso |
| Slack + bots | Conversaciones de equipo | Ruido, no estructurado |
| **RegAI** | Conversaciones estructuradas, inmutables, multi-participante | — |

---

## 📄 Licencia

MIT

---

> *"ChatGPT es para conversaciones desechables. RegAI es para conversaciones que importan."*