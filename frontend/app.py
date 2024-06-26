import streamlit as st
import httpx
from datetime import date, datetime
import os
import json

# Set the base URL of your backend API
API_BASE_URL = os.getenv('BACKEND_URL', 'http://localhost:8080')


def get_tasks():
    try:
        with httpx.Client() as client:
            response = client.get(f"{API_BASE_URL}/todo/getfullist")
            if response.status_code == 200:
                return response.json()
            else:
                return None
    except Exception as e:
        raise Exception(f"Failed to retrieve tasks: {e}")
    

def search_tasks(title: str):
    try:
        with httpx.Client() as client:
            response = client.get(f"{API_BASE_URL}/todo/searchtasks?title={title}")
            if response.status_code == 200:
                return response.json()
            else:
                return None
    except Exception as e:
        raise Exception(f"Failed to retrieve tasks: {e}")


def add_task(title: str, description: str, priority: str, due_date: date):
    try:
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
    except Exception as e:
        raise Exception(f"Failed to add task: {e}")
    

def update_task(_id: str, title: str, description: str, priority: str, due_date: date):
    try:
        with httpx.Client() as client:
            due_date_str = due_date.strftime("%Y-%m-%d") if isinstance(due_date, date) else due_date
            payload = {
                "_id": _id,
                "title": title,
                "description": description,
                "priority": priority,
                "due_date": due_date_str
            }
            response = client.put(f"{API_BASE_URL}/todo/updatesingletask", json=payload)
            return response.status_code
    except Exception as e:
        raise Exception(f"Failed to update task: {e}")
    

def delete_task(_id: str):
    try:
        with httpx.Client() as client:
            response = client.delete(f"{API_BASE_URL}/todo/deletesingletask?id={_id}")
            return response.status_code
    except Exception as e:
        raise Exception(f"Failed to delete task: {e}")


def delete_task_list():
    try:
        with httpx.Client() as client:
            response = client.delete(f"{API_BASE_URL}/todo/deletefulllist")
            return response.status_code
    except Exception as e:
        raise Exception(f"Failed to delete task list: {e}")


def view_tasks(tasks):
    if len(tasks) > 0:
        for task in tasks:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    if f"edit_{task['_id']}" in st.session_state and st.session_state[f"edit_{task['_id']}"]:
                        # Make task details editable
                        title = st.text_input("Title", value=task['title'], key=f"title_{task['_id']}")
                        description = st.text_area("Description", value=task['description'], key=f"desc_{task['_id']}")
                        priority = st.selectbox("Priority", options=["LOWEST", "LOW", "MEDIUM", "HIGH", "HIGHEST"], index=["LOWEST", "LOW", "MEDIUM", "HIGH", "HIGHEST"].index(task['priority']), key=f"priority_{task['_id']}")
                        due_date = st.date_input("Due Date", value=datetime.strptime(task['due_date'], '%Y-%m-%d').date(), key=f"due_{task['_id']}")
                    else:
                        # Display task details
                        st.write(f"Title: {task['title']}")
                        st.write(f"Description: {task['description']}")
                        st.write(f"Priority: {task['priority']}")
                        st.write(f"Due Date: {task['due_date']}")

                with col2:
                    if st.button("Update", key=f"update_{task['_id']}"):
                        # Enable editing mode
                        st.session_state[f"edit_{task['_id']}"] = True
                        # Refresh to show editable fields
                        st.rerun()  
                    # Display Confirm button only if edit mode is enabled for this task
                    if st.session_state.get(f"edit_{task['_id']}", False):
                        if st.button("Confirm", key=f"confirm_{task['_id']}"):
                            # Call update_task with new details
                            update = update_task(_id=task['_id'], title=st.session_state[f"title_{task['_id']}"], description=st.session_state[f"desc_{task['_id']}"], priority=st.session_state[f"priority_{task['_id']}"], due_date=st.session_state[f"due_{task['_id']}"])
                            if update == 200:
                                st.success("Task updated successfully!")
                            else:
                                st.error("An error occurred while updating the task. Please try again.")
                            # Disable editing mode
                            st.session_state[f"edit_{task['_id']}"] = False
                            # Refresh to show updated tasks
                            st.rerun()

                with col3:
                    if st.button("Delete", key=f"delete_{task['_id']}"):
                        delete = delete_task(_id=task['_id'])
                        if delete == 200:
                            tasks.remove(task)
                            st.rerun()  # Refresh to show updated tasks list

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
        priority = st.selectbox("Priority", ["LOWEST", "LOW", "MEDIUM", "HIGH", "HIGHEST"])
        due_date = str(st.date_input("Due Date"))
        submit_button = st.form_submit_button("Add Task")
        if submit_button:
            status_code = add_task(title, description, priority, due_date)
            if status_code == 200:
                st.success("Task added successfully!")
            else:
                st.error("An error occurred while adding the task. Please try again.")


# Search tasks in task list
elif st.session_state.current_view == "search_tasks":
    st.subheader("Search Tasks")
    task_title = st.text_input("Enter task title to search")
    if task_title:
        tasks = search_tasks(task_title)
        if tasks:
            view_tasks(tasks)
        else:
            st.error("There are no tasks contain this title.")


# Display existing tasks
elif st.session_state.current_view == "view_tasks":
    st.subheader("Tasks")
    if st.button('Delete Task List'):
        delete_task_list()
        st.success('Task list deleted successfully!')
    tasks = get_tasks()
    view_tasks(tasks)