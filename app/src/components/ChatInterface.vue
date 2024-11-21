<template>

  <div class="demo-title">
    <h1>Wisetax Assignment</h1>
    <h3>Chatbot Demo</h3>
  </div>

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

async function importResume() {

  try {
    // Call Python CLI using relative path
    const response = await fetch('/import', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
    })

    // Trimming the response to make it look nice in the UI
    const data = await response.json() as ApiResponse;
    messages.value.push({
      role: 'assistant',
      content: data.response.replace('No state file found. Creating a new one.', '')
    })
  } catch (error) {
    console.error('Error:', error)
    messages.value.push({
      role: 'assistant',
      content: 'Sorry, there was an error processing your request: ' + (error as Error).message
    })
  }
}


const sendMessage = async (): Promise<void> => {
  if (!currentMessage.value.trim()) return

  // Add user message
  messages.value.push({
    role: 'user',
    content: currentMessage.value
  })

  try {
    // Call Python CLI using relative path
    const response = await fetch('/ask', {
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

importResume()

// Auto-scroll to bottom when new messages arrive
watch(() => messages.value.length, () => {
  setTimeout(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  }, 0)
})
</script>
