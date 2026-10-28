from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext 
from service import *
import os
import asyncio
from connection import *

load_dotenv()

token_bot = os.getenv("BOT_TOKEN")

bot = Bot(token=token_bot)
dp = Dispatcher()

main_kb = ReplyKeyboardMarkup(
   keyboard=[
       [
       KeyboardButton(text="Add Task"),
       KeyboardButton(text="Read Task")
       ],
       [
       KeyboardButton(text="Update Task"),
       KeyboardButton(text="Delete Task")
       ],
       
       ], resize_keyboard=True,
    
)

class AddTask(StatesGroup):
    get_title = State()
    get_caption = State()
    get_due_date = State()
    
class ReadTask(StatesGroup):
    get_id = State()
    
    
class UpdateTask(StatesGroup):
    get_id = State()
    get_title = State()
    get_caption = State()
    get_due_date = State()
    
class DeleteTask(StatesGroup):
    get_id = State()
    
@dp.message(F.text == "Add Task")
@dp.message(Command("add"))
async def add_task(message: Message, state: FSMContext):
    await message.answer("Enter task title:")
    await state.set_state(AddTask.get_title)


@dp.message(AddTask.get_title)
async def add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Enter caption:")
    await state.set_state(AddTask.get_caption)


@dp.message(AddTask.get_caption)
async def add_task_get_caption(message: Message, state: FSMContext):
    await state.update_data(caption=message.text)
    await message.answer("Enter duration:")
    await state.set_state(AddTask.get_due_date)


@dp.message(AddTask.get_due_date)
async def add_task_duration(message: Message, state: FSMContext):
    await state.update_data(due_date=message.text)
    data = await state.get_data()
    await create_task(
        data["title"],
        data["caption"],
        data["due_date"],
        message.from_user.id
    )
    await message.answer("Your task saved successfully!")
    await state.clear() 
    
@dp.message(F.text == "Read Task")
@dp.message(Command("read"))
async def read_task(message: Message):
    tasks = await get_task()
    if tasks:
        for task in tasks:
            await message.answer(f"""
ID: {task['task_id']}
Title: {task['title']}
Caption: {task['caption']}
Due date: {task['due_date']}
Created at: {task['created_at']}
""")
    else:
        await message.answer(f"You dont have task")
        






@dp.message(F.text == "Update Task")
@dp.message(Command("update_task"))
async def update_task_start(message: Message, state: FSMContext):
    await message.answer("Enter task id:")
    await state.set_state(UpdateTask.get_id)


@dp.message(UpdateTask.get_id)
async def update_task_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Enter a number task id:")
        return
    await state.update_data(task_id=message.text)
    await message.answer("Enter new task title:")
    await state.set_state(UpdateTask.get_title)


@dp.message(UpdateTask.get_title)
async def update_task_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Enter new task caption:")
    await state.set_state(UpdateTask.get_caption)


@dp.message(UpdateTask.get_caption)
async def update_task_caption(message: Message, state: FSMContext):
    await state.update_data(caption=message.text)
    await message.answer("Enter new task due date:")
    await state.set_state(UpdateTask.get_due_date)


@dp.message(UpdateTask.get_due_date)
async def update_task_due_date(message: Message, state: FSMContext):
    await state.update_data(due_date=message.text)
    data = await state.get_data()
    await update_task(
        data["task_id"],
        data["title"],
        data["caption"],
        data["due_date"]
    )
    await message.answer("Task updated successfully!")
    await state.clear()








@dp.message(F.text == "Delete Task")
@dp.message(Command("delete"))
async def delete_task_start(message: Message, state: FSMContext):
    await message.answer("Enter task id to delete:")
    await state.set_state(DeleteTask.get_id)


@dp.message(DeleteTask.get_id)
async def delete_task_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Enter a number task id: ")
        return
    task_id = int(message.text)
    await delete_task(task_id)
    await message.answer("Task deleted successfully!")
    await state.clear()







@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Hello my dear friend", reply_markup=main_kb)
    

async def main():
    await create_table()
    print("Bot started!")
    await dp.start_polling(bot)
    
    
if __name__ == "__main__":
    asyncio.run(main())
