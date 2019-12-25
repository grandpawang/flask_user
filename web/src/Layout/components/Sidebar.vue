<template>
  <div class="menu-bar-container">
    <!-- 导航菜单 -->
    <el-menu ref="navmenu" mode="vertical" :default-active="activeMenu" :class="collapse?'menu-bar-collapse-width':'menu-bar-width'" :collapse="collapse" background-color="#324157" text-color="#bfcbd9" active-text-color="#20a0ff" collapse-transitions unique-opened>
      <sidebar-item v-for="route in sidebar" :key="route.path" :item="route" :base-path="route.path" />
    </el-menu>
  </div>
</template>

<script>
import { mapState } from "vuex";
import SidebarItem from './Sidebar/SidebarItem.vue'
export default {
  data() {
    return {};
  },
  components: {
    SidebarItem,
  },
  computed: {
    ...mapState({
      collapse: state => state.app.collapse,
      appName: state => state.app.appName,
      sidebar: state => state.app.sidebar,
    }),
    activeMenu() {
      const route = this.$route
      const { meta, path } = route
      // if set path, the sidebar will highlight the path you set
      if (meta.activeMenu) {
        return meta.activeMenu
      }
      return path
    },
  },
  methods: {
    // 侧边栏折叠
    collapseChage() {
      this.$store.commit("set_collapse");
    }
  },
  mounted() {
    if (document.body.clientWidth < 1500) {
      this.collapseChage();
    }
  }
};
</script>

<style scoped lang="scss">
.menu-bar-container {
  position: fixed;
  top: 0px;
  left: 0;
  bottom: 0;
  z-index: 1001;
  .el-menu {
    position: absolute;
    top: 0px;
    bottom: 0px;
    padding-left: 0px;
    text-align: left;
  }
}
.menu-bar-width {
  width: 200px;
}
.menu-bar-collapse-width {
  width: 54px;
}
</style>

<style lang="scss">
.el-menu--collapse {
  // hidden span icon
  .el-submenu {
    & > .el-submenu__title {
      & > span {
        height: 0;
        width: 0;
        overflow: hidden;
        visibility: hidden;
        display: inline-block;
      }
      .el-submenu__icon-arrow {
        display: none;
      }
    }
  }
}
</style>
