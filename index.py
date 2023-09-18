import telebot
from telebot import types
bot = telebot.TeleBot('6475734185:AAH2S4m1xtQBYwDQxWydGnnOJvYn8r6LhNQ')

vacancies = [
    {
        'title': 'Менеджер з продажу',
        'description': '''Який графік роботи? \nПн- пт з 9.00 до 18.00, одна година перерви в продовж дня. Робота повністю віддалена але потребує 8 годин робочого часу.\n\n
Яка заробітна плата? \nЗарплатня залежить від бажання працювати та докладених зусиль і при цьому не має обмежень по сумі. В середньому новачок отримує від 20 тис грн, з другого/третього місяця 30 тис +. Заробітна плата складається з відсотку від продажів та бонусів за виконання нормативів. Щотижня в нас проходять регулярні конкурси та розіграші, що стимулюють ентузіазм і допомагають збільшити дохід.\n\n
Що потрібно для роботи? \n► Oблаштоване робоче місце \n► Ноутбук/пк \n► Iнтернет \n► Гарнітура (мікрофон + навушники) \n► Бажання працювати\n\n
Кого шукаємо? \nРозглядаємо кандидатів з 18 років з досвідом або без досвіду роботи на аналогічній посаді з великим бажанням навчатись та працювати. Володіння українською мовою на рівні спілкування є обов’язковим. Перевага а старті буде якщо ти не маєш обмежень в розмові з іншими людьми, не боїшся спілкуватися, і робити від 100 дзвінків на день.'''
    }
]


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    next = types.InlineKeyboardButton("Далі")
    markup.row(next)
    caption = f'Вітаю, {message.from_user.first_name}! я бот – Тарас, я допоможу тобі ознайомитись з компанією IQmeda, дізнатись більше про продукцію та актуальні вакансії. \n \nМи на ринку вже 4 роки та маємо більше 10 тис задоволених клієнтів. Незважаючи на тяжкую ситуацію в країні, наш колектив постійно розвивається та росте, тому ми запрошуємо саме тебе приєднатися до команди професіоналів своєї справи.'
    bot.send_message(message.chat.id, caption, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Далі')
def final(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    vacancy = types.KeyboardButton("Наші вакансії")
    about = types.KeyboardButton("Детальніше про компанію")
    product = types.KeyboardButton("Наша продукція")
    markup.add(vacancy, about, product)
    caption = f'Щоб перейти до меню, натисни тут 👇😁'
    bot.send_message(message.chat.id, caption, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Наші вакансії')
def vacancy(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for vacancy in vacancies:
        buttons.append(types.KeyboardButton(vacancy['title']))
    back = types.KeyboardButton('Назад')
    buttons.append(back)
    markup.add(*buttons)
    caption = 'Вибери вакансію, яка тебе зацікавила 😉'
    bot.send_message(message.chat.id, caption, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in [vacancy['title'] for vacancy in vacancies])
def handle_vacancy(message):
    vacancy_title = message.text
    selected_vacancy = next((vacancy for vacancy in vacancies if vacancy['title'] == vacancy_title), None)
    if selected_vacancy:
        bot.send_chat_action(message.chat.id, 'typing')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        form = types.InlineKeyboardButton('Подати заявку')
        markup.add(form)
        caption = selected_vacancy['description']
        bot.send_message(message.chat.id, caption, reply_markup=markup)
        bot.register_next_step_handler(message, ask_experience, vacancy_title)


def ask_experience(message, vacancy_title):
    bot.send_message(message.chat.id, 'Чи маєте досвід роботи в продажах?')
    bot.register_next_step_handler(message, ask_age, vacancy_title)


def ask_age(message, vacancy_title):
    expirience = message.text
    bot.send_message(message.chat.id, 'Cкільки вам років?')
    bot.register_next_step_handler(message, ask_money, vacancy_title, expirience)


def ask_money(message, vacancy_title, expirience):
    age = message.text
    bot.send_message(message.chat.id, 'Який дохід в місяць хотіли б мати?')
    bot.register_next_step_handler(message, ask_name, vacancy_title, expirience, age)

def ask_name(message, vacancy_title, expirience, age):
    money = message.text
    bot.send_message(message.chat.id, "Вкажіть ваше ім'я та прізвище:")
    bot.register_next_step_handler(message, ask_phone, vacancy_title, expirience, age, money)


def ask_phone(message, vacancy_title, expirience, age, money):
    first_name = message.text
    bot.send_message(message.chat.id, "Ваш телефон для зв'язку: ")
    bot.register_next_step_handler(message, send_contact, vacancy_title, first_name, expirience, age , money)


def send_contact(message, vacancy_title, first_name, expirience, age, money):
    phone_number = message.text
    username = message.from_user.username
    chat_id = '-4027607878' 
    text = f"Вакансия: {vacancy_title}\nДосвід: {expirience}\nВік: {age}\nДохід в місяць хотіли б мати: {money}\nИм'я: {first_name}\nНомер телефона: {phone_number}\nUsername Telegram: @{username}"
    bot.send_message(chat_id, text)
    bot.send_message(message.chat.id, "Вашу заявку було надіслано нашому HR-відділу, ми з вами зв'яжемося")
    bot.register_next_step_handler(message, final)


@bot.message_handler(func=lambda message: message.text == 'Детальніше про компанію')
def detail(message):
    caption = f'''IQmeda це міжнародна динамічна компанія, яка постійно розвивається. \n\n  
► Ми працюємо з довготривалою перспективою, для нас клієнт – це клієнт на все життя, а співробітник – це сім'я. \n 
► Наша місія – робити людей здоровими та щасливими. Ми чуємо клієнта та вирішуємо його потреби. Для цього ми випускаємо тільки ефективну продукцію і працюємо з якісними та натуральними продуктами. Наші рецептури розробляються найкращими технологами тільки з натуральних компонентів.\n
► Наша місія всередині команди – дбати про співробітників, ми надаємо корпоративне навчання. Допомагаємо отримати досвід та компетенції, які призводять до зростання нових навичок та заробітної плати, втілення як робочих так і особистих цілей. Ми вчимося бути «чарівниками» та сприяємо виконанню мрій.\n
► Ми відбираємо найкращих серед претендентів і розвиваємося через взрощування лідерів всередині компанії. \n
► Ми вітаємо тебе! у тебе є можливість швидко вирости з менеджера у керівника чи партнера.Тобі дуже пощастило, всього за 2 тижні ти можеш стати професіоналом у спілкуванні та прийти до бажаного рівня заробітної плати. У нас побудована система професійного ефективного навчання, на базі якої за короткий проміжок часу ти можеш швидко рости і розвиватися. Але за однієї умови – серйозного ставлення до всього, що ти будеш вивчати всередині нашої компанії.\n ►Наше завдання зібрати сильну та ефективну команду лідерів та вийти на нові ринки Європи та Азії.


'''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton('Меню')
    markup.add(back)
    bot.send_message(message.chat.id, caption, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Наша продукція')
def product(message):
    final(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton('Меню')
    caption = f'''Серед товарів представлений широкий асортимент натуральних засобів, розроблених на основі рецептів народної медицини із застосуванням лікарських рослин. Секрет оздоровчої дії продукції на організм прихований в ідеальному співвідношенні природних компонентів у складах бальзамів, еліксирів, концентратів та інших продуктів бренду IQmeda. Вся продукція бренду IQmeda – натуральна, абсолютно безпечна, не викликає звикання, має необхідні сертифікати якості. Наша продукція представлена в каталозі сайту «Розетка», де ви можее познайомитись з асортиментом та справжніми відгуками.  https://rozetka.com.ua/ua/seller/bioletta/goods/'''
    markup.add(back)
    bot.send_message(message.chat.id, caption, reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == 'Меню')
def go_menu(message):
    final(message)
    

@bot.message_handler(func=lambda message: message.text == 'Назад')
def go_final(message):
    final(message)


bot.polling(none_stop=True)