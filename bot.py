import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage


TOKEN = os.getenv("USTATOP_TOKEN")

if not TOKEN:
    raise ValueError("USTATOP_TOKEN topilmadi!")


bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class MasterForm(StatesGroup):
    name = State()
    phone = State()
    category = State()
    location = State()
    experience = State()
    services = State()
    photos = State()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Usta topish")],
            [KeyboardButton(text="🧑‍🔧 Men ustaman")],
            [KeyboardButton(text="📦 Buyurtmalarim")],
            [KeyboardButton(text="👤 Profilim")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "🔧 USTaTOP\n\nIshonchli ustani tez toping!",
        reply_markup=keyboard
    )


@dp.message(F.text == "🧑‍🔧 Men ustaman")
async def master_start(message: Message, state: FSMContext):
    await state.set_state(MasterForm.name)
    await message.answer("👤 Ismingizni kiriting:")


@dp.message(MasterForm.name)
async def master_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(MasterForm.phone)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="📱 Telefon raqamimni yuborish",
                request_contact=True
            )]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "📱 Telefon raqamingizni yuboring:",
        reply_markup=keyboard
    )


@dp.message(MasterForm.phone, F.contact)
async def master_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(MasterForm.category)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔌 Elektrik")],
            [KeyboardButton(text="🚰 Santexnik")],
            [KeyboardButton(text="📱 Telefon ustasi")],
            [KeyboardButton(text="💻 Kompyuter ustasi")],
            [KeyboardButton(text="❄️ Konditsioner ustasi")],
            [KeyboardButton(text="🧊 Muzlatgich ustasi")],
            [KeyboardButton(text="🚗 Avto usta")],
            [KeyboardButton(text="🧱 Remont ustasi")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "🔧 Qaysi sohada ishlaysiz?",
        reply_markup=keyboard
    )


@dp.message(MasterForm.category)
async def master_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(MasterForm.location)

    await message.answer(
        "📍 Qaysi hududda ishlaysiz?\n\n"
        "Masalan: Qo‘qon"
    )


@dp.message(MasterForm.location)
async def master_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(MasterForm.experience)

    await message.answer(
        "💼 Necha yil tajribangiz bor?"
    )


@dp.message(MasterForm.experience)
async def master_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await state.set_state(MasterForm.services)

    await message.answer(
        "🔧 Qanday xizmatlar ko‘rsatasiz?\n\n"
        "Masalan:\n"
        "• Rozetka o‘rnatish\n"
        "• Elektr simlarini ta'mirlash\n"
        "• Chiroq o‘rnatish"
    )


@dp.message(MasterForm.services)
async def master_services(message: Message, state: FSMContext):
    await state.update_data(services=message.text)
    await state.set_state(MasterForm.photos)

    await message.answer(
        "📸 Endi qilgan ishlaringizning rasmlarini yuboring.\n\n"
        "Bir nechta rasm yuborishingiz mumkin.\n"
        "Tugatgach /done yozing."
    )


@dp.message(MasterForm.photos, F.photo)
async def master_photo(message: Message, state: FSMContext):
    data = await state.get_data()

    photos = data.get("photos", [])
    photos.append(message.photo[-1].file_id)

    await state.update_data(photos=photos)

    await message.answer(
        f"✅ Rasm qabul qilindi!\n"
        f"📸 Rasmlar soni: {len(photos)}\n\n"
        f"Yana rasm yuboring yoki /done yozing."
    )


@dp.message(MasterForm.photos, F.text == "/done")
async def master_done(message: Message, state: FSMContext):
    data = await state.get_data()

    photos = data.get("photos", [])

    if not photos:
        await message.answer(
            "⚠️ Kamida 1 ta ish rasmini yuboring."
        )
        return

    await message.answer(
        "🎉 Usta profilingiz tayyor!\n\n"
        f"👨‍🔧 {data['name']}\n"
        f"🔧 {data['category']}\n"
        f"📍 {data['location']}\n"
        f"💼 Tajriba: {data['experience']}\n"
        f"📸 Ish rasmlari: {len(photos)} ta\n\n"
        "✅ Profil muvaffaqiyatli yaratildi!"
    )

    await state.clear()


async def main():
    print("🤖 UstaTop bot ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
