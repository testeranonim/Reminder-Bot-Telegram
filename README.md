![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

<h1>🍓 Reminder Bot for Telegram</h1> 
<p>Бот для записи напомнинаний пользователей, которые хранятся в бд и присылаются в назначенное время. Также для юзера доступна команда, реализована с помощью пагинации, которая выводит список <b>всех</b> напоминаний</p>
<p></p>
<img src="https://github.com/user-attachments/assets/204da5be-c441-4c42-a8a5-e299f82c89f0" width="449" height="394" />

## 🤖 Возможности | Команды
<div>
  <p>
    <ul>
      <li>Команда <code><i><b>/add</b></i></code> добавляет напоминание в следующем формате: <code>/add <i>text YY-MM-DD HH:MM</i></code></li>
      <li>Команда <code><i><b>/list</b></i></code> показывает все активные записи</li>
    </ul>
  </p>
</div>

<div align="center">
  <img width="500" height="370" alt="image" src="https://github.com/user-attachments/assets/0ef1bdd4-b7e5-4f9b-bbf6-4f9c64affa65" />
  <img width="400" height="220" alt="image" src="https://github.com/user-attachments/assets/f277534b-fba4-4e52-b6d7-d612a8d95edf" />
</div>

<h2>🚀 Локальный запуск</h2> 
<h3>Требования</h3>
<div>
  <p>
    <ul>
      <li>Python 3.12.2</li>
      <li><code>pip</code></li>
    </ul>
  </p>
</div>

<h3>Клонирование репозитория</h3> 

```cmd
    git clone https://github.com/testeranonim/Reminder-Bot-Telegram.git
    cd Reminder-Bot-Telegram
```

<h3>Установка зависимостей</h3> 
<div><p>Перед установкой зависимостей рекомендуется использовать виртуальное окружение.</p></div>
<h4>Windows</h4> 

```
    python -m venv venv               # создание виртуального окружения
    venv\Scripts\activate             # активация окружения
    pip install -r requirements.txt   # установка зависимостей
```

<h3>Конфигурация</h3>

<div>
  <p>
    <ul>
      <li>Получите токен бота у BotFather в Telegram.</li>
      <li>Создайте файл <b>.env</b> и впишите <i>token='ВАШПОЛУЧЕННЫЙТОКЕН'</i></li>
    </ul>
  </p>
</div>

<h3>Запуск бота</h3>

```
    python main.py
```

<h2>📩 Обратная связь</h2>
В тг моя личка всегда открыта для любых вопросов 👉 @spidoznaya_shlyha


