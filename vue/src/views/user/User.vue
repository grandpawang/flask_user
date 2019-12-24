<template>
  <div class="table">
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 用户列表
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <super-table ref="table" permsEdit="user.alert" permsDelete="user.delete" permsAdd="user.create" :expand="true" :data="tableData" :dataFormRules="dataFormRules" @select="handleSelect" @edit="handleEdit" @delete="handleDelete" @search="handleSearch">
      <div slot="edit_head_img" slot-scope="{data}">
        <header-upload :img.sync="head_img" />
      </div>

      <el-form label-position="left" class="table-expand" slot="expand" slot-scope="data">
        <el-form-item v-for="(data, index) in detailData[data.data]" :key="index" :label="data.comment" :style="data.style">
          <div v-for="(permissions, index) in data.content" :key="index" style="margin-left: 100px;">
            <el-tag v-for="(item, index) in permissions" :key="index" :style="item.style">{{item.comment}}</el-tag>
          </div>
        </el-form-item>
      </el-form>

      <div slot="head_img" slot-scope="data">
        <el-avatar size="small" :src="tableData.content[data.data].head_img" v-if="tableData.content[data.data].head_img"></el-avatar>
        <el-avatar size="small" icon="el-icon-user-solid" v-else></el-avatar>
      </div>

    </super-table>
  </div>
</template>

<script>
import SuperTable from "@/components/table/SuperTable";
import data2tree from "@/utils/data2tree";
import parseData from "@/utils/parseData";
import randomColor from "@/utils/randomColor";
import array2set from "@/utils/array2set";
import structbytes from "@/utils/structbytes.js";
import headerUpload from '@/components/headerUpload/index.vue'

export default {
  components: {
    SuperTable,
    headerUpload,
  },
  data() {
    return {
      dataFormRules: {
        username: [
          {
            // required: true,
            message: "请输入用户名",
            trigger: "blur"
          }
        ]
      },
      tableData: {},
      detailData: [],
      head_img: null,
      // roles: {},
    };
  },
  mounted() { },
  methods: {
    structDetailData() {
      this.detailData = this.tableData.content.map((data, index, arr) => {
        var permissions = [];
        var roles = data.roles.concat();
        // 角色下的权限
        roles.map((value, index, arr) => {
          var style = Object.assign(randomColor.RandomStyle(0.3), {
            margin: "3px"
          });
          arr[index].style = style;
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
        permissions = permissions.concat(
          data.permissions.map((value, index, arr) => {
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
        return [
          { comment: "角色", content: [roles] },
          { comment: "权限", content: permissions }
        ];
      });
    },
    handleSelect(req) {
      this.$api.user
        .select(req.data)
        .then(res => {
          console.log(res.data.data);
          var option = this.structOptions(res.data.data.options);
          var statusFormat = (row, column) => {
            if (row.status === 1) {
              return "已注销";
            } else {
              return "使用中";
            }
          };
          this.tableData = res.data.data;
          this.tableData.labels = {
            head_img: {
              label: "头像",
              selectAble: false,
              slot: true,
              edit_slot: true,
              edit_formatt: val => {
                this.head_img = val;
              }
            },
            username: {
              label: "用户名",
            },
            fullname: {
              label: "真实姓名",
            },
            phone: {
              label: "电话",
            },
            create_at: {
              label: "创建时间",
              show_props: { sortable: true, },
              user_edit: false,
              edit: "el-date-picker",
              edit_props: { type: "datetime", clearable: true }
            },
            update_at: {
              label: "更改时间",
              show_props: { sortable: true, },
              user_edit: false,
              edit: "el-date-picker",
              edit_props: { type: "datetime", clearable: true }
            },
            status: {
              label: "使用状态",
              show_props: { formatter: statusFormat },
              edit: "el-switch",
            },
            permissions: {
              label: "操作权限",
              show_list: false,
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
            },
            roles: {
              label: "角色",
              show_list: false,
              edit: "el-cascader",
              edit_props: {
                props: {
                  multiple: true,
                  expandTrigger: "hover",
                  checkStrictly: false
                },
                "show-all-levels": false,
                clearable: true,
                options: option.roles
              },
              edit_formatt: value => {
                return value.map((val, index, arr) => {
                  if (val.group_id) {
                    return [val.group_id, val.id];
                  }
                  return val;
                });
              }
            }
          };
          this.structDetailData();
        })
        .then(() => {
          if (req) req.callback();
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
      for (var key in data.group) {
        roles[data.group[key].id] = {
          label: data.group[key].comment,
          value: data.group[key].id,
          children: []
        };
      }
      for (var key in data.role) {
        roles[data.role[key].group_id].children.push({
          value: data.role[key].id,
          label: data.role[key].comment
        });
      }
      return roles;
    },
    structOptions(data) {
      return {
        permissions: Object.values(
          this.structOptionPermission(data, {
            group: "机构权限",
            role: "角色权限",
            user: "用户权限",
            test: "test",
            test2: "test2"
          })
        ),
        roles: Object.values(this.structOptionRoles(data))
      };
    },
    handleSearch(req) {
      try {
        req.data.word = req.data.word.map((val, index, arr) => {
          return val[1];
        });
      } catch (err) { }

      this.$api.user.search(req.data).then(res => {
        this.tableData.content = res.data.data.content;
      });
    },
    handleDelete: function (req) {
      // 批量删除
      this.$api.user.del(req.data).then(res => {
        req.callback(res);
      });
    },
    handleEdit: function (req) {
      // 处理编辑、新增操作
      req.data.permissions = req.data.permissions.map((value, index, arr) => {
        return value[1];
      });
      req.data.roles = req.data.roles.map((value, index, arr) => {
        return value[1];
      });
      req.data.head_img = this.head_img;
      this.$api.user.add_edit(req.data).then(res => {
        req.callback(res);
      });
      // req.callback({ data: { status: true } });
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
