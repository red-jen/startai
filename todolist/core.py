from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Boolean, Enum
from datetime import datetime

engine = create_engine('postgresql://postgres:Ren-ji24@localhost:5432/to_do_list')
meta = MetaData()
meta.reflect(bind=engine)

Todo = meta.tables['todos']
# Todo = Table(
#     "todos",
#     meta,
#     Column('id', Integer, primary_key=True),
#     Column('name', String(225)),
#     Column('description', Text),
#     Column('status', Boolean, default=False)  
# )


# with engine.begin() as conn:

#     meta.create_all(conn)  


def add_todo(name, description, status, priority=0):
    with engine.begin() as conn:
        result = conn.execute(Todo.insert().values(name=name, description=description, status=status, priority=priority))
        return result.inserted_primary_key[0]

def get_all_todos():
    with engine.begin() as conn:
        result = conn.execute(Todo.select())
        return result.fetchall()

def update_todo_status(todo_id, status):
    with engine.begin() as conn:
        conn.execute(Todo.update().where(Todo.c.id == todo_id).values(status=status))

def delete_todo(todo_id):
    with engine.begin() as conn:
        conn.execute(Todo.delete().where(Todo.c.id == todo_id))
def update_task_details(task_id, name, description, priority=None):
    with engine.begin() as conn:
        update_values = {'name': name, 'description': description}
        if priority is not None:
            update_values['priority'] = priority
        conn.execute(
            Todo.update()
            .where(Todo.c.id == task_id)
            .values(**update_values)
        )

def update_todo_priority(todo_id, priority):
    with engine.begin() as conn:
        conn.execute(Todo.update().where(Todo.c.id == todo_id).values(priority=priority))

def get_todos_by_priority(ascending=True):
    with engine.begin() as conn:
        order_by = Todo.c.priority.asc() if ascending else Todo.c.priority.desc()
        result = conn.execute(Todo.select().order_by(order_by))
        return result.fetchall()

def get_todos_by_status(status):
    with engine.begin() as conn:
        result = conn.execute(Todo.select().where(Todo.c.status == status))
        return result.fetchall()


