# Cash Cow - expense tracker app

Subscribe to [my Boosty](https://boosty.to/yesspeace)

### English version

This is an application for tracking expenses and income and
creating a budget.
It was developed as a school project.

The application is built using Python 3.10 and 
the [Kivy](https://kivy.org/doc/stable/) 2.1.0
and [KivyMD](https://kivymd.readthedocs.io/en/1.0.2/getting-started/) 1.0.2
frameworks.

Also recommend check my 
[presentation](https://docs.google.com/presentation/d/1uidXIrrqYoYwO-60CMU89alcnqA_kzORhoNKwwhtAUc/edit?usp=sharing)
for more information about the school project.

## Installation

To install the application, simply download the
appropriate file from
the [latest release](https://github.com/YESsPeace/Cash-Cow---expense-tracker-app/releases) or 
click on this [link](https://github.com/YESsPeace/Cash-Cow---expense-tracker-app/releases/download/release/CashCow-1.0.apk)

## Features

The application have 4 menus:

- **Accounts Menu**

<img src="https://i.imgur.com/JioJX27.gif" alt="Accounts menu gif" width="270">

- **Categories Menu**

<img src="https://i.imgur.com/DQs79H6.gif" alt="Creating a new category" width="270"> <img src="https://i.imgur.com/b7pgmnV.gif" alt="writing new transaction" width="270"> <img src="https://i.imgur.com/nkdljwF.gif" alt="month switching" width="270">

- **Transaction Menu**

<img src="https://i.imgur.com/qUoQYtm.gif" alt="Editing a transaction" width="270"> <img src="https://i.imgur.com/M9klZvP.gif" alt="Creating a new transaction" width="270"> 

- **Budget Menu**

<img src="https://i.imgur.com/tVMhRiI.gif" alt="Month switching" width="270">

## For developers

### To contribute the application

1. Install Python 3.10
2. Install [git](https://git-scm.com/downloads)
3. Clone this repository `git clone https://github.com/YESsPeace/Cash-Cow---expense-tracker-app.git`
4. Install from `requirements.txt`
   - Install [kivy](https://kivy.org/doc/stable/) `pip install kivy==2.1.0`
   - Install [kivymd](https://kivymd.readthedocs.io/en/1.0.2/getting-started/) `pip install kivymd==1.0.2`
   - Install plyer `pip install plyer==2.1.0`

### To package the application for android (buildozer)

**Buildozer works only on Linux** 

1. Install buildozer `pip install buildozer`
2. Install these libraries for buildozer, if you don't have them (commands for Ubuntu):
    - `sudo apt install git`
    - `sudo apt install cython`
    - `sudo apt install openjdk-13-jdk-headless`
    - `sudo apt install make`
    - `sudo apt install autoconf`
    - `sudo apt install libltdl-dev`
    - `sudo apt-get install build-essential libsqlite3-dev sqlite3 bzip2 libbz2-dev zlib1g-dev libssl-dev openssl libgdbm-dev libgdbm-compat-dev liblzma-dev libreadline-dev libncursesw5-dev libffi-dev uuid-dev`
3. Install cython for your venv `pip install cython`
4. Rename the main file to main.py
5. Put my [buildozer.spec](https://github.com/YESsPeace/Cash-Cow---expense-tracker-app/blob/master/buildozer.spec) file
6. Run the command `buildozer android debug deploy run`

## Contact

If you have any questions or suggestions, please email damir.ernazarov.yesspeace@gmail.com

You can also subscribe to [my Boosty](https://boosty.to/yesspeace)

____

# Cash Cow - приложения для учета расходов

Подпишитесь на [мой Boosty](https://boosty.to/yesspeace)

### Версия на Русском

Это приложение для отслеживания расходов, доходов и
создание бюджета.
Оно было разработано для школьного проекта.

Приложение написанно с использованием Python 3.10, 
[Kivy](https://kivy.org/doc/stable/) 2.1.0
и [KivyMD](https://kivymd.readthedocs.io/en/1.0.2/getting-started/) 1.0.2
фрейворками.

Также рекомендую ознакомиться с 
[моей презентацией](https://docs.google.com/presentation/d/1uidXIrrqYoYwO-60CMU89alcnqA_kzORhoNKwwhtAUc/edit?usp=sharing) 
для того, чтобы узнать больше о школьном проекте.

# Установка

Для того, чтобы установить приложения, просто скачайте соответсвующий файл из [последнего релиза](https://github.com/YESsPeace/Cash-Cow---expense-tracker-app/releases) или 
кликнув на эту [ссылку](https://github.com/YESsPeace/Cash-Cow---expense-tracker-app/releases/download/release/CashCow-1.0.apk)

# Функционал

В приложение 4 меню:

- **Accounts Menu**

<img src="https://i.imgur.com/JioJX27.gif" alt="Accounts menu gif" width="270">

- **Categories Menu**

<img src="https://i.imgur.com/DQs79H6.gif" alt="Creating a new category" width="270"> <img src="https://i.imgur.com/b7pgmnV.gif" alt="writing new transaction" width="270"> <img src="https://i.imgur.com/nkdljwF.gif" alt="month switching" width="270">

- **Transaction Menu**

<img src="https://i.imgur.com/qUoQYtm.gif" alt="Editing a transaction" width="270"> <img src="https://i.imgur.com/M9klZvP.gif" alt="Creating a new transaction" width="270"> 

- **Budget Menu**

<img src="https://i.imgur.com/tVMhRiI.gif" alt="Month switching" width="270">

## Для разработчиков

### Внести свой вклад в разработку

1. Установите Python 3.10
2. Скачайте [git](https://git-scm.com/downloads)
3. Клонируйте репозиторий `git clone https://github.com/YESsPeace/Cash-Cow---expense-tracker-app.git`
4. Установить из `requirements.txt`
   - Установить [kivy](https://kivy.org/doc/stable/) `pip install kivy==2.1.0`
   - Установить [kivymd](https://kivymd.readthedocs.io/en/1.0.2/getting-started/) `pip install kivymd==1.0.2`
   - Установить plyer `pip install plyer==2.1.0`

### Чтобы упаковать приложение для android (buildozer)

**Buildozer работает только на Linux** 

1. Установите buildozer `pip install buildozer`
2. Скачайте эти библиотеки, если у вас их нет (команды для Ubuntu):
    - `sudo apt install git`
    - `sudo apt install cython`
    - `sudo apt install openjdk-13-jdk-headless`
    - `sudo apt install make`
    - `sudo apt install autoconf`
    - `sudo apt install libltdl-dev`
    - `sudo apt-get install build-essential libsqlite3-dev sqlite3 bzip2 libbz2-dev zlib1g-dev libssl-dev openssl libgdbm-dev libgdbm-compat-dev liblzma-dev libreadline-dev libncursesw5-dev libffi-dev uuid-dev`
3. Установите cython `pip install cython`
4. Переименуйте главный файл проекта в  main.py
5. Вставьте мой [buildozer.spec](https://github.com/YESsPeace/Cash-Cow---expense-tracker-app/blob/master/buildozer.spec) file
6. Запустите команду для упаковки `buildozer android debug deploy run`

## Связаться со мной

Если у вас есть какие-то вопросы или предложения, то пишите на почту damir.ernazarov.yesspeace@gmail.com

А также, вы можете подписаться на [мой Boosty](https://boosty.to/yesspeace)
