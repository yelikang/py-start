<template>
  <div>
    <a-textarea
      v-model:value="message"
      placeholder="请输入内容"
      :auto-size="{ minRows: 2, maxRows: 5 }"
    />
    <button @click="sendMessage">发送</button>
  </div>
</template>

<script setup lang="ts">
import { ref, defineEmits } from "vue";

const message = ref<string>("帮我写一个200字小说");
const emit = defineEmits(["sendMessage"]);
const sendMessage = () => {
  emit("sendMessage", message.value);
};
</script>