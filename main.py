from datetime import datetime

class Entity:
    _id_counter = 0
    def __init__(self, created_at = None, updated_at = None):
        Entity._id_counter += 1
        self._id = Entity._id_counter
        self._created_at = created_at or datetime.now()
        self._updated_at = updated_at or datetime.now()

    @property
    def id(self):
        return self._id

class Task(Entity):
    def __init__(self, title, description = "", status = "In progress", deadline = "", assignee = None, created_at = datetime.now(), updated_at = datetime.now()):
        super().__init__(created_at, updated_at)
        self._title = title
        self._description = description
        self._status = status
        self._deadline = deadline
        self._assignee = assignee # User

    def get_details_string(self):
        return f'{self._id}: ({self._status}) | {self._assignee.name} | {self._title}: {self._description}'

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def description(self):
        return self._description

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def assignee(self):
        return self._assignee

    @assignee.setter
    def assignee(self, value):
        self._assignee = value


class User(Entity):
    def __init__(self, name, email, created_at = datetime.now(), updated_at = datetime.now()):
        super().__init__(created_at, updated_at)
        self._name = name
        self._email = email

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

class Project(Entity):
    def __init__(self, name, created_at = datetime.now(), updated_at = datetime.now(), tasks=None, members=None):
        super().__init__(created_at, updated_at)
        if tasks is None:
            tasks = []
        if members is None:
            members = []
        self._name = name
        self._tasks = tasks #List[Task]
        self._members = members #List[User]

    @property
    def name(self):
        return self._name

    @property
    def tasks(self):
        return self._tasks

    def append_task(self, task):
        self._tasks.append(task)

    def print_project_tasks(self):
        print(f'Project {self._name} current tasks:')
        for task in self._tasks:
            print(task.get_details_string())
        print("\n")

class TaskFlowApp:
    def __init__(self):
        self.projects = []
        self.users = []

    def create_project(self, project_name):
        self.projects.append(Project(project_name))

    def print_list_of_projects(self):
        for project in self.projects:
            print(f'{project.id}. {project.name}')


def print_menu():
    print(
        "\n1. Create project.\n"
        "2. Create users\n"
        "3. Add tasks\n"
        "4. List tasks\n"
        "5. Assign tasks to users\n"
        "6. Filter tasks by user or status\n"
        "7. Mark tasks complete\n"
    )

def create_project_menu():
    print("CREATE PROJECT")
    project_name = input("Project name:")
    app.create_project(project_name)
    print("Project created!")
    print("Current projects list:")
    app.print_list_of_projects()
    enter_main_menu()

def add_tasks_menu():
    if len(app.projects) == 0:
        print("No projects. Create a project first.")
        enter_main_menu()
        return
    else:
        app.print_list_of_projects()

    while True:
        current_project_id = input("Enter current project id:")
        if not current_project_id.isdigit():
            print("Project id is not a number.")
            add_tasks_menu()
        else:
            break
    current_project_id = int(current_project_id)
    found_project = False
    for project in app.projects:
        if project.id == current_project_id:
            found_project = True
            create_task(project)
            enter_main_menu()
            break

    if found_project is False:
        print("Project not found.")
        add_tasks_menu()


def get_assignee_for_task():
        print_list_of_current_users()
        while True:
            assignee_id = input("Choose an assignee for the task by entering his ID:")
            if not assignee_id.isdigit():
                print("User id is not a number.")
                add_tasks_menu()
            else:
                break

        assignee_id = int(assignee_id)
        task_assignee = None
        for user in app.users:
            if user.id == assignee_id:
                task_assignee = user

        return task_assignee

def create_task(project):
    task_title = input("Enter task title:")
    task_description = input("Enter task description:")
    while True:
        task_assignee = get_assignee_for_task()
        if task_assignee is not None:
            break
        print("Enter a valid user id")
    project.append_task(Task(title = task_title, description = task_description, assignee = task_assignee))
    project.print_project_tasks()

def print_list_of_current_users():
    for user in app.users:
        print(f'{user.id}:{user.name}, {user.email}')

def create_users_menu():
    user_name = input("Enter user name: ")
    user_email = input("Enter user email: ")
    app.users.append(User(user_name,user_email))
    print("\nCurrent users:")
    print_list_of_current_users()
    enter_main_menu()

def list_all_tasks():
    print("List of current tasks in all projects:")
    for project in app.projects:
        project.print_project_tasks()

def list_all_tasks_menu():
    list_all_tasks()
    enter_main_menu()

def assign_tasks_to_users():
    if len(app.projects) == 0:
        print("No active projects. Create a project first.")
        enter_main_menu()
        return

    if len(app.users) == 0:
        print("No users registered. Add a user first.")
        enter_main_menu()
        return

    list_all_tasks()
    all_tasks_list = []
    selected_task = None
    while True:
        current_task_id = input("Choose a task id:")
        if not current_task_id.isdigit():
            print("Task id is not a number.")
            assign_tasks_to_users()
            break

        for project in app.projects:
            all_tasks_list += project.tasks

        for task in all_tasks_list:
            if int(task.id) == int(current_task_id):
                selected_task = task
                break

        if selected_task is None:
            print("Task not found.")
        else:
            print(f'Select a user for the {selected_task.id}: {selected_task.title} task.')
            break

    print_list_of_current_users()
    selected_user = None
    found_user = False
    while True:
        current_user_id = input("Select a user for the task: ")
        if not current_user_id.isdigit():
            print("User id is not a number")
            continue
        for user in app.users:
            if user.id == int(current_user_id):
                found_user = True
                selected_user = user
                break

        if not found_user:
            print("User id not found.")
            continue
        else:
            break

    if selected_user is None:
        print("ERROR: Failed to set task assignee")
        enter_main_menu()
        return

    selected_task.assignee = selected_user
    print("Updated task:\n", selected_task.get_details_string())
    enter_main_menu()

def filter_task_by_user_or_status_menu():
    if len(app.projects) == 0:
        print("No active projects. Create a project first.")
        enter_main_menu()
        return

    print("Filter task:\n","1.By user\n","2.By status")
    selected_user = None
    while True:
        option = input("Choose an option:")
        if not option.isdigit():
            print("Option is not a number")
        elif int(option) == 1 or int(option) == 2:
            break
        else:
            print("Invalid option")


    if int(option) == 1:
        if len(app.users) == 0:
            print("No users registered. Add a user first.")
            enter_main_menu()
            return

        print_list_of_current_users()
        found_user = False
        while True:
            current_user_id = input("Select a user: ")
            if not current_user_id.isdigit():
                print("User id is not a number")
                continue
            for user in app.users:
                if user.id == int(current_user_id):
                    found_user = True
                    selected_user = user
                    break

            if not found_user:
                print("User id not found.")
                continue
            else:
                break

        if selected_user is None:
            print("ERROR: Failed to set task assignee.")
            enter_main_menu()
            return


        for project in app.projects:
            project_tasks = project.tasks
            for task in project_tasks:
                if task.assignee == selected_user:
                    print(task.get_details_string())
        enter_main_menu()
    elif int(option) == 2:
        if len(app.users) == 0:
            print("No users registered. Add a user first.")
            enter_main_menu()
            return

        print("1. In progress\n", "2. Done")
        while True:
            status_option = input("Enter a option:")
            if not status_option.isdigit():
                print("User id is not a number")
                continue

            if int(status_option) == 1:
                show_tasks_by_status("In progress")
                enter_main_menu()
                return
            elif int(status_option) == 2:
                show_tasks_by_status("Done")
                enter_main_menu()
                return
            else:
                print("Invalid option")
                continue

        enter_main_menu()
    else:
        print("ERROR:Invalid filter option.")
        enter_main_menu()


def show_tasks_by_status(status):
    for project in app.projects:
        project_tasks = project.tasks
        for task in project_tasks:
            if task.status == status:
                print(task.get_details_string())

def mark_tasks_complete_menu():
    tasks_list = []
    for project in app.projects:
        tasks_list += project.tasks

    if len(tasks_list) == 0:
        print("No active tasks. Add a task first.")
        enter_main_menu()
        return

    selected_task = None
    for task in tasks_list:
        print(task.get_details_string())

    while True:
        selected_task_id = input("Choose a task by id:")
        if not selected_task_id.isdigit():
            print("Task id is not a number")
            continue
        for task in tasks_list:
            if task.id == int(selected_task_id):
                selected_task = task
                break

        if selected_task is not None:
            selected_task.status = "Done"
            print(f'Updated task:\n'
                  f'{selected_task.get_details_string()}')
            enter_main_menu()
            break
        else:
            print("Invalid task id.")


def handle_main_menu_option(option):
    match option:
        case 1:
            create_project_menu()
        case 2:
            create_users_menu()
        case 3:
            add_tasks_menu()
        case 4:
            list_all_tasks_menu()
        case 5:
            assign_tasks_to_users()
        case 6:
            filter_task_by_user_or_status_menu()
        case 7:
            mark_tasks_complete_menu()
        case _:
            pass


def enter_main_menu():
    while True:
        print_menu()
        option = input("Enter option number:")
        if not option.isdigit()  or int(option) < 1 or int(option) > 7:
            print("ERROR: Invalid option")
        else:
            handle_main_menu_option(int(option))
            break

app = TaskFlowApp()
enter_main_menu()
