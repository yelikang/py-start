<template>
  <div>
    <div v-html="content"></div>

    <ChatInput @sendMessage="sendMessage" />
  </div>
</template>



<script setup lang="ts">
import { chatRes } from "@/api";
import { ref } from "vue";
import ChatInput from "@/components/chat-input.vue";

let content = ref("");

const getChatList = () => {
  chatRes.getChatList({ chatId: "666" }).then((res: any) => {
    console.log(res);
  });
};

const sendMessage = (_query: string) => {
  chatRes.ask({ query: _query }).then((res: any) => {
    content.value = res?.data?.content;
  });
};
</script>

<style scoped>
</style>
