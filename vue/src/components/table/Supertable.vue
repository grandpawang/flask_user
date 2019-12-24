<template>
  <div class="page-container">
    <!-- 工具栏左边 -->
    <select-bar :labels="data.labels" :columns="baseColumns" @action="handleSearch" style="float:left;padding-top:5px;padding-left:7px;" />

    <!-- 工具栏右边 -->
    <div class="toolbar" style="float:right;padding-top:10px;padding-right:15px;">
      <el-form :inline="true" :size="size">
        <el-form-item>
          <el-button-group>
            <el-tooltip :content="$t('action.refresh')" placement="top">
              <el-button icon="el-icon-lx-refresh" @click="handleSelect(null)">{{$t('action.refresh')}}</el-button>
            </el-tooltip>
            <el-tooltip :content="$t('action.column')" placement="top">
              <el-button icon="el-icon-lx-filter" @click="columnDialogVisible=true;" type="info">{{$t('action.column')}}</el-button>
            </el-tooltip>
            <el-tooltip :content="$t('action.add')" placement="top">
              <super-button :label="$t('action.add')" icon="el-icon-lx-add" :perms="permsAdd" :size="size" @click="showAddForm" type="primary" />
            </el-tooltip>
            <!-- <el-tooltip content="导出" placement="top">
                        <el-button icon="fa fa-file-excel-o"></el-button>
            </el-tooltip>-->
          </el-button-group>
        </el-form-item>
      </el-form>
    </div>

    <!--表格显示栏-->
    <el-table ref="SuperTable" :data="data.content" :highlight-current-row="highlightCurrentRow" @selection-change="selectionChange" v-loading="loading" :element-loading-text="$t('action.loading')" :border="border" :stripe="stripe" :show-overflow-tooltip="showOverflowTooltip" :max-height="maxHeight" :height="height" :size="size" :align="align" style="width:100%;">
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column type="expand" v-if="expand" width="1">
        <template slot-scope="scope">
          <slot name="expand" :data="scope.$index" />
        </template>
      </el-table-column>
      <div v-for="column in columns" v-if="column.show_list">
        <el-table-column header-align="center" align="center" :key="column.prop" :label="column.label" v-bind="column.show_props" v-if="column.slot">
          <template slot-scope="scope">
            <slot :name="column.prop" :data="scope.$index" />
          </template>
        </el-table-column>
        <el-table-column header-align="center" align="center" :key="column.prop" :prop="column.prop" :label="column.label" v-bind="column.show_props" v-else></el-table-column>
      </div>
      <el-table-column :label="$t('action.operation')" width="225" header-align="center" align="center" fixed="right">
        <template slot-scope="scope">
          <el-button type="primary" v-if="expand" :size="size" @click="showDetail(scope.$index, scope.row)">{{$t('action.detail')}}</el-button>
          <super-button :label="$t('action.edit')" :perms="permsEdit" :size="size" @click="showEditform(scope.$index, scope.row)" />
          <super-button :label="$t('action.delete')" :perms="permsDelete" :size="size" type="danger" @click="handleDelete([scope.row.id])" />
        </template>
      </el-table-column>
    </el-table>
    <!-- 表格显示列对话框 -->
    <filter-column :columns="baseColumns" :size="size" @action="handleFilterColumns" v-model="columnDialogVisible" />
    <!-- 编辑界面 -->
    <edit-form :operation="operation" :columns="columns" :size="size" :dialogVisible.sync="dialogVisible" :dataFormRules="dataFormRules" v-model="dataForm" @action="handleEdit" @update="handleSelect" v-for="column in columns" v-if="column.edit_slot" :key="column.prop">
      <div :slot="column.prop" slot-scope="{data}">
        <slot :name="'edit_' + column.prop" :data="data" />
      </div>
    </edit-form>
    <!--分页栏-->
    <div class="toolbar" style="padding:10px;">
      <super-button :label="$t('action.batchDelete')" :perms="permsDelete" :size="size" type="danger" @click="handleBatchDelete" :disabled="this.selections.length===0" style="float:left;" />
      <el-pagination layout="total, prev, pager, next, jumper" @current-change="refreshPageRequest" :current-page="pageRequest.page" :page-size="pageRequest.size" :page-count="pageRequest.page_count" style="float:right;"></el-pagination>
    </div>
  </div>
</template>

<script>
import permission from "@/permission";
import SuperButton from "@/components/SuperButton/index.vue";
import SelectBar from "@/components/SelectBar/index.vue";
import FilterColumn from "@/components/FilterColumn/index.vue";
import EditForm from "@/components/EditForm/index.vue";

export default {
  name: "superTable",
  components: {
    SuperButton,
    SelectBar,
    FilterColumn,
    EditForm
  },
  props: {
    data: {
      type: Object,
      default: {}
    }, // 表格分页数据
    dataFormRules: Object,
    permsEdit: String, // 编辑权限标识
    permsDelete: String, // 删除权限标识
    permsAdd: String, // 新增权限标识
    size: {
      type: String,
      default: "mini"
    }, // 尺寸样式
    align: {
      type: String,
      default: "left"
    }, // 文本对齐方式
    maxHeight: {
      type: Number
      // default: 420
    }, // 表格最大高度
    height: {
      type: Number
      // default: 250
    }, // 表格最大高度
    border: {
      type: Boolean,
      default: false
    }, // 是否显示边框
    expand: {
      type: Boolean,
      default: false
    }, // 列是否显示详细信息
    stripe: {
      type: Boolean,
      default: true
    }, // 是否显示斑马线
    highlightCurrentRow: {
      type: Boolean,
      default: true
    }, // 是否高亮当前行
    showOverflowTooltip: {
      type: Boolean,
      default: true
    } // 是否单行显示
  },
  data() {
    return {
      // 分页信息
      operation: false, // true:新增, false:编辑
      dialogVisible: false, // 新增编辑界面是否显示
      pageRequest: {
        page: 1,
        size: 10,
        page_count: 1
      },
      loading: false, // 加载标识
      selections: [], // 列表选中列
      baseColumns: [], // 所有列
      columns: [], // 显示列
      dataForm: {}, // 渲染dataForm
      columnDialogVisible: false // 显示 -- 过滤显示列对话框
    };
  },
  methods: {
    // 显示编辑界面
    showEditform: function (index, row) {
      this.dialogVisible = true;
      this.operation = false;
      this.dataForm = Object.assign({}, row); // 拷贝对象
      for (var key in this.data.labels) {
        if (this.data.labels[key].user_edit) {
          if (this.data.labels[key].edit_formatt) {
            this.dataForm[key] = this.data.labels[key].edit_formatt(row[key]);
          }
        }
      }
      // console.log(this.$refs)
    },
    showAddForm: function () {
      this.dialogVisible = true;
      this.operation = true;
      this.dataForm = {};
    },
    // 显示详细信息
    showDetail(index, row) {
      const $table = this.$refs.SuperTable;
      $table.toggleRowExpansion(row);
      // $table.toggleRowSelection(row);
    },
    // 选择切换
    selectionChange: function (selections) {
      this.selections = selections;
    },
    // 换页刷新
    refreshPageRequest: function (pageNum) {
      this.pageRequest.page = pageNum;
      this.handleSelect();
    },
    // 分页查询
    handleSelect: function () {
      this.loading = true;
      let callback = () => {
        // 数据加载好了 调用这个函数
        this.loading = false;
        this.columns = [];
        this.baseColumns = [];
        for (var key in this.data.labels) {
          // 设置默认值
          this.data.labels[key].prop = key;
          this.data.labels[key].edit =
            typeof this.data.labels[key].edit != "undefined"
              ? this.data.labels[key].edit
              : "el-input";
          this.data.labels[key].user_edit =
            typeof this.data.labels[key].user_edit != "undefined"
              ? this.data.labels[key].user_edit
              : true;
          this.data.labels[key].show_list =
            typeof this.data.labels[key].show_list != "undefined"
              ? this.data.labels[key].show_list
              : true;
          this.data.labels[key].selectAble =
            typeof this.data.labels[key].selectAble != "undefined"
              ? this.data.labels[key].selectAble
              : true;
          this.data.labels[key].edit_slot =
            typeof this.data.labels[key].edit_slot != "undefined"
              ? this.data.labels[key].edit_slot
              : false;
          this.columns.push(this.data.labels[key]);
          if (this.data.labels[key].show_list) {
            this.baseColumns.push(this.data.labels[key]);
          }
        }
        this.pageRequest = this.data.pageRequest;
      };
      this.$emit("select", {
        data: this.pageRequest,
        callback: callback
      });
    },
    // 搜索
    handleSearch: function (data) {
      this.$emit("search", {
        data: data.data
      });
    },
    // 处理表格列过滤显示
    handleFilterColumns: function (columns) {
      this.columns = columns;
    },
    // 编辑
    handleEdit: function (callback) {
      this.$emit("edit", {
        data: this.dataForm,
        callback: callback
      });
    },
    // 批量删除
    handleBatchDelete: function () {
      let ids = this.selections.map(item => item.id);
      this.handleDelete(ids);
    },
    // 删除操作
    handleDelete: function (ids) {
      ids = ids.toString();
      this.$confirm(this.$t("message.sure_delete"), this.$t("message.tips"), {
        type: "warning"
      })
        .then(() => {
          this.loading = true;
          let callback = res => {
            if (res.data.status) {
              this.$message({
                message: this.$t("message.sucess_delete"),
                type: "success"
              });
              this.handleSelect();
            } else {
              this.$message({
                message: this.$t("message.fail_delete") + res.msg,
                type: "error"
              });
            }
            this.loading = false;
          };

          this.$emit("delete", {
            data: {
              id: ids
            },
            callback: callback
          });
        })
        .catch(() => { });
    }
  },
  created() {
    this.refreshPageRequest(1);
  },
  mounted() { }
};
</script>

<style>
.el-table__expand-column .cell {
  display: none;
}
.el-table__expand-column .el-icon {
  visibility: hidden;
}
</style>
