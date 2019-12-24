<template>
  <div class="personal-panel">
    <div class="personal-desc">
      <div class="avatar-container">
        <img class="avatar" :src="user.head_img" />
        <el-form label-width="80px" class="info-list-form" :size="size">
          <el-form-item label="用户名">
            <span v-text="user.username" />
          </el-form-item>
          <el-form-item label="真实姓名">
            <span v-text="user.fullname" />
          </el-form-item>
          <el-form-item label="电话">
            <span v-text="user.phone" />
          </el-form-item>
        </el-form>
      </div>
    </div>

    <!-- <div class="personal-relation">
      <span class="relation-item">followers</span>
      <span class="relation-item">watches</span>
      <span class="relation-item">friends</span>
    </div>-->
    <div class="main-operation">
      <span class="main-operation-item">
        <el-button size="small" icon="el-icon-user" @click="$router.push('/current_user')">个人中心</el-button>
      </span>
      <span class="main-operation-item">
        <el-button size="small" icon="el-icon-setting">修改密码</el-button>
      </span>
    </div>
    <div class="personal-footer" @click="logout">{{$t("common.logout")}}</div>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import randomColor from "@/utils/randomColor";
import array2set from "@/utils/array2set";

export default {
  name: "Panel",
  props: {
    user: {
      type: Object,
      default: {}
    },
    size: {
      type: String,
      default: "mini"
    }
  },
  data() {
    return {
      detailData: []
    };
  },
  methods: {
    // 退出登录
    logout: function() {
      this.$confirm("确认退出吗?", "提示", {
        type: "warning"
      })
        .then(() => {
          Cookies.remove("authenticate");
          this.$store.commit('user/LOGOUT');
          this.$router.push("/login");
        })
        .catch(() => {});
    }
  },
};
</script>

<style scoped lang="scss">
.personal-panel {
  width: 280px;
  text-align: center;
  border-color: rgba(180, 190, 190, 0.2);
  border-width: 1px;
  border-style: solid;
  background: rgba(182, 172, 172, 0.1);
  margin: -14px;
  .personal-desc {
    padding-top: 15px;
    color: #999;
    // border-bottom: 2px solid #ccc;
    .avatar-container {
      display: flex;
      align-items: center;
      .avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        margin-left: 10px;
      }
      .info-list-form {
        color: #666;
        .el-form-item {
          margin-bottom: 0px;
        }
      }
    }
  }
}

.main-operation {
  padding: 8px;
  margin-top: 10px;
  margin-right: 1px;
  /* background: rgba(175, 182, 179, 0.3); */
  border-color: rgba(201, 206, 206, 0.2);
  border-top-width: 1px;
  border-top-style: solid;
}
.main-operation-item {
  margin: 15px;
}

.personal-footer {
  margin-right: 1px;
  font-size: 14px;
  text-align: center;
  padding-top: 10px;
  padding-bottom: 10px;
  border-color: rgba(180, 190, 190, 0.2);
  border-top-width: 1px;
  border-top-style: solid;
}
.personal-footer:hover {
  cursor: pointer;
  color: rgb(19, 138, 156);
  background: #b1a6a61e;
}
</style>