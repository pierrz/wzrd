<template>
  <div class="chat-container">
    <div class="chat-messages" ref="messagesContainer">
      <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
        <div class="message-content">{{ message.content }}</div>
      </div>
    </div>
    <div class="input-container">
      <input 
        v-model="currentMessage" 
        @keyup.enter="sendMessage"
        placeholder="Type your message here..."
        type="text"
      >
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

interface ApiResponse {
  response: string
}

const messages = ref<Message[]>([])
const currentMessage = ref('')
const messagesContainer = ref<HTMLDivElement | null>(null)

const sendMessage = async (): Promise<void> => {
  if (!currentMessage.value.trim()) return

  // Add user message
  messages.value.push({
    role: 'user',
    content: currentMessage.value
  })

  try {
    // Call Python CLI
    const response = await fetch('http://localhost:5000/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        question: currentMessage.value
      })
    })

    const data = await response.json() as ApiResponse

    // Add assistant response
    messages.value.push({
      role: 'assistant',
      content: data.response
    })
  } catch (error) {
    console.error('Error:', error)
    messages.value.push({
      role: 'assistant',
      content: 'Sorry, there was an error processing your request: ' + (error as Error).message
    })
  }

  currentMessage.value = ''
}

// Auto-scroll to bottom when new messages arrive
watch(() => messages.value.length, () => {
  setTimeout(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  }, 0)
})
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.chat-messages {
  flex-grow: 1;
  overflow-y: auto;
  margin-bottom: 20px;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
}

.message {
  margin-bottom: 20px;
  padding: 12px 16px;
  border-radius: 8px;
  max-width: 80%;
}

.message.user {
  background: #007AFF;
  color: white;
  margin-left: auto;
}

.message.assistant {
  background: #E9ECEF;
  color: #212529;
  margin-right: auto;
}

.input-container {
  display: flex;
  gap: 10px;
}

input {
  flex-grow: 1;
  padding: 12px;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-size: 16px;
}

button {
  padding: 12px 24px;
  background: #007AFF;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover {
  background: #0056b3;
}
</style>
