<template>
  <div class="chat-input">
    <a-textarea
      v-model:value="message"
      placeholder="请输入内容"
      :auto-size="{ minRows: 2, maxRows: 5 }"
    />
    <div class="chat-input__button">
      <a-button type="primary" @click="sendMessage">发送</a-button>
      <a-button type="default" @click="clearMessage">清空</a-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineEmits } from "vue";

const message = ref<string>("帮我写一个200字小说");
const emit = defineEmits(["sendMessage", "clearMessage"]);
const sendMessage = () => {
  emit("sendMessage", message.value);
};
const clearMessage = () => {
  emit("clearMessage");
};
</script>

<style scoped lang="less">
.chat-input {
  &__button {
    display: flex;
    justify-content: flex-end;
    margin-top: 10px;
    button{
      margin-left: 10px;
    }
  }
}
</style>