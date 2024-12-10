#### `find_game(pattern: str, supportedlang='russian', page_start=0) -> dict`

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
```

### `find_info(link: str, strict_regime=True) -> dict`

Извлекает информацию о игре из магазина Steam по заданной ссылке.

#### Параметры:

- **link** (`str`): URL-адрес страницы игры в Steam (например, `'https://store.steampowered.com/app/431960/Wallpaper_Engine/'`).

- **strict_regime** (`bool`, по умолчанию `True`): Если установлено в `True`, функция будет выбрасывать исключения, если не удается найти определенные атрибуты. Если `False`, функция вернет `None` для отсутствующих атрибутов.

#### Возвращает:

`dict`: Словарь, содержащий информацию о игре, в следующем формате:

```python
{
    'name': 'Wallpaper Engine',
    'price': 249.0,
    'description': 'Устанавливайте шикарные живые обои на рабочий стол...',
    'minimal_option': {
        'ОС': 'Windows 10, Windows 11',
        'Процессор': '1.66 GHz Intel i5 or equivalent',
        'Оперативная память': '1024 MB ОЗУ',
        'Видеокарта': 'HD Graphics 4000 or above',
        'DirectX': 'версии 11',
        'Место на диске': '512 MB'
    },
    'recomendation_option': {
        'ОС': 'Windows 10, Windows 11',
        'Процессор': '2.0 GHz Intel i7 or equivalent',
        'Оперативная память': '2048 MB ОЗУ',
        'Видеокарта': 'NVIDIA GeForce GTX 660, AMD HD7870, 2 GB VRAM or above',
        'DirectX': 'версии 11',
        'Место на диске': '1024 MB'
    },
    'source': {
        'images': [
            'https://example.com/image1.jpg',
            'https://example.com/image2.jpg'
        ],
        'videos': [
            'https://video.fastly.steamstatic.com/store_trailers/256735610/movie_max.mp4'
        ]
    }
}
