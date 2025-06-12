<template>
    <div class="message">
        <ul>
            <li v-for="item in messages" :key="item.id">
                <template v-if="item.role === 'user'">
                    <div class="message__item--user">
                        <ui-chat-list-item :content="item.content" />
                    </div>
                </template>
                <template v-else-if="item.role === 'assistant'">
                    <div class="message__item--assistant">
                        <ui-chat-list-item :content="item.content" />
                    </div>
                </template>
              
            </li>
        </ul>
    </div>
</template>

<script setup lang="ts">
import { PropType } from 'vue';
import UiChatListItem from './ui-chat-list-item.vue';
defineProps({
    messages: {
        type: Array as PropType<any[]>,
        default: () => []
    }
})

</script>

<style scoped lang="less">
.message {
    width: 100%;
    height: 100%;
    background-color: #fff;

    ul{
        list-style: none;
        padding: 0;
        margin: 0;
        li{
            margin-bottom: 20px;
        }
    }

    &__item{
        &--user{
            display: flex;
            justify-content: flex-end;
            >div{
                background-color: #eff6ff;
                padding: 10px;
                border-radius: 10px;
            }
        }
        &--assistant{
            display: flex;
            justify-content: flex-start;
            >div{
                background-color: rgb(245 245 245);
                padding: 10px;
                border-radius: 10px;
            }
        }
    }
}
</style>