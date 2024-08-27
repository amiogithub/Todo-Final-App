import functions
import time
import PySimpleGUI as me
import os

if not os.path.exists("todos.txt"):
    with open("todos.txt", "w") as file:
        pass

def update_clock():
    return time.strftime("%b %d, %Y %H:%M:%S")

def show_congratulations():
    me.popup("Congratulations!",
             "Good job completing your task!!",
             title="Well Done!",
             font=('Helvetica', 15))

# Define custom styles
def custom_button(text, key, color, hover_color, tooltip):
    return me.Button(
        text,
        button_color=('white', color),
        font=('Helvetica', 12, 'bold'),
        size=(8, 2),  # Adjust size for visual appeal
        key=key,
        tooltip=tooltip,
        border_width=2,
        mouseover_colors=hover_color
    )

add_button = custom_button(
    "Add", "Add", "#2E8B57", "#3CB371", "Add Todo"
)

edit_button = custom_button(
    "Edit", "Edit", "#FFA500", "#FFD700", "Edit Todo"
)

complete_button = custom_button(
    "Complete", "Complete", "#DC143C", "#FF6347", "Complete Todo"
)

exit_button = custom_button(
    "Exit", "Exit", "#4682B4", "#4169E1", "Exit"
)

input_box = me.InputText(tooltip="Enter todo", key='todo')
list_box = me.Listbox(values=functions.get_todos(), key='todos', enable_events=True, size=[45, 10])

layout = [
    [me.Text("", size=(20, 1), key='clock', font=('Helvetica', 14, 'bold'), background_color='black', text_color='white')],
    [me.Text("Type in a to-do", size=(20, 1), font=('Helvetica', 12), background_color='black', text_color='white')],
    [input_box, add_button],  # Space between input_box and add_button
    [list_box, edit_button, complete_button],  # Align buttons next to the list_box
    [exit_button]
]

window = me.Window("My To-Do App", layout=layout, font=('Helvetica', 12), background_color='black')

while True:
    event, values = window.read(timeout=1000)  # Update every second
    window["clock"].update(update_clock())
    print(event)
    print(values)
    match event:
        case "Add":
            todos = functions.get_todos()
            new_todo = values['todo'] + "\n"
            todos.append(new_todo)
            functions.write_todos(todos)
            window['todos'].update(values=todos)

        case "Edit":
            try:
                todo_to_edit = values['todos'][0]
                new_todo = values['todo']

                todos = functions.get_todos()
                index = todos.index(todo_to_edit)
                todos[index] = new_todo
                functions.write_todos(todos)
                window['todos'].update(values=todos)
            except IndexError:
                me.popup("Select an item first", font=('Helvetica', 15))

        case "Complete":
            try:
                todo_to_complete = values['todos'][0]
                todos = functions.get_todos()
                todos.remove(todo_to_complete)
                functions.write_todos(todos)
                window['todos'].update(values=todos)
                window['todo'].update(value='')
                show_congratulations()  # Show popup after completing a todo
            except IndexError:
                me.popup("Select an item first", font=('Helvetica', 15))

        case "Exit":
            break

        case 'todos':
            window['todo'].update(value=values['todos'][0])

        case me.WINDOW_CLOSED:
            break

window.close()
