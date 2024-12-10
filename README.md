### `find_game(pattern: str, supportedlang='russian', page_start=0) -> dict`

Ищет игры на платформе Steam по заданному шаблону и возвращает список результатов.

#### Параметры:

- **pattern** (`str`): Название игры или часть названия, по которому будет производиться поиск.
  
- **supportedlang** (`str` или `list`, по умолчанию `'russian'`): Язык, на котором будут отображаться результаты. Можно указать как строку, так и список языков. Поддерживаемые языки:
  - `russian`
  - `romanian`
  - `schinese`
  - `tchinese`
  - `japanese`
  - `koreana`
  - `bulgarian`
  - `thai`
  - `czech`
  - `danish`
  - `german`
  - `english`
  - `spanish`
  - `latam`
  - `greek`
  - `french`

- **page_start** (`int`, по умолчанию `0`): Номер страницы для начала поиска. Используется для постраничного вывода.

#### Возвращает:

`dict`: Словарь, где ключами являются названия игр, а значениями — URL-адреса этих игр. Например:

```python
{
    'game_name': 'url',
    'another_game_name': 'url',
}
