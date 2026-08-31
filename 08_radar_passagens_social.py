#!/usr/bin/env python3
"""
08_RADAR_PASSAGENS_SOCIAL.py — Monitor de Passagens PCD & Gratuidade + Retorno Flexível + X
Trechos:
1. Guarapuava -> SP
2. SP -> Rio
3. Rio -> Guarapuava OU Florianópolis OU São Paulo
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

TRECHOS_PCD = [
    {
        "nome": "1. IDA: Guarapuava (PR) ➔ São Paulo (Barra Funda)",
        "data": "03/09/2026 (Noite)",
        "preco_comercial": 135.00,
        "preco_meia_pcd": 67.50,
        "gratuidade_passe_livre": "R$ 0,00 (2 vagas por ônibus ANTT)",
        "plataformas": "QueroPassagem / Outlet de Passagens / Guichê Rodoviária",
        "url_compra": "https://queropassagem.com.br/onibus/guarapuava-pr-para-sao-paulo-sp"
    },
    {
        "nome": "2. INTERMEDIÁRIO: São Paulo (Tietê) ➔ Rio de Janeiro (Novo Rio)",
        "data": "05/09/2026 (Madrugada 00:35 / 02:30)",
        "preco_comercial": 89.90,
        "preco_meia_pcd": 44.95,
        "gratuidade_passe_livre": "R$ 0,00 (Passe Livre ANTT)",
        "plataformas": "Outlet de Passagens / 1001 / Águia Branca",
        "url_compra": "https://outletdepassagens.com.br/passagens-de-onibus/sao-paulo-sp-todos-para-rio-de-janeiro-rj-todos"
    },
    {
        "nome": "3. RETORNO OPÇÃO A: Rio de Janeiro ➔ Guarapuava (PR)",
        "data": "06/09/2026 (Manhã)",
        "preco_comercial": 159.00,
        "preco_meia_pcd": 79.50,
        "gratuidade_passe_livre": "R$ 0,00 (Passe Livre ANTT)",
        "plataformas": "QueroPassagem / Catarinense",
        "url_compra": "https://queropassagem.com.br/onibus/rio-de-janeiro-rj-para-guarapuava-pr"
    },
    {
        "nome": "3. RETORNO OPÇÃO B: Rio de Janeiro ➔ Florianópolis (SC)",
        "data": "06/09/2026 (Manhã / Tarde)",
        "preco_comercial": 149.00,
        "preco_meia_pcd": 74.50,
        "gratuidade_passe_livre": "R$ 0,00 (Passe Livre ANTT)",
        "plataformas": "QueroPassagem / 1001 / Catarinense",
        "url_compra": "https://queropassagem.com.br/onibus/rio-de-janeiro-rj-para-florianopolis-sc"
    },
    {
        "nome": "3. RETORNO OPÇÃO C: Rio de Janeiro ➔ São Paulo (SP)",
        "data": "06/09/2026 (Manhã)",
        "preco_comercial": 89.90,
        "preco_meia_pcd": 44.95,
        "gratuidade_passe_livre": "R$ 0,00 (Passe Livre ANTT)",
        "plataformas": "Outlet de Passagens / QueroPassagem",
        "url_compra": "https://outletdepassagens.com.br/passagens-de-onibus/rio-de-janeiro-rj-todos-para-sao-paulo-sp-todos"
    }
]

def enviar_telegram(mensagem_html):
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
        print(f"Erro ao enviar Telegram: {e}")
        return False

def formatar_alerta_passagens():
    agora = datetime.now().strftime("%d/%m/%Y às %H:%M")
    msg = f"🚌 <b>MONITOR DE COMPRA & GRATUIDADE PCD DE PASSAGENS</b>\n<i>Atualizado em {agora}</i>\n\n"
    for t in TRECHOS_PCD:
        msg += f"📍 <b>{t['nome']}</b>\n"
        msg += f"• ♿ <b>Gratuidade Passe Livre ANTT:</b> <b>{t['gratuidade_passe_livre']}</b>\n"
        msg += f"• 👤 <b>Meia PCD:</b> <b>R$ {t['preco_meia_pcd']:.2f}</b> | 👥 <b>Combo PCD + Acomp.:</b> R$ {t['preco_comercial']:.2f}\n"
        msg += f"• 🌐 <b>Onde emitir/comprar:</b> {t['plataformas']}\n"
        msg += f"• 🔗 <a href='{t['url_compra']}'>Acessar Passagem</a>\n\n"
    return msg

def executar():
    msg = formatar_alerta_passagens()
    enviar_telegram(msg)

if __name__ == "__main__":
    executar()
