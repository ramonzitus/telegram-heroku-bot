import os
import random
from datetime import datetime, timedelta, time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
import asyncio
import pytz

# Obter TOKEN e CHAT_ID das variáveis de ambiente
TOKEN = os.environ.get('TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

if not TOKEN or not CHAT_ID:
    raise ValueError("TOKEN e CHAT_ID precisam ser definidos nas variáveis de ambiente.")

# Configurar o fuso horário
fuso_horario = pytz.timezone('America/Sao_Paulo')

bot = Bot(token=TOKEN)

async def enviar_mensagem():
    await bot.send_message(chat_id=CHAT_ID, text="Lembrete: Registre seu ponto no Coalize.")

def agendar_mensagens():
    scheduler = AsyncIOScheduler(timezone=fuso_horario)

    # Definir os períodos (hora_inicial, minuto_inicial, hora_final, minuto_final)
    periodos = [
        (7, 50, 8, 10),
        (12, 21, 12, 31),
        (13, 31, 13, 41),
        (18, 50, 19, 10),
        (23, 15, 23, 25),
    ]

    agora = datetime.now(fuso_horario)

    for hora_inicio, minuto_inicio, hora_fim, minuto_fim in periodos:
        inicio = agora.replace(hour=hora_inicio, minute=minuto_inicio, second=0, microsecond=0)
        fim = agora.replace(hour=hora_fim, minute=minuto_fim, second=0, microsecond=0)

        # Se o período já passou hoje, agendar para o próximo dia
        if agora > fim:
            inicio += timedelta(days=1)
            fim += timedelta(days=1)

        # Gerar um horário aleatório dentro do período
        delta = fim - inicio
        segundos_aleatorios = random.randint(0, int(delta.total_seconds()))
        horario_envio = inicio + timedelta(seconds=segundos_aleatorios)

        # Agendar o envio da mensagem
        scheduler.add_job(enviar_mensagem, 'date', run_date=horario_envio)
        print(f"Mensagem agendada para: {horario_envio}")

    scheduler.start()
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    agendar_mensagens()
