<template>
  <div class="wrapper">
    <!-- 头部区域 -->
    <v-head></v-head>
    <!-- 导航栏 -->
    <v-sidebar></v-sidebar>
    <!-- 主内容区域 -->
    <v-content></v-content>
  </div>
</template>

<script>
import vHead from "./components/Header.vue";
import vSidebar from "./components/Sidebar.vue";
import vContent from "./components/Content.vue";
export default {
  data() {
    return {};
  },
  components: {
    vHead,
    vSidebar,
    vContent
  }
};
</script>

<style scoped lang="scss">
.wrapper {
  position: absolute;
  top: 0px;
  left: 0px;
  right: 0px;
  bottom: 0px;
  // background: rgba(224, 234, 235, 0.1);
}
</style>