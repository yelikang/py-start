<template>
  <div>
    <div v-html="markdownContent"></div>

    <ChatInput @sendMessage="sendMessage" />
  </div>
</template>



<script setup lang="ts">
import { chatRes, sseRes } from "@/api";
import { ref } from "vue";
import ChatInput from "@/components/chat-input.vue";
import markdownToHtml from "@/utils/markdown-to-html";

let content = ref("");
let markdownContent = ref("");

const getChatList = () => {
  chatRes.getChatList({ chatId: "666" }).then((res: any) => {
    console.log(res);
  });
};

const sendMessage = (_query: string) => {
  content.value = "";
  markdownContent.value = "";
  sseRes
    .sendSSE({ query: _query }, (msg: any) => {
      content.value += msg;
      // markdownContent.value = content.value;
      console.log(content.value);

      markdownToHtml(content.value).then((html: any) => {
        markdownContent.value = html;
      });
    })
    .then(() => {
      console.log("结束");
    });
};
</script>

<style scoped>
</style>
