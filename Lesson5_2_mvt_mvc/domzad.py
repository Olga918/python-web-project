"""
Урок 5.2 — у одному застосунку реалізовані три завдання.

1) Облік витрат (MVC):
   - додати витрату;
   - видалити витрату за id;
   - список витрат;
   - загальна сума витрат.

2) Книга рецептів (MVT):
   - додати рецепт (назва, опис, інгредієнти, інструкція);
   - видалити за id;
   - редагувати рецепт;
   - збереження у JSON між запусками;
   - шаблони: список усіх страв; повний рецепт;
   - усі рецепти завантажуються з файлу при старті застосунку.

3) Клас «Фільм» (назва, жанр, режисер, рік, тривалість, студія, актори з П.І.Б. та роллю).
   MVT: шаблони повної / короткої інформації про фільм; повна та коротка інформація про актора.
"""

from __future__ import annotations

import json
import sys
import time
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import List

RECIPES_FILE = Path(__file__).resolve().parent / "recipes.json"


def _configure_console_utf8() -> None:
    for stream in (sys.stdout, sys.stdin, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (OSError, ValueError, AttributeError):
                pass


# ---------------------------------------------------------------------------
# 1) MVC — облік витрат
# ---------------------------------------------------------------------------


def get_date_now() -> str:
    return str(datetime.now())


class Expense:
    __id: int
    title: str
    amount: float
    date: str

    def __init__(self, title: str, amount: float):
        self.__id = time.time_ns()
        self.title = title.strip()
        self.amount = float(amount)
        self.date = get_date_now()

    @property
    def id(self) -> int:
        return self.__id

    def __str__(self) -> str:
        return (
            f"Id: {self.id}\n"
            f"Назва: {self.title}\n"
            f"Сума: {self.amount:.2f}\n"
            f"Дата: {self.date}"
        )


class ExpenseModel:
    def __init__(self) -> None:
        self.expenses: list[Expense] = []

    def add_expense(self, expense: Expense) -> None:
        self.expenses.append(expense)

    def get_expense(self, expense_id: int) -> Expense | None:
        for e in self.expenses:
            if e.id == expense_id:
                return e
        return None

    def delete_expense(self, expense_id: int) -> bool:
        item = self.get_expense(expense_id)
        if item is None:
            return False
        self.expenses.remove(item)
        return True

    def get_expenses(self) -> list[Expense]:
        return self.expenses

    def get_total(self) -> float:
        return sum(e.amount for e in self.expenses)


class ExpenseView:
    def show_menu(self) -> int:
        print("1) Додати витрату")
        print("2) Список витрат")
        print("3) Видалити витрату за id")
        print("4) Загальна сума витрат")
        print("5) Вихід")
        return int(input("Оберіть пункт (1–5): "))

    def show_message(self, message: str) -> None:
        print(message)

    def create_expense(self) -> Expense:
        title = input("Опис витрати: ")
        amount_raw = input("Сума (число): ")
        return Expense(title, float(amount_raw))

    def read_delete_id(self, expenses: list[Expense]) -> int:
        self.show_expenses(expenses)
        return int(input("Id витрати для видалення: "))

    def show_expenses(self, expenses: list[Expense]) -> None:
        if not expenses:
            print("(Список порожній)")
            return
        for e in expenses:
            print("-" * 30)
            print(e)
            print("-" * 30, "\n")

    def show_total(self, total: float) -> None:
        print(f"Загальна сума витрат: {total:.2f}")


class ExpenseController:
    def __init__(self, model: ExpenseModel, view: ExpenseView) -> None:
        self.model = model
        self.view = view

    def action_add(self) -> None:
        try:
            exp = self.view.create_expense()
            if exp.amount < 0:
                self.view.show_message("Сума не може бути від'ємною.")
                return
            if not exp.title:
                self.view.show_message("Опис не може бути порожнім.")
                return
            self.model.add_expense(exp)
            self.view.show_message("Витрату додано.")
        except ValueError:
            self.view.show_message("Некоректна сума.")

    def action_list(self) -> None:
        self.view.show_expenses(self.model.get_expenses())

    def action_delete(self) -> None:
        expenses = self.model.get_expenses()
        if not expenses:
            self.view.show_message("Немає витрат для видалення.")
            return
        try:
            eid = self.view.read_delete_id(expenses)
            if self.model.delete_expense(eid):
                self.view.show_message("Витрату видалено.")
            else:
                self.view.show_message("Витрату з таким id не знайдено.")
        except ValueError:
            self.view.show_message("Некоректний id.")

    def action_total(self) -> None:
        self.view.show_total(self.model.get_total())


def run_expense_app() -> None:
    app = ExpenseController(ExpenseModel(), ExpenseView())
    while True:
        try:
            choice = app.view.show_menu()
        except ValueError:
            app.view.show_message("Введіть число від 1 до 5.")
            continue

        match choice:
            case 1:
                app.action_add()
            case 2:
                app.action_list()
            case 3:
                app.action_delete()
            case 4:
                app.action_total()
            case 5:
                app.view.show_message("Назад у головне меню.")
                break
            case _:
                app.view.show_message("Невірний пункт меню.")


# ---------------------------------------------------------------------------
# 2) MVT — книга рецептів
# ---------------------------------------------------------------------------


class Recipe:
    __id: int
    title: str
    description: str
    ingredients: list[str]
    instructions: str

    def __init__(
        self,
        title: str,
        description: str,
        ingredients: list[str],
        instructions: str,
        recipe_id: int | None = None,
    ):
        self.__id = recipe_id if recipe_id is not None else time.time_ns()
        self.title = title.strip()
        self.description = description.strip()
        self.ingredients = [i.strip() for i in ingredients if i.strip()]
        self.instructions = instructions.strip()

    @property
    def id(self) -> int:
        return self.__id

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
        }

    @staticmethod
    def from_dict(data: dict) -> Recipe:
        return Recipe(
            data["title"],
            data["description"],
            list(data["ingredients"]),
            data["instructions"],
            recipe_id=int(data["id"]),
        )


class RecipeModel:
    def __init__(self, storage_path: Path = RECIPES_FILE) -> None:
        self._path = storage_path
        self.recipes: list[Recipe] = []
        self.load()

    def load(self) -> None:
        self.recipes = []
        if not self._path.is_file():
            return
        raw = self._path.read_text(encoding="utf-8").strip()
        if not raw:
            return
        data = json.loads(raw)
        for item in data:
            self.recipes.append(Recipe.from_dict(item))

    def save(self) -> None:
        payload = [r.to_dict() for r in self.recipes]
        self._path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def add_recipe(self, recipe: Recipe) -> None:
        self.recipes.append(recipe)
        self.save()

    def get_recipe(self, recipe_id: int) -> Recipe | None:
        for r in self.recipes:
            if r.id == recipe_id:
                return r
        return None

    def delete_recipe(self, recipe_id: int) -> bool:
        r = self.get_recipe(recipe_id)
        if r is None:
            return False
        self.recipes.remove(r)
        self.save()
        return True

    def update_recipe(
        self,
        recipe_id: int,
        title: str,
        description: str,
        ingredients: list[str],
        instructions: str,
    ) -> bool:
        r = self.get_recipe(recipe_id)
        if r is None:
            return False
        r.title = title.strip()
        r.description = description.strip()
        r.ingredients = [i.strip() for i in ingredients if i.strip()]
        r.instructions = instructions.strip()
        self.save()
        return True

    def get_recipes(self) -> list[Recipe]:
        return self.recipes


class RecipeTemplate(ABC):
    @abstractmethod
    def render(self, recipes: List[Recipe]) -> None:
        pass


class DishListTemplate(RecipeTemplate):
    def render(self, recipes: List[Recipe]) -> None:
        if not recipes:
            print("Рецептів ще немає.")
            return
        print("-" * 40)
        for r in recipes:
            print(f"  [{r.id}]  {r.title}")
        print("-" * 40, "\n")


class RecipeFullTemplate(RecipeTemplate):
    def render(self, recipes: List[Recipe]) -> None:
        if not recipes:
            print("Немає рецепта для показу.")
            return
        for r in recipes:
            print("=" * 40)
            print(f"Id: {r.id}")
            print(f"Назва: {r.title}")
            print(f"Опис: {r.description}")
            print("Інгредієнти:")
            for i, ing in enumerate(r.ingredients, 1):
                print(f"  {i}. {ing}")
            print("Інструкція:")
            print(r.instructions)
            print("=" * 40, "\n")


class RecipesView:
    def __init__(self, model: RecipeModel) -> None:
        self.model = model

    def render(self, template: RecipeTemplate) -> None:
        template.render(self.model.get_recipes())


def _read_ingredients_line() -> list[str]:
    line = input("Інгредієнти (через кому): ")
    return [x.strip() for x in line.split(",") if x.strip()]


def create_recipe_interactive() -> Recipe:
    title = input("Назва страви: ")
    description = input("Короткий опис: ")
    ingredients = _read_ingredients_line()
    print("Інструкція (кілька рядків, порожній рядок — кінець):")
    lines: list[str] = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    instructions = "\n".join(lines)
    return Recipe(title, description, ingredients, instructions)


def edit_recipe_interactive(model: RecipeModel) -> None:
    if not model.get_recipes():
        print("Немає рецептів для редагування.")
        return
    RecipesView(model).render(DishListTemplate())
    try:
        rid = int(input("Id рецепта для зміни: "))
    except ValueError:
        print("Некоректний id.")
        return
    r = model.get_recipe(rid)
    if r is None:
        print("Рецепт не знайдено.")
        return
    print(f"(Enter — залишити поточне значення)\nПоточна назва: {r.title}")
    t = input("Нова назва: ")
    title = t if t.strip() else r.title
    print(f"Поточний опис: {r.description}")
    d = input("Новий опис: ")
    description = d if d.strip() else r.description
    print(f"Поточні інгредієнти: {', '.join(r.ingredients)}")
    ing_line = input("Нові інгредієнти (через кому, Enter — без змін): ")
    ingredients = (
        [x.strip() for x in ing_line.split(",") if x.strip()]
        if ing_line.strip()
        else r.ingredients
    )
    print("Нова інструкція (кілька рядків, лише Enter у першому рядку — без змін):")
    lines = []
    while True:
        line = input()
        if line == "" and not lines:
            instructions = r.instructions
            break
        if line == "":
            instructions = "\n".join(lines)
            break
        lines.append(line)
    if model.update_recipe(rid, title, description, ingredients, instructions):
        print("Рецепт оновлено.")
    else:
        print("Не вдалося оновити.")


def delete_recipe_interactive(model: RecipeModel) -> None:
    if not model.get_recipes():
        print("Немає рецептів для видалення.")
        return
    RecipesView(model).render(DishListTemplate())
    try:
        rid = int(input("Id рецепта для видалення: "))
    except ValueError:
        print("Некоректний id.")
        return
    if model.delete_recipe(rid):
        print("Видалено.")
    else:
        print("Рецепт з таким id не знайдено.")


def show_full_recipe_interactive(model: RecipeModel, view: RecipesView) -> None:
    if not model.get_recipes():
        print("Немає рецептів.")
        return
    view.render(DishListTemplate())
    try:
        rid = int(input("Id рецепта для перегляду: "))
    except ValueError:
        print("Некоректний id.")
        return
    r = model.get_recipe(rid)
    if r is None:
        print("Не знайдено.")
        return
    RecipeFullTemplate().render([r])


def recipe_book_menu() -> int:
    print("1) Додати рецепт")
    print("2) Список усіх страв (шаблон)")
    print("3) Показати повний рецепт за id (шаблон)")
    print("4) Редагувати рецепт")
    print("5) Видалити рецепт за id")
    print("6) Назад")
    return int(input("Оберіть пункт (1–6): "))


def run_recipe_book_app(model: RecipeModel, view: RecipesView) -> None:
    while True:
        try:
            choice = recipe_book_menu()
        except ValueError:
            print("Введіть число від 1 до 6.")
            continue

        match choice:
            case 1:
                model.add_recipe(create_recipe_interactive())
                print("Збережено.")
            case 2:
                view.render(DishListTemplate())
            case 3:
                show_full_recipe_interactive(model, view)
            case 4:
                edit_recipe_interactive(model)
            case 5:
                delete_recipe_interactive(model)
            case 6:
                print("Назад у головне меню.")
                break
            case _:
                print("Невірний пункт.")


# ---------------------------------------------------------------------------
# 3) MVT — каталог фільмів (клас «Фільм», шаблони для фільму та актора)
# ---------------------------------------------------------------------------


class Actor:
    """Актор: П.І.Б. та роль у фільмі."""

    full_name: str
    role: str

    def __init__(self, full_name: str, role: str) -> None:
        self.full_name = full_name.strip()
        self.role = role.strip()


class Film:
    """Фільм: назва, жанр, режисер, рік, тривалість (хв), студія, актори."""

    __id: int
    title: str
    genre: str
    director: str
    year: int
    duration_minutes: int
    studio: str
    actors: list[Actor]

    def __init__(
        self,
        title: str,
        genre: str,
        director: str,
        year: int,
        duration_minutes: int,
        studio: str,
        actors: list[Actor],
        film_id: int | None = None,
    ) -> None:
        self.__id = film_id if film_id is not None else time.time_ns()
        self.title = title.strip()
        self.genre = genre.strip()
        self.director = director.strip()
        self.year = int(year)
        self.duration_minutes = int(duration_minutes)
        self.studio = studio.strip()
        self.actors = list(actors)

    @property
    def id(self) -> int:
        return self.__id


class FilmModel:
    def __init__(self) -> None:
        self.films: list[Film] = []

    def add_film(self, film: Film) -> None:
        self.films.append(film)

    def get_films(self) -> list[Film]:
        return self.films

    def get_film(self, film_id: int) -> Film | None:
        for f in self.films:
            if f.id == film_id:
                return f
        return None


class FilmTemplate(ABC):
    @abstractmethod
    def render(self, films: List[Film]) -> None:
        pass


class FilmFullInfoTemplate(FilmTemplate):
    """Повна інформація про фільм (усі поля та актори)."""

    def render(self, films: List[Film]) -> None:
        if not films:
            print("Фільмів немає.")
            return
        for f in films:
            print("=" * 50)
            print(f"Id: {f.id}")
            print(f"Назва: {f.title}")
            print(f"Жанр: {f.genre}")
            print(f"Режисер: {f.director}")
            print(f"Рік випуску: {f.year}")
            print(f"Тривалість: {f.duration_minutes} хв.")
            print(f"Студія: {f.studio}")
            print("Актори:")
            for i, a in enumerate(f.actors, 1):
                print(f"  {i}. {a.full_name} — роль: {a.role}")
            print("=" * 50, "\n")


class FilmShortInfoTemplate(FilmTemplate):
    """Коротка інформація: назва, рік, жанр."""

    def render(self, films: List[Film]) -> None:
        if not films:
            print("Фільмів немає.")
            return
        print("-" * 40)
        for f in films:
            print(f"  [{f.id}]  {f.title} ({f.year}), {f.genre}")
        print("-" * 40, "\n")


class ActorTemplate(ABC):
    @abstractmethod
    def render(self, actors: List[Actor], film_title: str) -> None:
        pass


class ActorFullInfoTemplate(ActorTemplate):
    """Повна інформація про кожного актора (П.І.Б. та роль)."""

    def render(self, actors: List[Actor], film_title: str) -> None:
        if not actors:
            print("Акторів немає.")
            return
        print(f"--- Актори фільму «{film_title}» (повно) ---")
        for i, a in enumerate(actors, 1):
            print(f"  {i}. П.І.Б.: {a.full_name}")
            print(f"      Роль: {a.role}")
        print()


class ActorBriefInfoTemplate(ActorTemplate):
    """Коротка інформація: один рядок на актора (П.І.Б. — роль)."""

    def render(self, actors: List[Actor], film_title: str) -> None:
        if not actors:
            print("Акторів немає.")
            return
        print(f"--- Актори «{film_title}» (коротко) ---")
        for a in actors:
            print(f"  • {a.full_name} — {a.role}")
        print()


class FilmsView:
    def __init__(self, model: FilmModel) -> None:
        self.model = model

    def render(self, template: FilmTemplate) -> None:
        template.render(self.model.get_films())


def _read_actors_interactive() -> list[Actor]:
    actors: list[Actor] = []
    print("Актори (порожнє П.І.Б. — кінець списку):")
    while True:
        name = input("  П.І.Б. актора: ")
        if not name.strip():
            break
        role = input("  Роль у фільмі: ")
        actors.append(Actor(name, role))
    return actors


def create_film_interactive() -> Film:
    title = input("Назва фільму: ")
    genre = input("Жанр: ")
    director = input("Режисер: ")
    year = int(input("Рік випуску: "))
    duration = int(input("Тривалість (хвилини): "))
    studio = input("Студія: ")
    actors = _read_actors_interactive()
    return Film(title, genre, director, year, duration, studio, actors)


def film_catalog_menu() -> int:
    print("1) Додати фільм")
    print("2) Список фільмів (короткий шаблон)")
    print("3) Список фільмів (повний шаблон)")
    print("4) Актори обраного фільму (повний шаблон)")
    print("5) Актори обраного фільму (короткий шаблон)")
    print("6) Назад")
    return int(input("Оберіть пункт (1–6): "))


def _pick_film(model: FilmModel) -> Film | None:
    films = model.get_films()
    if not films:
        print("Немає фільмів.")
        return None
    FilmsView(model).render(FilmShortInfoTemplate())
    try:
        fid = int(input("Id фільму: "))
    except ValueError:
        print("Некоректний id.")
        return None
    f = model.get_film(fid)
    if f is None:
        print("Фільм не знайдено.")
    return f


def run_film_app(model: FilmModel, view: FilmsView) -> None:
    while True:
        try:
            choice = film_catalog_menu()
        except ValueError:
            print("Введіть число від 1 до 6.")
            continue
        match choice:
            case 1:
                try:
                    model.add_film(create_film_interactive())
                    print("Фільм додано.")
                except ValueError:
                    print("Некоректні числові поля (рік / тривалість).")
            case 2:
                view.render(FilmShortInfoTemplate())
            case 3:
                view.render(FilmFullInfoTemplate())
            case 4:
                f = _pick_film(model)
                if f:
                    ActorFullInfoTemplate().render(f.actors, f.title)
            case 5:
                f = _pick_film(model)
                if f:
                    ActorBriefInfoTemplate().render(f.actors, f.title)
            case 6:
                print("Назад у головне меню.")
                break
            case _:
                print("Невірний пункт.")


# ---------------------------------------------------------------------------
# Запуск
# ---------------------------------------------------------------------------


def main() -> None:
    _configure_console_utf8()
    recipe_model = RecipeModel()
    recipe_view = RecipesView(recipe_model)
    film_model = FilmModel()
    film_view = FilmsView(film_model)

    print("Вітаємо! У файлі — завдання 1 (MVC), 2 (MVT, рецепти) і 3 (MVT, фільми).")
    print("Рецепти вже завантажені з recipes.json (якщо файл існує).\n")

    while True:
        print("--- Головне меню ---")
        print("1) Завдання 1 — облік витрат (MVC)")
        print("2) Завдання 2 — книга рецептів (MVT)")
        print("3) Завдання 3 — каталог фільмів (MVT)")
        print("4) Вихід")
        try:
            root = int(input("Оберіть (1–4): "))
        except ValueError:
            print("Введіть число.")
            continue
        match root:
            case 1:
                run_expense_app()
            case 2:
                run_recipe_book_app(recipe_model, recipe_view)
            case 3:
                run_film_app(film_model, film_view)
            case 4:
                print("До побачення.")
                break
            case _:
                print("Невірний пункт.")


if __name__ == "__main__":
    main()
