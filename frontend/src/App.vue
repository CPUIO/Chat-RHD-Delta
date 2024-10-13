<template>
  <div>
    <!-- Отображение всех сообщений (как пользователя, так и сервера) -->
    <div class="response-block">
      <div
        v-for="(message, index) in chatMessages"
        :key="index"
        :class="message.role"
      >
        <p>{{ message.role === "user" ? "Вы" : "Сервер" }}:</p>
        {{ message.text }}
      </div>
    </div>

    <!-- Форма с полем ввода и кнопкой отправки -->
    <form @submit.prevent="sendMessage">
      <input
        type="text"
        v-model="question"
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
const chatMessages = ref([]); // Поле для хранения ответа от сервера

const sendMessage = async () => {
  if (question.value.trim()) {
    chatMessages.value.push({ role: "user", text: question.value });
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

      // Добавляем ответ сервера в список чата
      chatMessages.value.push({ role: "bot", text: data.response });

      question.value = "";
    } catch (error) {
      alert(
        "Произошла непредвиденная ошибка при отправке сообщения, попробуйте позже.",
        error
      );
    }
  } else {
    alert("Введите сообщение.");
  }
};
</script>

<style scoped>
.response-block {
  width: 100%;
  height: 100%;
  padding: 20vh;
  background-color: bisque;
}
</style>
