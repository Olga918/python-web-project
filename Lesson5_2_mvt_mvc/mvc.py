# MVC -> Model -> View -> Controller

# View(Froms, Input, Buttons)
# Controller -> Model
# |
# View

"""
class Product(Model):
    id = Guid(UUID)
    name = TEXT
    price = DECIMAL
    description = TEXT

DAO -> Data Access Object -> CRUD(Create, Read, Update, Delete)
"""

from datetime import datetime

def get_current_timestamp():
    return int(datetime
               .timestamp(
                   datetime.now()
               ))

def get_date_now():
    return str(datetime
               .now())

# Entity
class Task:
    __id: int
    header: str
    description: str
    date: str
    def __init__(self, _header, _description):
        self.__id = get_current_timestamp()
        self.header = _header
        self.description = _description
        self.date = get_date_now()
        
    @property
    def id(self):
        return self.__id
    
    def __str__(self):
        return f"TaskId: {self.id}\nHeader: {self.header}\nDescription: {self.description}\nDate: {self.date}"

class Model:
    def __init__(self):
        self.tasks = []
        
    def add_task(self, task:Task):
        self.tasks.append(task)
        
    def get_task(self, id)->Task: 
        if len(self.tasks) < 1: return None
        for i in self.tasks:
            if i.id == id:
                return i
        return None
    
    def update_task(self, id ,task:Task):
        _task = self.get_task(id)
        if not _task: return False
        _task.header = task.header
        _task.description = task.description
        return True
    
    def delete_task(self, id):
        _task = self.get_task(id)
        if not _task: return False
        self.tasks.remove(_task)
        return True  
    
    def get_tasks(self):
        return self.tasks
    
class View:
    def show_menu(self):
        print("1) Show all tasks")
        print("2) Show task by id")
        print("3) Create new task")
        print("4) Update task")
        print("5) Delete task")
        print("6) Exit")
        return int(input("Select menu item, enter value 1-5: "))
    
    def show_message(self, message: str):
        print(message)
    
    def create_task(self)->Task:
        header = input("Enter header for task: ")
        description = input("Enter description of task: ")
        return Task(header, description)
    def update_task(self, tasks)-> tuple:
        self.show_tasks(tasks)
        id = input("Choose task for update(enter id): ")
        header = input("Enter new header for task: ")
        description = input("Enter new description of task: ")
        return (int(id), Task(header, description))
    def delete_task(self, tasks)->int:
        self.show_tasks(tasks)
        return int(input("Choose task for delete(enter id): "))
    def show_tasks(self, tasks):
        for task in tasks:
            print("-"*30)
            print(task)
            print("-"*30,"\n")
    def show_task(self):
        return int(input("Choose task(enter id): "))

class Controller:
    def __init__(self, model: Model, view:View):
        self.model = model
        self.view = view
    def action_create_task(self):
        task = self.view.create_task()
        self.model.add_task(task)
        self.view.show_message("Task created!")
    def action_update_task(self):
        (id, task) = self.view.update_task(self.model.get_tasks())
        result = self.model.update_task(id, task)
        if result:
            self.view.show_message("Update task successfully!")
        else: self.view.show_message("Update task failed!")
    def action_delete_task(self):
        delete_id = self.view.delete_task(self.model.get_tasks())
        if self.model.delete_task(delete_id):
            self.view.show_message("Delete task successfully!")
        else: self.view.show_message("Delete task failed!")
    
    def action_show_tasks(self):
        self.view.show_tasks(self.model.get_tasks())
    
    def action_show_task(self):
        id = self.view.show_task()
        task = self.model.get_task(id)
        self.view.show_message(str(task))
    

app = Controller(Model(), View())

while True:
    result = app.view.show_menu()
    
    match result:
        case 1:
            app.action_show_tasks()
        case 2:
            app.action_show_task()
        case 3:
            app.action_create_task()
        case 4:
            app.action_update_task()
        case 5: 
            app.action_delete_task()
        case 6:
            print("Exit!")
            break
        case _:
            print("Wrong menu item!")