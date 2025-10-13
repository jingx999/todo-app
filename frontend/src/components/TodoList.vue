<template>
    <div style="max-width: 600px; margin: 2rem auto; padding: 1rem;">
        <h1>📝 Todo List</h1>

        <form @submit.prevent="addTodo">
            <input
                v-model="newTodo"
                type="text"
                placeholder="输入新的待做事项..."
                style="padding: 0.5rem; width: 70%; margin-right: 0.5rem;">
            <button type="submit" style="padding: 0.5rem 1rem;">添加</button>
        </form>

        <ul style="margin-top: 1rem; list-style: none; padding: 0;">
            <li
                v-for="todo in todos"
                :key="todo.id"
                style="padding: 0.5rem; border-bottom: 1px solid #eee; display: flex; justify-content: space-between;"
            >
                <span
                    :style="{ textDecoration: todo.done ? 'line-through' : 'none', color: todo.done ? '#888' : '#000' }"
                    @click="toggleTodo(todo.id)"
                >
                    {{ todo.title }}
                </span>
                <button @click="deleteTodo(todo.id)" style="color: red; background: none; border: none; cursor: pointer;">
                    ❌
                </button>
            </li>
        </ul>
    </div>
</template>

<script>
import axios from 'axios'

const API_BASE = 'http://localhost:5000/api'

export default {
    data() {
        return {
            todos: [],
            newTodo: ''
        }
    },
    async mounted() {
        await this.loadTodos()
    },
    methods: {
        async loadTodos() {
            const res = await axios.get(`${API_BASE}/todos`)
            this.todos = res.data
        },
        async addTodo() {
            if (!this.newTodo.trim()) return
            const res = await axios.post(`${API_BASE}/todos`, {title: this.newTodo})
            this.todos.push(res.data)
            this.newTodo = ''
        },
        async toggleTodo(id) {
            const todo = this.todos.find(t => t.id === id)
            const res = await axios.put(`${API_BASE}/todos/${id}`)
            todo.done = res.data.done
        },
        async deleteTodo(id) {
            await axios.delete(`${API_BASE}/todos/${id}`)
            this.todos = this.todos.filter(t => t.id !== id)
        }
    }
}
</script>