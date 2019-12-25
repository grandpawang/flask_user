<template>
  <div
    class="content-box"
    :class="$store.state.app.collapse?'position-collapse-left':'position-left'"
  >
    <!-- 标签页 -->
    <div class="tags">
      <ul>
        <li
          class="tags-li"
          v-for="(item,index) in tagsList"
          :class="{'active': isActive(item.path)}"
          :key="index"
        >
          <router-link :to="item.path" class="tags-li-title">{{item.title}}</router-link>
          <span class="tags-li-icon" @click="closeTags(index)">
            <i class="el-icon-close"></i>
          </span>
        </li>
      </ul>
      <div class="tags-close-box">
        <el-dropdown :show-timeout="0" trigger="hover">
          <el-button size="mini" type="primary">
            标签选项
            <i class="el-icon-arrow-down el-icon--right"></i>
          </el-button>
          <el-dropdown-menu size="small" slot="dropdown">
            <el-dropdown-item @click.native="tabsCloseAllHandle">关闭其他</el-dropdown-item>
            <el-dropdown-item @click.native="tabsCloseOtherHandle">关闭所有</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
    <!-- 主内容区域 -->
    <div class="content">
      <!-- fade -->
      <transition name="move" mode="out-in">
        <keep-alive>
          <router-view></router-view>
        </keep-alive>
      </transition>
      <el-backtop target=".content"></el-backtop>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  data() {
    return {};
  },
  computed: {
    tagsList: {
      get() {
        return this.$store.state.app.tags;
      },
      set(val) {
        this.$store.commit("update_tags", val);
      }
    },
    tagsActiveName: {
      get() {
        return this.$store.state.app.tagsActiveName;
      },
      set(val) {
        this.$store.commit("updateTagsActiveName", val);
      }
    }
  },
  watch: {
    $route(newValue, oldValue) {
      this.setTags(newValue);
    }
  },
  created() {
    this.setTags(this.$route);
  },
  methods: {
    isActive(path) {
      return path === this.$route.fullPath;
    },
    // 关闭单个标签
    closeTags(index) {
      const delItem = this.tagsList.splice(index, 1)[0];
      const item = this.tagsList[index]
        ? this.tagsList[index]
        : this.tagsList[index - 1];
      if (item) {
        delItem.path === this.$route.fullPath && this.$router.push(item.path);
      } else {
        this.$router.push("/");
      }
    },
    // 关闭全部标签
    tabsCloseAllHandle() {
      this.tagsList = [];
      this.$router.push("/");
    },
    // 关闭其他标签
    tabsCloseOtherHandle() {
      const curItem = this.tagsList.filter(item => {
        return item.path === this.$route.fullPath;
      });
      this.tagsList = curItem;
    },
    // 设置标签
    setTags(route) {
      const isExist = this.tagsList.some(item => {
        return item.path === route.fullPath;
      });
      if (!isExist) {
        if (this.tagsList.length >= 8) {
          this.tagsList.shift();
        }
        this.tagsList.push({
          title: route.meta.title,
          path: route.fullPath,
          name: route.matched[1].components.default.name
        });
      }
    }
  }
};
</script>


<style scoped lang="scss">
.content-box {
  padding: 0 0px 0px 0px;
  position: absolute;
  top: 50px;
  left: 0px;
  right: 0px;
  bottom: 0px;
  .content {
    position: absolute;
    top: 40px;
    left: 5px;
    right: 5px;
    bottom: 5px;
    padding: 5px;
  }
  .tags {
    position: relative;
    height: 30px;
    overflow: hidden;
    background: #fff;
    padding-right: 120px;
    box-shadow: 0 5px 10px #ddd;
    ul {
      box-sizing: border-box;
      width: 100%;
      height: 100%;
      .tags-li {
        float: left;
        margin: 3px 5px 2px 3px;
        border-radius: 3px;
        font-size: 12px;
        overflow: hidden;
        cursor: pointer;
        height: 23px;
        line-height: 23px;
        border: 1px solid #e9eaec;
        padding: 0 5px 0 12px;
        vertical-align: middle;
        color: #666;
        -webkit-transition: all 0.3s ease-in;
        -moz-transition: all 0.3s ease-in;
        transition: all 0.3s ease-in;
        .active {
          color: #fff;
          .tags-li-title {
            color: #fff;
          }
        }
        .tags-li-title {
          float: left;
          max-width: 80px;
          overflow: hidden;
          white-space: nowrap;
          text-overflow: ellipsis;
          margin-right: 5px;
          color: #666;
        }
      }
    }
    .tags-close-box {
      position: absolute;
      right: 0;
      top: 0;
      box-sizing: border-box;
      padding-top: 1px;
      text-align: center;
      width: 110px;
      height: 30px;
      background: #fff;
      box-shadow: -3px 0 15px 3px rgba(0, 0, 0, 0.1);
      z-index: 10;
    }
  }

}
.position-left {
  left: 200px;
}
.position-collapse-left {
  left: 54px;
}
</style>
