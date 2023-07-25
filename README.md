# Тестовое для Weborama

[Задание 1](Test_1/README.md)

[Задание 2](Test_2/README.md)

Для работы скриптов нужно установить библиотеки из [requirements.txt](requirements.txt)

[Задание 3 скрипт](Test_3/chains.py)

```Bash
python Test_3/chains.py [OPTIONS] IMPRESSIONS_FILEPATH EVENTS_FILEPATH CONVERSIONS_FILEPATH

Options:
  -c, --chains_with_conversion_included_only
                                  Whenever use chains with conversion included
                                  only
```
В случае, если необходимо вывести топ-10 только цепочек, в которых есть конверсия, то нужно использовать флаг `-c`.

[Задание 4 скрипт](Test_4/xlsx_value_counts.py)

```Bash
python Test_4/xlsx_value_counts.py INPUT_FILEPATH OUTPUT_FILEPATH
```
