class Product:
    """Демо-товар в памяти (не таблица БД)."""

    def __init__(self, id: int, slug: str, name: str, description: str):
        self.id = id
        self.slug = slug
        self.name = name
        self.description = description

    def __str__(self) -> str:
        return f"""
    <h3>{self.name}</h3>
    <h4>slug: {self.slug}</h4>
    <h4>id: {self.id}</h4>
    <p>{self.description}</p>
    """


products = [
    Product(0, "first-product", "Product 1", "Description of product 0"),
    Product(1, "second-product", "Product 2", "Description of product 1"),
    Product(2, "third-product", "Product 3", "Description of product 2"),
    Product(3, "fourth-product", "Product 4", "Description of product 3"),
]

# ДЗ 3: список задач (slug — для динамічного URL «за назвою»)
TASKS = [
    {"id": 1, "title": "Зробити ДЗ з Django", "slug": "django-dz", "done": False},
    {"id": 2, "title": "Купити продукти", "slug": "kupiti-produkty", "done": False},
    {"id": 3, "title": "Нагадати про дзвінок", "slug": "nagadati-dzvinok", "done": True},
    {"id": 4, "title": "Прочитати документацію", "slug": "docs", "done": False},
]


def get_task_by_id(task_id: int):
    for t in TASKS:
        if t["id"] == task_id:
            return t
    return None


def get_task_by_slug(task_slug: str):
    for t in TASKS:
        if t["slug"] == task_slug:
            return t
    return None
