<template>
  <div class="table">
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 机构列表
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <edit-form-table
      permsEdit="group.alert"
      permsDelete="group.delete"
      permsAdd="group.create"
      :expand="false"
      :data="tableData"
      :dataFormRules="dataFormRules"
      @select="handleSelect"
      @edit="handleEdit"
      @delete="handleDelete"
      @search="handleSearch"
    >
      <template v-slot:roles="data">
        <el-tag
          v-for="role, index in formatterData[data.data].roles"
          :key="index"
          style="margin:3px"
        >{{role.comment}}</el-tag>
      </template>
      <template v-slot:permissions="data">
        <div
          v-for="(permissions, index) in formatterData[data.data].permissions"
          :key="index"
          style="clear: both;"
        >
          <el-tag
            :style="item.style"
            :key="index"
            v-for="(item, index) in permissions"
          >{{item.comment}}</el-tag>
        </div>
      </template>
    </edit-form-table>
  </div>
</template>

<script>
import editFormTable from "@/components/CustomTable/editFormTable";
import randomColor from "@/utils/randomColor";

export default {
  components: {
    editFormTable,
  },
  data() {
    return {
      dataFormRules: {},
      tableData: {},
      formatterData: []
    };
  },
  mounted() {},
  methods: {
    structFormatterData() {
      this.formatterData = this.tableData.content.map((data, index, arr) => {
        var permissions = data.permissions.concat(); // 备份数据
        // 每个表格为一行
        var tmp = {};
        for (var key in permissions) {
          var table = permissions[key].permission.split(".")[0];
          if (tmp[table]) {
            tmp[table].push({
              comment: permissions[key].comment,
              style: tmp[table][0].style
            });
          } else {
            tmp[table] = [
              {
                style: Object.assign(randomColor.RandomStyle(0.3), {
                  margin: "3px"
                }),
                comment: permissions[key].comment
              }
            ];
          }
        }
        permissions = tmp;
        // console.log(permissions);
        return { roles: data.roles, permissions: permissions };
      });
    },
    structOptionPermission(data, labels) {
      var permission = {};
      for (var key in data.permission) {
        // 权限格式为 table.permission
        var item = data.permission[key].permission.split(".");
        if (permission[item[0]]) {
          permission[item[0]].children = permission[item[0]].children.concat([
            {
              value: data.permission[key].id,
              label: data.permission[key].comment
            }
          ]);
        } else {
          permission[item[0]] = {
            value: item[0],
            label: labels[item[0]],
            children: [
              {
                value: data.permission[key].id,
                label: data.permission[key].comment
              }
            ]
          };
        }
      }
      return permission;
    },
    structOptionRoles(data) {
      var roles = {};
      for (var key in data.role) {
        var item = data.role[key];
        roles[item.id] = {
          value: item.id,
          label: item.comment
        };
      }
      return roles;
    },
    structOptions(options) {
      return {
        permissions: Object.values(
          this.structOptionPermission(options, {
            group: "机构权限",
            role: "角色权限",
            user: "用户权限",
            test: "test",
            test2: "test2"
          })
        ),
        roles: Object.values(this.structOptionRoles(options))
      };
    },
    handleSelect(req) {
      this.$api.group
        .select(req.data)
        .then(res => {
          // console.log(res.data.data);
          this.tableData = res.data.data;
          this.structFormatterData();
          var option = this.structOptions(res.data.data.options);
          this.tableData.labels = {
            comment: {
              label: "名称",
            },
            roles: {
              label: "角色",
              user_edit: false,
              sortable: false,
              slot: true,
              selectAble: false,
            },
            permissions: {
              label: "权限",
              sortable: false,
              slot: true,
              edit: "el-cascader",
              edit_props: {
                props: {
                  multiple: true,
                  expandTrigger: "hover",
                  checkStrictly: false
                },
                "show-all-levels": false,
                clearable: true,
                options: option.permissions
              },
              edit_formatt: value => {
                try {
                  return value.map((val, index, arr) => {
                    return [val.permission.split(".")[0], val.id];
                  });
                } catch (err) {
                  return value;
                }
              }
            }
          };
        })
        .then(() => {
          if (req) req.callback();
        });
    },
    handleSearch(req) {
      try {
        req.data.word = req.data.word.map((val, index, arr) => {
          return val[1];
        });
      } catch (err) {}

      this.$api.group.search(req.data).then(res => {
        this.tableData.content = res.data.data.content;
      });
    },
    handleDelete: function(req) {
      // 批量删除
      this.$api.group.del(req.data).then(res => {
        req.callback(res);
      });
    },
    handleEdit: function(req) {
      // 处理编辑、新增操作
      req.data.permissions = req.data.permissions.map((value, index, arr) => {
        return value[1];
      });
      req.data.roles = req.data.roles.map((value, index, arr) => {
        return value.id;
      });
      this.$api.group.add_edit(req.data).then(res => {
        req.callback(res);
      });
    }
  }
};
</script>

<style>
.table-expand {
  font-size: 0;
}
.table-expand label {
  width: 100px;
  color: #99a9bf;
}
.table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
}
</style>
