<template>
  <div :class="['header', $store.state.app.collapse ? 'position-collapse-left': 'position-left']">
    <!-- 导航菜单 -->
    <span class="navbar">
      <hamburger id="hamburger-container" :is-active="collapse" class="hamburger-container" @toggleClick="toggleSideBar" />
    </span>

    <!-- 工具栏 -->
    <span class="header-right">
      <div class="header-user-con">
        <!-- 消息中心 -->
        <div class="btn-bell">
          <el-tooltip effect="dark" :content="message?`有${message}条未读消息`:`消息中心`" placement="bottom">
            <router-link to="/tabs">
              <i class="el-icon-bell"></i>
            </router-link>
          </el-tooltip>
          <span class="btn-bell-badge" v-if="message"></span>
        </div>

        <!-- 全屏 -->
        <div class="btn-fullscreen" @click="handleFullScreen">
          <el-tooltip effect="dark" :content="fullscreen?`取消全屏`:`全屏`" placement="bottom">
            <i class="el-icon-rank"></i>
          </el-tooltip>
        </div>

        <!-- i8n -->
        <el-popover placement="bottom-start" trigger="click" class="btn-i18n" v-model="langVisible">
          <div class="lang-item" @click="changeLanguage('zh_cn');">简体中文</div>
          <div class="lang-item" @click="changeLanguage('en_us');">English</div>
          <i slot="reference" class="el-icon-lx-global" />
        </el-popover>

        <!-- 用户信息 -->
        <el-popover placement="bottom-start" trigger="click" v-model="userVisible">
          <el-tooltip effect="dark" content="用户信息" placement="bottom" />
          <panel :user="user_info" />
          <div class="user-info" slot="reference">
            <span class="fullname">{{user_info.fullname}}</span>
            <img :src="user_info.head_img" />
          </div>
        </el-popover>
      </div>
    </span>
  </div>
</template>

<script>
import { mapState } from "vuex";
import Cookies from "js-cookie";
import Panel from "./Panel";
import Hamburger from "@/components/Hamburger/index.vue"
export default {
  components: {
    Panel,
    Hamburger
  },
  data() {
    return {
      userVisible: false,
      langVisible: false,
      fullscreen: false,
      message: 2
    };
  },
  computed: {
    ...mapState({
      collapse: state => state.app.collapse,
      appName: state => state.app.appName,
      user_info: state => state.user.info
    })
  },
  methods: {
    // i18n
    changeLanguage(lang) {
      console.log(lang, this);
      lang === "" ? "zh_cn" : lang;
      this.$i18n.locale = lang;
      this.langVisible = false;
      this.$message({
        message: this.$t("message.change_success"),
        type: "success"
      });
    },
    // 全屏事件
    handleFullScreen() {
      let element = document.documentElement;
      if (this.fullscreen) {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        } else if (document.webkitCancelFullScreen) {
          document.webkitCancelFullScreen();
        } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen();
        } else if (document.msExitFullscreen) {
          document.msExitFullscreen();
        }
      } else {
        if (element.requestFullscreen) {
          element.requestFullscreen();
        } else if (element.webkitRequestFullScreen) {
          element.webkitRequestFullScreen();
        } else if (element.mozRequestFullScreen) {
          element.mozRequestFullScreen();
        } else if (element.msRequestFullscreen) {
          // IE11
          element.msRequestFullscreen();
        }
      }
      this.fullscreen = !this.fullscreen;
    },
    toggleSideBar() {
      this.$store.commit('set_collapse')
    }
  }
};
</script>

<style scoped lang="scss">
.header {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 1030;
  height: 50px;
  line-height: 50px;
  background-color: #242f42;
  .navbar {
    float: left;
  }
  .header-right {
    padding-right: 50px;
    float: right;
  }
  .el-menu--horizontal > .el-menu-item {
    height: 50px;
    background-color: #242f42;
  }
}
.lang-item {
  font-size: 16px;
  padding-left: 8px;
  padding-top: 8px;
  padding-bottom: 8px;
  cursor: pointer;
  :hover {
    font-size: 18px;
    background: #b0d6ce4d;
  }
}

.header-user-con {
  display: flex;
  height: 50px;
  align-items: center;
  .btn-bell-badge {
    margin-top: 5px;
    position: absolute;
    right: 0;
    top: -2px;
    width: 8px;
    height: 8px;
    border-radius: 4px;
    background: #f56c6c;
    color: #666;
  }
  .btn-i18n,
  .btn-bell,
  .btn-fullscreen {
    margin-right: 15px;
    margin-bottom: 10px;
    font-size: 20px;
    position: relative;
    width: 35px;
    height: 35px;
    text-align: center;
    border-radius: 20px;
    cursor: pointer;
    color: rgb(185, 185, 185);
    .el-icon-bell {
      color: rgb(185, 185, 185);
    }
  }
  .user-info {
    font-size: 25px;
    cursor: pointer;
    img {
      width: 35px;
      height: 35px;
      border-radius: 50%;
      margin: 10px 0px 10px 10px;
      float: left;
    }
    .fullname {
      color: #fff;
      font-size: 15px;
      margin-left: 10px;
    }
  }
}

.badge {
  line-height: 18px;
}
.position-left {
  left: 200px;
}
.position-collapse-left {
  left: 54px;
}
</style>
