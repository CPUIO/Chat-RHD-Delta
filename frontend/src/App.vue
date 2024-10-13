<template>
  <div>
    <!-- Отображение всех ответов от сервера -->
    <div class="response-block">
      <div v-for="(res, index) in responses" :key="index" class="response">
        Ответ от сервера: {{ res }}
      </div>
    </div>

    <!-- Форма с полем ввода и кнопкой отправки -->
    <form @submit.prevent="sendMessage">
      <input
        type="text"
        v-model="message"
        @keyup.enter="sendMessage"
        placeholder="Введите сообщение"
      />
      <button type="submit">Отправить</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";

const question = ref(""); // Поле для ввода сообщения
const response = ref(""); // Поле для хранения ответа от сервера

const sendMessage = async () => {
  if (question.value.trim()) {
    try {
      // Используем fetch для отправки POST запроса на сервер
      const res = await fetch("http://127.0.0.1:8000/question/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: question.value }), // Отправляем сообщение в формате JSON
      });

      if (!res.ok) {
        alert(`Ошибка HTTP: ${res.status}. Проверьте подключение к интернету.`);
      }

      // Парсим JSON ответ от сервера
      const data = await res.json();

      // Добавляем новый ответ в список ответов
      responses.value.push(data.response);
    } catch (error) {
      alert(
        "Ошибка при отправке сообщения:",
        error,
        ". Произошла непредвиденная ошибка, попробуйте позже."
      );
    }
  } else {
    alert("Введите сообщение.");
  }
};
</script>

<style scoped>
.response-block {
  width: 300%;
  height: 100%;
  padding: 70%;
  background-color: #495A6E;
  border-radius: 10px;
}
</style>
