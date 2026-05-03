from . import utils


class Product:
    id: int
    slug: str
    name: str
    description: str

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
    Product(utils.get_current_timestamp(), "first-product", "Product 1", "Description of product 0"),
    Product(utils.get_current_timestamp(), "second-product", "Product 2", "Description of product 1"),
    Product(utils.get_current_timestamp(), "third-product", "Product 3", "Description of product 2"),
    Product(utils.get_current_timestamp(), "fourth-product", "Product 4", "Description of product 3"),
]
