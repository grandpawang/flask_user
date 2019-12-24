<template>
  <div>
    <div class="crumbs" style="position:relative;display: inline-block;">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 角色列表
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="toolbar" style="position:absolute;margin-left:150px;display:inline-block;">
      <el-tag :style="formatterPermissionStyle.role">角色权限</el-tag>
      <el-tag :style="formatterPermissionStyle.group">机构权限</el-tag>
    </div>

    <super-table permsEdit="role.alert" permsDelete="role.delete" permsAdd="role.create" :expand="false" :data="tableData" :dataFormRules="dataFormRules" @select="handleSelect" @edit="handleEdit" @delete="handleDelete" @search="handleSearch">
      <template v-slot:permissions="data">
        <div v-for="(permissions, index) in formatterData[data.data].permissions" :key="index" style="float:left;clear: both;">
          <el-tag :style="item.style" :key="index" v-for="(item, index) in permissions">{{item.comment}}</el-tag>
        </div>
      </template>
    </super-table>
  </div>
</template>

<script>
import SuperTable from "@/components/table/SuperTable";
import randomColor from "@/utils/randomColor";
import array2set from "@/utils/array2set";

export default {
  components: {
    SuperTable,

  },
  data() {
    return {
      dataFormRules: {},
      tableData: {},
      formatterData: [],
      formatterPermissionStyle: {
        role: Object.assign(randomColor.RandomStyle(0.3), { margin: "3px" }),
        group: Object.assign(randomColor.RandomStyle(0.3), { margin: "3px" })
      }
    };
  },
  mounted() { },
  methods: {
    structFormatterData() {
      this.formatterData = this.tableData.content.map((data, index, arr) => {
        var tmp = data.group.permissions.concat();
        var permissions = tmp.map((val, index, arr) => {
          return {
            comment: val.comment,
            style: this.formatterPermissionStyle.group,
            permission: val.permission
          };
        });

        tmp = data.permissions.concat(); // 备份数据
        permissions = permissions.concat(
          tmp.map((val, index, arr) => {
            return {
              comment: val.comment,
              style: this.formatterPermissionStyle.role,
              permission: val.permission
            };
          })
        );
        // 先留的覆盖后留的
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
        return { permissions: permissions };
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
    structOptionGroup(data) {
      var group = {};
      for (var key in data.group) {
        var item = data.group[key];
        group[item.id] = {
          value: item.id,
          label: item.comment
        };
      }
      return group;
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
        group: Object.values(this.structOptionGroup(options))
      };
    },
    handleSelect(req) {
      this.$api.role
        .select(req.data)
        .then(res => {
          // console.log(res.data.data);
          this.tableData = res.data.data;
          this.structFormatterData();
          var option = this.structOptions(res.data.data.options);
          this.tableData.labels = {
            comment: {
              show_props: { width: 120, },
              label: "名称"
            },
            group_id: {
              label: "机构",
              show_props: {
                formatter: (val, col, index) => {
                  return val.group.comment;
                },
              },
              edit: "el-cascader",
              edit_props: {
                props: {
                  expandTrigger: "hover",
                  checkStrictly: false
                },
                "show-all-levels": false,
                clearable: true,
                options: option.group
              },
              edit_formatt: value => {
                return value;
              }
            },
            permissions: {
              label: "权限",
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
      } catch (err) { }

      this.$api.role.search(req.data).then(res => {
        this.tableData.content = res.data.data.content;
      });
    },
    handleDelete: function (req) {
      // 批量删除
      this.$api.role.del(req.data).then(res => {
        req.callback(res);
      });
    },
    handleEdit: function (req) {
      // 处理编辑、新增操作
      req.data.permissions = req.data.permissions.map((value, index, arr) => {
        return value[1];
      });
      this.$api.role.add_edit(req.data).then(res => {
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
