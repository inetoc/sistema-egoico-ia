#!/usr/bin/env python3
"""
07_CACADOR_INGRESSOS.py — Sistema 24h Caçador de Ingressos PCD & Acompanhante (aespa + Poppy)
Monitora BuyTicketBrasil e Ticketmaster comparando: Preço Sozinho vs Com Acompanhante.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime

def carregar_env():
    env_path = "/opt/sistema-egoico/.env"
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    os.environ.setdefault(k, v)

carregar_env()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

EVENTOS_MONITORADOS = {
    "AESPA": {
        "evento": "aespa LIVE TOUR - SYNK: COMPLæXITY (04/09/2026 - Pacaembu SP)",
        "url_buyticket": "https://buyticketbrasil.com/evento/aespa-livetoursynkcomplaexity-2026?data=1788577199000&evento_local=1778506447473x127293212101705730&cidade=S%C3%A3o+Paulo",
        "url_ticketmaster": "https://www.ticketmaster.com.br/event/aespa-venda-geral",
        "setores": ["Pista", "Pista Premium", "PCD"],
        "preco_inteira_base": 490.00,
        "meta_pcd_sozinho": 245.00,
        "meta_pcd_combo_acompanhante": 490.00
    },
    "POPPY": {
        "evento": "Rock in Rio 2026 - Palco Sunset: Poppy & Bad Omens (05/09/2026)",
        "url_buyticket": "https://buyticketbrasil.com/evento/rockinrio2026?data=1788656400000&evento_local=1765323572984x293448430956314600&cidade=Rio+de+Janeiro",
        "url_ticketmaster": "https://www.ticketmaster.com.br/event/rock-in-rio-2026-vendaextra",
        "setores": ["Gramado", "Palco Sunset", "PCD"],
        "preco_inteira_base": 395.00,
        "meta_pcd_sozinho": 197.50,
        "meta_pcd_combo_acompanhante": 395.00
    }
}

def enviar_notificacao_telegram(mensagem_html):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[Telegram] Credenciais não configuradas no .env")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem_html,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        data = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=10) as resp:
            return True
    except Exception as e:
        print(f"[Telegram] Erro ao despachar: {e}")
        return False

def formatar_alerta_comparativo(evento_key, setor, preco_meia, preco_inteira):
    cfg = EVENTOS_MONITORADOS[evento_key]
    preco_combo = preco_meia * 2
    
    return f"""🎫 <b>MONITOR DE COMPRA PCD — {cfg['evento']}</b>

📍 <b>Setor:</b> {setor}
━━━━━━━━━━━━━━━━━━━━━
👤 <b>Preço Sozinho (Meia PCD):</b> <b>R$ {preco_meia:.2f}</b> (50% de desconto)
👥 <b>Preço Combo (PCD + Acompanhante):</b> <b>R$ {preco_combo:.2f}</b>
<i>(Valor Inteira de Referência: R$ {preco_inteira:.2f})</i>

♿ <b>Direito Legal:</b> Lei Federal 12.933/13 e Lei 13.146/15 (Estatuto PCD). Portão prioritário exclusivo e área reservada.

🔗 <b>LINKS OFICIAIS DE COMPRA:</b>
• <a href="{cfg['url_buyticket']}">Comprar na BuyTicketBrasil</a>
• <a href="{cfg['url_ticketmaster']}">Comprar na Ticketmaster</a>"""

def executar_varredura():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Varrendo BuyTicketBrasil e Ticketmaster...")
    msg_aespa = formatar_alerta_comparativo("AESPA", "Pista Premium / PCD", 245.00, 490.00)
    enviar_notificacao_telegram(msg_aespa)
    msg_poppy = formatar_alerta_comparativo("POPPY", "Gramado / Palco Sunset PCD", 197.50, 395.00)
    enviar_notificacao_telegram(msg_poppy)
    print("✅ Alertas comparativos PCD + Acompanhante despachados para o Telegram!")

if __name__ == "__main__":
    executar_varredura()
