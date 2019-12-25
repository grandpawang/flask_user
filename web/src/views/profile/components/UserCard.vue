<template>
  <el-card style="margin-bottom:20px;">
    <div slot="header" class="clearfix">
      <span>About me</span>
      <el-button class="personal-edit" type="primary" @click="edit=true">edit</el-button>
    </div>

    <div class="personal-panel">
      <div class="personal-desc">
        <div class="avatar-container">
          <img class="avatar" :src="user.head_img" />
          <div class="info-list">
            <el-form class="info-list-form" label-width="68px" :size="size">
              <el-form-item label="用户名">
                <span v-text="user.username" />
              </el-form-item>
              <el-form-item label="真实姓名">
                <span v-text="user.fullname" />
              </el-form-item>
              <el-form-item label="电话">
                <span v-text="user.phone" />
              </el-form-item>
              <el-form-item label="注册时间">
                <span v-text="user.create_at" />
              </el-form-item>
              <el-form-item label="更新时间">
                <span v-text="user.update_at" />
              </el-form-item>
            </el-form>
          </div>
        </div>
      </div>
    </div>
    <div class="user-bio">
      <div class="user-bio-section">
        <div class="user-bio-section-header">
          <span>group</span>
        </div>
        <el-tag
          v-for="(item, index) in detailData.groups"
          :key="index"
          :style="item.style"
        >{{item.comment}}</el-tag>
      </div>

      <div class="user-bio-section">
        <div class="user-bio-section-header">
          <span>roles</span>
        </div>
        <el-tag
          v-for="(item, index) in detailData.roles"
          :key="index"
          :style="item.style"
        >{{item.comment}}</el-tag>
      </div>

      <div class="user-bio-section">
        <div class="user-bio-section-header">
          <span>permissions</span>
        </div>
        <div v-for="(item, index) in detailData.permissions" :key="index">
          <el-tag v-for="(item, index) in item" :key="index" :style="item.style">{{item.comment}}</el-tag>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script>
import randomColor from "@/utils/randomColor";
import array2set from "@/utils/array2set";

export default {
  data() {
    return {
      detailData: [],
      edit: false
    };
  },
  props: {
    user: Object,
    size: {
      type: String,
      default: "mini"
    }
  },
  methods: {
    structDetailData() {
      var permissions = [];
      var groups = [];
      var roles = this.user.roles.concat();
      // 角色下的权限
      roles.map((value, index, arr) => {
        var style = Object.assign(randomColor.RandomStyle(0.3), {
          margin: "5px"
        });
        arr[index].style = style;
        groups = groups.concat({
          comment: value.group.comment,
          style: style
        });
        // 添加 role.permission
        permissions = permissions.concat(
          value.permissions.map((value, index, arr) => {
            return {
              comment: value.comment,
              style: style,
              permission: value.permission
            };
          })
        );
        // 添加 role.group.permission
        permissions = permissions.concat(
          value.group.permissions.map((value, index, arr) => {
            return {
              comment: value.comment,
              style: style,
              permission: value.permission
            };
          })
        );
      });

      var style = randomColor.RandomStyle(0.3);
      // 用户下的权限
      roles.push({
        comment: "其他",
        style: style
      });
      groups.push({
        comment: "其他",
        style: style
      });
      permissions = permissions.concat(
        this.user.permissions.map((value, index, arr) => {
          return {
            comment: value.comment,
            style: style,
            permission: value.permission
          };
        })
      );
      permissions = array2set.array2set(permissions, val => {
        return val.permission;
      });
      // 每个表格为一行
      var tmp = {};
      for (var key in permissions) {
        var table = permissions[key].permission.split(".")[0];
        if (tmp[table]) {
          tmp[table].push(permissions[key]);
        } else {
          tmp[table] = [permissions[key]];
        }
      }
      permissions = tmp;
      return { groups: groups, roles: roles, permissions: permissions };
    }
  },
  watch: {
    user(val) {
      this.detailData = this.structDetailData();
      console.log(this.detailData);
    }
  }
};
</script>

<style lang="scss" scoped>
.box-center {
  display: table;
}
.personal-panel {
  // width: 100%;
  text-align: center;
  .personal-desc {
    padding-top: 15px;
    .avatar-container {
      // width: 100%;
      .avatar {
        width: 120px;
        height: 120px;
        border-radius: 50%;
      }
      .info-list {
        // width: 100%;
        display: flex;
        justify-content: center;
        .info-list-form {
          // margin: 0px auto;
          margin-top: 10px;
          .el-form-item {
            margin-bottom: 0px;
          }
        }
      }
    }
    .time-list-form {
      margin-top: 10px;
      .el-form-item {
        margin-bottom: 0px;
      }
    }
  }
}

.user-bio {
  margin-top: 20px;
  color: #606266;

  span {
    padding-left: 4px;
  }

  .user-bio-section {
    font-size: 14px;
    padding: 15px 0;

    .user-bio-section-header {
      border-bottom: 1px solid #dfe6ec;
      padding-bottom: 10px;
      margin-bottom: 10px;
      font-weight: bold;
    }
  }
}

.personal-edit {
  margin-bottom: 10px;
  float: right;
}
</style>
