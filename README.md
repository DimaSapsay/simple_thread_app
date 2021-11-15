simple threading request app
-----------------

В данном случае применялись потоки. Т.к. мы имеем дело с операциями I/O.

Вермя выполнения - 6,8 сек.

Длинна 1го словаря (п. 3 задания) - 69.
Длинна 2го словаря (п. 4 задания) - 61.

## Подготовить виртуальную среду
```bash
virtualenv -p python3 venv
source ./venv/bin/activate
```
## Установить зависимости
```bash
pip install -r requirements.txt
```
## Запустить
```bash
python app.py
```
