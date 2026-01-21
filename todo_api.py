from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  # 新增：数据校验，更规范
import sqlite3
from contextlib import contextmanager  # 新增：安全管理数据库连接

# 1. 初始化 FastAPI 应用
app = FastAPI(title="Todo API", version="1.0")

# 2. 定义数据模型（新增：替代原有的 dict，实现参数校验）
class TodoItem(BaseModel):
    title: str
    completed: bool = False  # 默认未完成

# 3. 数据库连接管理（新增：避免连接泄露，更健壮）
@contextmanager
def get_db_connection():
    conn = None
    try:
        # 连接数据库（不存在会自动创建）
        conn = sqlite3.connect("todo.db")
        # 启用行工厂，查询结果可以用字段名访问
        conn.row_factory = sqlite3.Row
        yield conn
    finally:
        if conn:
            conn.close()

# 4. 初始化数据库表（新增：首次运行自动创建表，解决"表不存在"报错）
def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # 创建 todos 表，id 自增为主键
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        """)
        conn.commit()

# 启动时初始化数据库
init_db()

# 5. 接口实现（修复原代码的问题）
@app.get("/todos", summary="获取待办事项列表")
async def read_todos(q: str = "", skip: int = 0, limit: int = 100):
    """
    获取待办事项列表，支持模糊搜索、分页
    - q: 按标题模糊搜索（可选）
    - skip: 跳过前 N 条（默认0）
    - limit: 返回条数（默认100）
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # 修复原代码：添加分页，避免返回所有数据
        cursor.execute("""
            SELECT id, title, completed FROM todos 
            WHERE title LIKE ? 
            LIMIT ? OFFSET ?
        """, (f"%{q}%", limit, skip))
        results = cursor.fetchall()
        # 转换为字典列表，更易读
        todos = [{"id": r["id"], "title": r["title"], "completed": bool(r["completed"])} for r in results]
    return {"todos": todos, "count": len(todos)}

@app.post("/todos", summary="创建待办事项")
async def create_todo(item: TodoItem):
    """创建新的待办事项"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO todos (title, completed) VALUES (?, ?)",
            (item.title, item.completed)
        )
        conn.commit()
        # 返回新建项的ID，更实用
        return {"message": "Todo created successfully!", "todo_id": cursor.lastrowid}

@app.put("/todos/{todo_id}", summary="更新待办事项")
async def update_todo(todo_id: int, item: TodoItem):
    """更新指定ID的待办事项"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # 先检查项是否存在
        cursor.execute("SELECT id FROM todos WHERE id = ?", (todo_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Todo not found")
        # 更新数据
        cursor.execute(
            "UPDATE todos SET title=?, completed=? WHERE id=?",
            (item.title, item.completed, todo_id)
        )
        conn.commit()
    return {"message": "Todo updated successfully!", "todo_id": todo_id}

@app.delete("/todos/{todo_id}", summary="删除待办事项")
async def delete_todo(todo_id: int):
    """删除指定ID的待办事项"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # 先检查项是否存在
        cursor.execute("SELECT id FROM todos WHERE id = ?", (todo_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Todo not found")
        # 删除数据
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
    return {"message": "Todo deleted successfully!", "todo_id": todo_id}

# 6. 根路径（新增：测试接口是否正常运行）
@app.get("/", summary="健康检查")
async def root():
    return {"message": "Todo API is running!", "docs_url": "/docs"}