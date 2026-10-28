from connection import * 
        
async def create_task(title, caption, due_date, telegram_id):
    try:
        conn = await connection_db()
        await conn.execute("""
            insert into tasks (title, caption, due_date, telegram_id) values
            ($1, $2, $3, $4)
        """, title, caption, due_date, str(telegram_id))
        return True
    except Exception as error:
        print(f"Create task Error: {error}")
        return False
    finally:
            await conn.close()


async def get_task():
    try:
        conn = await connection_db() 
        tasks = await conn.fetch("""
            select * from tasks git 
            """) 
        return tasks 
    except Exception as error: 
            print(f"Get task Error: {error}")  
    finally: 
            await conn.close()  
        
        
async def update_task(task_id,title,caption,due_date):
    try:
        conn = await connection_db()
        await conn.execute(
            """
            update tasks
            set title = $1,
            caption = $2,
            due_date = $3
            where task_id = $4
            """,
            title, caption, due_date, int(task_id)
            )
        print("Task updated succesfully!")
    except Exception as error:
        print(f"Update task error: {error}")
    finally:
            await conn.close()
            
            
            
async def delete_task(task_id):
    try:
        conn = await connection_db()
        await conn.execute("""
            delete from tasks
            where task_id = $1
        """, task_id)
        print("Task deleted successfully!")
    except Exception as error:
        print(f"Delete task error: {error}")
    finally:
            await conn.close()