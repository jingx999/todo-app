import os
from flask import Flask, request, jsonify
from models import db, Todo
from flask_cors import CORS


# 获取当前文件所在的目录
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# 使用绝对路径构建数据库文件路径
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'instance', 'todo.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 允许前端跨域请求
CORS(app)
db.init_app(app)


# 确保 instance 目录存在
instance_path = os.path.join(basedir, "instance")
os.makedirs(instance_path, exist_ok=True)


@app.route("/")
def index():
    return "sssss"


# 获取所有 todos
@app.route("/api/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return jsonify([t.to_dict() for t in todos])


# 添加 todo
@app.route("/api/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    new_todo = Todo(title=data["title"], done=False)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201


# 更新 todo
@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.done = not todo.done
    db.session.commit()
    return jsonify(todo.to_dict())


# 删除 todo
@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200


if __name__ == "__main__":
    # 在应用上下文中创建数据库表
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5000)
