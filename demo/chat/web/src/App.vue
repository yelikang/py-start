<template>
  <div>
    <ui-chat-list :messages="chatList"></ui-chat-list>

    <!-- <div v-html="markdownContent"></div> -->
    <ChatInput @sendMessage="sendMessage" @clearMessage="clearMessage" />
  </div>
</template>



<script setup lang="ts">
import { chatRes, sseRes } from "@/api";
import { ref, onMounted } from "vue";
import ChatInput from "@/components/chat-input.vue";
import UiChatList from "@/components/ui/ui-chat-list.vue";
import { cache } from "@/utils/cache";
let chatList = ref([]);

const getChatList = () => {
  chatRes.getChatList().then((res: any) => {
    chatList.value = res;
  });
};

const sendMessage = async (_query: string) => {
  const userMessage = {
    role: "user",
    content: _query,
  };

  const history = cache.get("chat_messages", []);

  await chatRes.createMessage(userMessage);
  chatList.value.push(userMessage);


  await sseRes.sendSSE({ query: _query, history }, async (msg: any) => {
    const history = cache.get("chat_messages", []);
    const lastMessage = history[history.length - 1];

    // 判断最后一条消息是否是用户消息
    if (lastMessage.role === "user") {
      // 如果是用户消息，则添加回复信息
      const content = msg;
      const assistantMessage: any = {
        role: "assistant",
        content,
      };
      await chatRes.createMessage(assistantMessage);
      chatList.value.push(assistantMessage);
    } else if (lastMessage.role === "assistant") {

      lastMessage.content += msg;
      await chatRes.updateChatList(history);

      // 如果是回复信息，则更新回复信息
      const ulLastMessage: any = chatList.value[chatList.value.length - 1];
      ulLastMessage.content += msg;
    }
  });
};

const clearMessage = () => {
  chatRes.clearChatList();
  getChatList();
};

onMounted(() => {
  getChatList();
});
</script>

<style scoped>
</style>
