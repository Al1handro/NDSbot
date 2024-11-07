from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
import kbd

router = Router()

admin_ids = [1242185723, 7012760302]  # фильтры админов , 6329233703,
list_HR = ['Владимир', 'Евгений', 'Александра', 'Мария']
list_leads = []
list_applications = []
garbage = ''


class AddHR(StatesGroup):
    input_hr = State()


class AdminAnswer(StatesGroup):
    select_HR = State()
    input_answer = State()


class AddApplication(StatesGroup):
    add = State()


class IsAdmin(BaseFilter):
    def __init__(self, admin_ids) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


class NotIsAdmin(BaseFilter):
    def __init__(self, admin_ids) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return not message.from_user.id in self.admin_ids


@router.message(CommandStart())
async def start(message: Message) -> None:
    global list_leads
    if len(list_leads) == 0:
        list_leads.append(
            '#' + message.from_user.username + f' время создания лида - {(datetime.now()).strftime("%d %b %Y %H:%M:%S")}')
    else:
        flag = True
        for i in list_leads:
            if message.from_user.username in i:
                flag = False
        if flag:
            list_leads.append(
                '#' + message.from_user.username + f' время создания лида - {(datetime.now()).strftime("%d %b %Y %H:%M:%S")}')
    await message.answer('''🍀Мы рады приветствовать вас в нашем чат сервисе Greenavi!

Если у вас есть вопросы, связанные с оптимизацией налоговой нагрузки или другими услугами, которые мы предоставляем, пожалуйста, не стесняйтесь их задавать. Наша команда готова помочь вам в подборе поставщиков, обеспечит консультации по налоговым вопросам и предоставит информацию об условиях работы и стоимости услуг. Для оформления заявок используйте прикрепленную форму, а для получения консультации просто напишите нам в чате. Мы всегда рады помочь вашему бизнесу стать более эффективным и успешным!

Наша команда непрерывно работает над улучшением качества и эффективности работы нашего сервиса. Обновляем и увеличиваем парк компаний, улучшаем их характеристики и внедряем в работу новейшие инструменты.

С нами вы сможете подобрать для себя поставщиков с различными характеристиками:

– история реально действующей организации;
– наличие р/с;
– контактные данные и интернет-ресурсы (электронная почта, почта, номер телефона, сайт);
– штат сотрудников;
– обширный перечень кодов ОКВЭД для подбора и многое другое.  

Сервис \"Greenavi\" нацелен на долгосрочное сотрудничество, где мы стремимся стать надежной опорой в финансовом управлении вашего бизнеса.

 🍀Для оформления заказа на НДС заполните вкладку "Заявка на НДС".''')
    await message.answer(text='Если возникнут вопросы – напишите нам.')
    await message.answer_document(document='BQACAgIAAxkBAAIBqGcMHgeod8zWWV0KSe9mHuE7I8HmAAJqVQACf69pSMqIMv-QUkxtNgQ')
    await message.answer_document(document='BQACAgIAAxkBAAIBrmcMHtVZD9Q83sGt7-sXvjMM1N9nAAJvVQACf69pSAj0wUdW_bc4NgQ')


@router.message(IsAdmin(admin_ids), F.text == 'admin')
async def admin(message: Message) -> None:
    k = [
        [InlineKeyboardButton(text='Инструкция', callback_data='instruction')]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=k)
    await message.answer('Приветствую тебя, админ системы обработки заявок компании Greenavi.\n'
                         'Этот бот предназначен для упрощения обработки лидов (потенциальных клиентов компании).\n'
                         'Для удобной работы рекомендуется ознакомиться с инструкцией',
                         reply_markup=kb)
    await message.answer('Клавиатура активирована, в случае если она пропадет перезайдите в систему '
                         '(напишите в чат admin)',
                         reply_markup=kbd.start_kbd_admin)


@router.callback_query(F.data == 'instruction')
async def instruction(call: CallbackQuery) -> None:
    await call.message.answer(text='1) В панели управления 3 кнопки: статистка, список HR, принять заявку. Которые '
                              'соответственно показывают список лидов и принятых заявок, список псевдонимов для HR и'
                              ' последняя кнопка принятия заявки\nДальнейшие кнопки интуитивно понятны и '
                              'выполняют одноименные задачи.\n')
    await call.message.answer(text='2) Для того чтобы просмотреть всю переписку с клиентом необходимо выбрать выбрать '
                              'сгенерированную для каждого взаимодействия с пользователем хэштег метку (#username)\n')
    await call.message.answer(text='3) Список лидов заполняется автоматически, '
                              'список принятых заявок необходимо вести самому.\n')


@router.callback_query(F.data == 'cansel_add_hr')
async def cansel(call: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await call.message.delete()
    await state.clear()
    global list_HR
    if len(list_HR) == 0:
        await call.message.answer('Нет HR', reply_markup=kbd.add_hr)
    else:
        x = ''
        for i in list_HR:
            x += i + '\n'
        await call.message.answer(f'{x}', reply_markup=kbd.add_hr)


@router.callback_query(F.data == 'clear_hr')
async def clear_hr(call: CallbackQuery, bot: Bot) -> None:
    await call.message.delete()
    global list_HR
    list_HR.clear()
    await bot.send_message(chat_id=call.from_user.id,
                           text='Список HR очищен', reply_markup=kbd.add_hr)


@router.message(IsAdmin(admin_ids), F.text == 'Статистика')
async def leads(message: Message) -> None:
    global list_leads
    global list_applications
    k = [
        [InlineKeyboardButton(text='Показать лиды', callback_data='look_leads')],
        [InlineKeyboardButton(text='Показать заявки', callback_data='look_application')]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=k)
    await message.answer(f'Количество лидов - {len(list_leads)}\nКоличество принятых заявок - {len(list_applications)}',
                         reply_markup=kb)


@router.message(IsAdmin(admin_ids), F.text == 'Принять заявку')
async def accept_application(message: Message, bot: Bot, state: FSMContext) -> None:
    await state.set_state(AddApplication.add)
    k = [
        [InlineKeyboardButton(text='Назад', callback_data='close_answer')]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=k)
    await message.answer(text='Введите тег заявки в фомате #username', reply_markup=kb)


@router.message(AddApplication.add)
async def add_application(message: Message, state: FSMContext) -> None:
    await state.clear()
    global list_leads
    global list_applications
    if len(list_leads) == 0:
        await message.answer('Нету лидов для оформления заявки')
    else:
        app = message.text + f' время принятия заявки - {(datetime.now()).strftime("%d %b %Y %H:%M:%S")}'
        list_applications.append(app)
        await message.answer(f'Заявка {app}\nуспешно создана')
        for i in range(0, len(list_leads)):
            if message.text in list_leads[i]:
                list_leads.pop(i)
                break


@router.callback_query(IsAdmin(admin_ids), F.data == 'go_around')
async def leads(call: CallbackQuery) -> None:
    await call.message.delete()
    global list_leads
    global list_applications
    k = [
        [InlineKeyboardButton(text='Показать лиды', callback_data='look_leads')],
        [InlineKeyboardButton(text='Показать заявки', callback_data='look_application')]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=k)
    await call.message.answer(
        f'Количество лидов - {len(list_leads)}\nКоличество принятых заявок - {len(list_applications)}',
        reply_markup=kb)


@router.callback_query(F.data == 'look_leads')
async def look_leads(call: CallbackQuery, bot: Bot) -> None:
    await call.message.delete()
    global list_leads
    global garbage
    if len(list_leads) == 0:
        await call.message.answer(text='Лист лидов пуст', reply_markup=kbd.go_around)
    else:
        for i in list_leads:
            garbage += i + '\n'
        await call.message.answer(text=f'{garbage}', reply_markup=kbd.go_around)
    garbage = ''


@router.callback_query(F.data == 'look_application')
async def look_application(call: CallbackQuery, bot: Bot) -> None:
    await call.message.delete()
    global list_applications
    global garbage
    if len(list_applications) == 0:
        await call.message.answer(text='Лист принятых заявок пуст',
                                  reply_markup=kbd.go_around)
    else:
        for i in list_applications:
            garbage += i + '\n'
        await call.message.answer(text=f'{garbage}', reply_markup=kbd.go_around)
    garbage = ''


@router.message(IsAdmin(admin_ids), F.text == 'Список HR')
async def hr(message: Message) -> None:
    global list_HR
    if len(list_HR) == 0:
        await message.answer('Нет HR', reply_markup=kbd.add_hr)
    else:
        x = ''
        for i in list_HR:
            x += i + '\n'
        await message.answer(f'{x}', reply_markup=kbd.add_hr)


@router.callback_query(F.data == 'add_hr')
async def add_hr(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await call.message.delete()
    await bot.send_message(chat_id=call.from_user.id,
                           text='Введите имя HR или список с именами, в котором каждое имя записано с новой строки.',
                           reply_markup=kbd.cansel_add_hr)
    await state.set_state(AddHR.input_hr)


@router.message(AddHR.input_hr)
async def input_hr(message: Message, state: FSMContext) -> None:
    global list_HR
    list_HR += message.text.split('\n')
    await message.answer('Список HR изменен')
    await state.clear()
    if len(list_HR) == 0:
        await message.answer('Нет HR', reply_markup=kbd.add_hr)
    else:
        x = ''
        for i in list_HR:
            x += i + '\n'
        await message.answer(f'{x}', reply_markup=kbd.add_hr)


@router.callback_query(F.data == 'close_answer')
async def close_answer(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.delete()


@router.callback_query(F.data.startswith('answer_admin'))
async def answer_script(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    x = call.data.split('`')
    chat_id = x[1]
    username = x[2]
    print(x)
    global list_HR
    res = []
    for i in list_HR:
        res.append([InlineKeyboardButton(text=i, callback_data='next' + '`' + i + '`' + chat_id + '`' + username)])
    res.append([InlineKeyboardButton(text='Назад', callback_data='close_answer')])
    kb = InlineKeyboardMarkup(inline_keyboard=res)
    await call.message.answer(text='Выберите HR', reply_markup=kb)


@router.callback_query(F.data.startswith('next'))
async def input_answer(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.message.delete()
    await state.set_state(AdminAnswer.input_answer)
    x = call.data.split('`')
    name = x[1]
    chat_id = x[2]
    username = x[3]
    await state.update_data(HR_name=name)
    await state.update_data(chat_id=chat_id)
    await state.update_data(username=username)
    await call.message.answer('Введите сообщение')


@router.message(AdminAnswer.input_answer)
async def input_answer(message: Message, bot: Bot, state: FSMContext):
    zalupa = await state.get_data()
    print(zalupa)
    await bot.send_message(chat_id=int(zalupa['chat_id']),
                           text=f'<b>{zalupa["HR_name"]}</b>\n'
                                f'{message.text}',
                           parse_mode=ParseMode.HTML)
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Пользователь @{zalupa["username"]}'
                                f'\n#{zalupa["username"]}')
    await state.clear()


@router.message(NotIsAdmin(admin_ids))
async def default(message: Message, bot: Bot) -> None:
    global list_leads
    buttons = [
        [InlineKeyboardButton(text='Ответить сообщением', callback_data='answer_admin' + '`' +
                                                                        str(message.from_user.id) + '`' +
                                                                        str(message.from_user.username))],
        [InlineKeyboardButton(text='Принять заявку', callback_data='accept_the_application')]
    ]
    answer_button = InlineKeyboardMarkup(inline_keyboard=buttons)
    for i in admin_ids:
        await bot.forward_message(i, message.from_user.id, message.message_id)
        await bot.send_message(chat_id=i, text=f'Пользователь @{message.from_user.username}'
                                               f'\n#{message.from_user.username}',
                               reply_markup=answer_button)
