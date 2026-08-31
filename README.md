# SISTEMA EGÓICO DE IA — ARQUITETURA COGNITIVA MULTI-AGENTE

O **Sistema Egóico de IA** é uma arquitetura avançada de atendimento e conversão autônoma inspirada no modelo estrutural da psique humana (Id, Ego e Superego), projetada especificamente para operações no WhatsApp com alta taxa de conversão e proteção contra banimentos da Meta.

## 🚀 Infraestrutura & Links Oficiais
- **Servidor Oficial:** Hostinger VPS `179.197.74.26` (Ambiente `/opt/`)
- **WebApp Mobile Live:** https://design.glitchorganic.com/aventura/
- **Telegram Bot:** `@Paineletalz_bot`

## 📁 Estrutura de Arquivos
- `00-ARQUITETURA-MODEL-ROUTER.md` — Matriz de modelos (DeepSeek V4 + Gemini 3.7 + Ollama local) e governança de custos.
- `01-SCHEMAS-DATABASE.sql` — DDL PostgreSQL 16 + pgvector (leads, perfis, mensagens, debates cognitivos e RAG).
- `02-PROMPTS-AGENTES.md` — Prompts calibrados para Id, Superego, Ego e Profiler.
- `03-WORKFLOW-MODEL-ROUTER.json` — Sub-workflow n8n com fallback automático e teto de custo em Redis.
- `03-WORKFLOW-N8N.json` — Workflow principal n8n integrado à Evolution API.
- `04-GUIA-DEPLOY-VPS.md` — Guia de subida do stack Docker e Traefik SSL na VPS.
- `05-ANTI-BAN-COMPLIANCE.md` — Matriz de proteção de chip, typing delays e aquecimento.
- `06-MONITORAMENTO-UPTIME-KUMA.md` — Healthchecks 24/7 e alertas no Telegram.
- `07_cacador_ingressos.py` — Monitor 24h BuyTicketBrasil/Ticketmaster (Meia PCD vs Combo Acomp.).
- `08_radar_passagens_social.py` — Monitor Outlet de Passagens/QueroPassagem + Digest X/Twitter.
- `09-AGENT-MEMORY-PERSONALIZADO.md` — Integração com Egoic Agent Memory e MCP.
- `index.html` — WebApp Mobile PWA com 3 abas, modo offline e mostrador de custos em R$.
- `.github/workflows/agent-memory-sync.yml` — GitHub Actions para validação e sincronização de memória.
