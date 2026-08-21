import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from database import init_db, add_task, get_tasks, complete_task

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the Todo Manager Bot!\n\n"
        "Commands:\n"
        "/add <task> - Add a new task\n"
        "/list - Show pending tasks\n"
        "/done <id> - Mark a task as completed"
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    task_text = " ".join(context.args)
    if not task_text:
        await update.message.reply_text("Please provide a task description. Example:\n/add Buy milk")
        return
    add_task(user_id, task_text)
    await update.message.reply_text(f"Task added: {task_text}")

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tasks = get_tasks(user_id)
    if not tasks:
        await update.message.reply_text("Your todo list is empty!")
        return
    
    msg = "Your Pending Tasks:\n\n"
    for task_id, task, _ in tasks:
        msg += f"🔹 [{task_id}] {task}\n"
    msg += "\nUse /done <id> to mark a task as completed."
    await update.message.reply_text(msg)

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Please provide a valid task ID. Example:\n/done 1")
        return
    
    task_id = int(context.args[0])
    complete_task(task_id, user_id)
    await update.message.reply_text(f"Task #{task_id} marked as completed!")

if __name__ == "__main__":
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_tasks))
    app.add_handler(CommandHandler("done", done))
    
    print("Bot is running...")
    app.run_polling()