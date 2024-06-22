import streamlit as st
import httpx
from datetime import date, datetime
import os

# Set the base URL of your backend API
API_BASE_URL = os.getenv('BACKEND_URL')


def get_tasks():
    with httpx.Client() as client:
        response = client.get(f"{API_BASE_URL}/todo/getfullist")
        return response.json()
    

def search_tasks(title: str):
    with httpx.Client() as client:
        response = client.get(f"{API_BASE_URL}/todo/searchtasks?title={title}")
        return response.json()


def add_task(title: str, description: str, priority: str, due_date: date):
    with httpx.Client() as client:
        due_date_str = due_date.strftime("%Y-%m-%d") if isinstance(due_date, date) else due_date
        payload = {
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date_str
        }
        response = client.post(f"{API_BASE_URL}/todo/addtask", json=payload)
        return response.status_code
    

def update_task(id: int, title: str, description: str, priority: str, due_date: date):
    with httpx.Client() as client:
        due_date_str = due_date.strftime("%Y-%m-%d") if isinstance(due_date, date) else due_date
        payload = {
            "id": id,
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date_str
        }
        response = client.put(f"{API_BASE_URL}/todo/updatesingletask", json=payload)
        return response.status_code
    

def delete_task(id: int):
    with httpx.Client() as client:
        response = client.delete(f"{API_BASE_URL}/todo/deletesingletask?id={id}")
        return response.status_code


def delete_task_list():
    with httpx.Client() as client:
        response = client.delete(f"{API_BASE_URL}/todo/deletefulllist")
        return response.status_code


def view_tasks(tasks):
    for task in tasks:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                if f"edit_{task['id']}" in st.session_state and st.session_state[f"edit_{task['id']}"]:
                    # Make task details editable
                    title = st.text_input("Title", value=task['title'], key=f"title_{task['id']}")
                    description = st.text_area("Description", value=task['description'], key=f"desc_{task['id']}")
                    priority = st.selectbox("Priority", options=["1", "2", "3", "4", "5"], index=["1", "2", "3", "4", "5"].index(task['priority']), key=f"priority_{task['id']}")
                    due_date = st.date_input("Due Date", value=datetime.strptime(task['due_date'], '%Y-%m-%d').date(), key=f"due_{task['id']}")
                else:
                    # Display task details
                    st.write(f"Title: {task['title']}")
                    st.write(f"Description: {task['description']}")
                    st.write(f"Priority: {task['priority']}")
                    st.write(f"Due Date: {task['due_date']}")

            with col2:
                if st.button("Update", key=f"update_{task['id']}"):
                    # Enable editing mode
                    st.session_state[f"edit_{task['id']}"] = True
                    # Refresh to show editable fields
                    st.experimental_rerun()  
                # Display Confirm button only if edit mode is enabled for this task
                if st.session_state.get(f"edit_{task['id']}", False):
                    if st.button("Confirm", key=f"confirm_{task['id']}"):
                        # Call update_task with new details
                        update_task(id=task['id'], title=st.session_state[f"title_{task['id']}"], description=st.session_state[f"desc_{task['id']}"], priority=st.session_state[f"priority_{task['id']}"], due_date=st.session_state[f"due_{task['id']}"])
                        # Disable editing mode
                        st.session_state[f"edit_{task['id']}"] = False
                        # Refresh to show updated tasks
                        st.experimental_rerun()

            with col3:
                if st.button("Delete", key=f"delete_{task['id']}"):
                    delete_task(task['id'])  # Call delete_task function
                    st.experimental_rerun()  # Refresh to show updated tasks list

            st.markdown("---")


# Streamlit UI
st.title("Todo List Manager")

# Define the buttons for "Add Task" and "View Tasks" at the top of the page
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("View Tasks"):
        st.session_state.current_view = "view_tasks"
with col2:
    if st.button("Add Task"):
        st.session_state.current_view = "add_task"
with col3:
    if st.button("Search Tasks"):
        st.session_state.current_view = "search_tasks"

# Initialize the current_view in session state if it doesn't exist
if "current_view" not in st.session_state:
    st.session_state.current_view = "view_tasks"  # Default view


# Form to add a new task
if st.session_state.current_view == "add_task":
    with st.form("Add Task"):
        st.subheader("Add Task")
        title = st.text_input("Title")
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["1", "2", "3", "4", "5"])
        due_date = str(st.date_input("Due Date"))
        submit_button = st.form_submit_button("Add Task")
        if submit_button:
            status_code = add_task(title, description, priority, due_date)
            if status_code == 200:
                st.success("Task added successfully!")
            else:
                st.error("An error occurred while adding the task.")


# Search tasks in task list
elif st.session_state.current_view == "search_tasks":
    st.subheader("Search Tasks")
    task_title = st.text_input("Enter task title to search")
    if task_title:
        tasks = search_tasks(task_title)
        view_tasks(tasks)


# Display existing tasks
elif st.session_state.current_view == "view_tasks":
    st.subheader("Tasks")
    if st.button('Delete Task List'):
        delete_task_list()
        st.success('Task list deleted successfully!')
    tasks = get_tasks()
    view_tasks(tasks)