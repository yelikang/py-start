<template>
  <div class="ui-chat-list-item">
    <div v-html="html"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import markdownToHtml from "@/utils/markdown-to-html";

const props = defineProps({
  content: {
    type: String,
    default: "",
  },
});

const html = ref("");

watch(
  () => props.content,
  (newVal) => {
    markdownToHtml(newVal).then((res: string) => {
      html.value = res;
    });
  },
  {
    immediate: true,
  }
);
</script>

<style scoped lang="less">
.message {
  width: 100%;
  height: 100%;
  background-color: #fff;

  ul {
    list-style: none;
    padding: 0;
    margin: 0;
    li {
      margin-bottom: 20px;
    }
  }

  &__item {
    &--user {
      display: flex;
      justify-content: flex-end;
      > div {
        background-color: #eff6ff;
        padding: 10px;
        border-radius: 10px;
      }
    }
    &--assistant {
      display: flex;
      justify-content: flex-start;
      > div {
        background-color: rgb(245 245 245);
        padding: 10px;
        border-radius: 10px;
      }
    }
  }
}
</style>