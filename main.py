from fastapi import FastAPI
from sqllite import run_sql

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API de Usuários - Acesse /docs para testar"}

@app.get("/users")
def read_users():
    #Retorna todos os usuários
    result = run_sql("SELECT * FROM users")
    columns = ["id_users", "name", "age"]
    users = [dict(zip(columns, row)) for row in result]
    return users

@app.post("/users")
def create_user(name: str, age: int):
    #Cria um novo usuário
    query = "INSERT INTO users (name, age) VALUES (?, ?)"
    run_sql(query, (name, age))
    return {"message": "Usuário criado com sucesso"}

@app.get("/users/{id_users}")
def read_user(id_users: int):
    #Retorna um usuário específico pelo ID
    query = "SELECT * FROM users WHERE id_users = ?"
    result = run_sql(query, (id_users,))
    
    if not result:
        return {"error": "Usuário não encontrado"}
    
    columns = ["id_users", "name", "age"]
    user = dict(zip(columns, result[0]))
    return user

@app.put("/users/{id_users}")
def update_user(id_users: int, name: str, age: int):
    #Atualiza um usuário existente
    check_query = "SELECT * FROM users WHERE id_users = ?"
    existing = run_sql(check_query, (id_users,))
    
    if not existing:
        return {"error": "Usuário não encontrado"}
    
    update_query = "UPDATE users SET name = ?, age = ? WHERE id_users = ?"
    run_sql(update_query, (name, age, id_users))
    
    updated = run_sql("SELECT * FROM users WHERE id_users = ?", (id_users,))
    columns = ["id_users", "name", "age"]
    user = dict(zip(columns, updated[0]))
    return {"message": "Usuário atualizado com sucesso", "user": user}

@app.delete("/users/{id_users}")
def delete_user(id_users: int):
    #Remove um usuário
    check_query = "SELECT * FROM users WHERE id_users = ?"
    existing = run_sql(check_query, (id_users,))
    
    if not existing:
        return {"error": "Usuário não encontrado"}
    
    delete_query = "DELETE FROM users WHERE id_users = ?"
    run_sql(delete_query, (id_users,))
    
    return {"message": f"Usuário com ID {id_users} deletado com sucesso"}