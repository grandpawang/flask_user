<template>
  <!-- 表格显示列界面 -->
  <el-dialog title="表格显示列" width="40%" :visible.sync="visible" :close-on-click-modal="false">
    <el-table
      tooltip-effect="dark"
      header-align="left"
      align="left"
      style="width: 100%"
      :size="size"
      :data="columns"
      @selection-change="ColumnSelectionChange"
    >
      <el-table-column type="selection" width="55" align="center"></el-table-column>
      <el-table-column label="列名">
        <template slot-scope="scope">
          <el-input :size="size" v-model="scope.row.label"></el-input>
        </template>
      </el-table-column>
      <el-table-column label="最小宽度">
        <template slot-scope="scope">
          <el-input :size="size" v-model="scope.row.minWidth"></el-input>
        </template>
      </el-table-column>
    </el-table>
    <div slot="footer" class="dialog-footer">
      <el-button :size="size" @click.native="visible = false">{{$t('action.cancel')}}</el-button>
      <el-button
        :size="size"
        type="primary"
        @click.native="handleFilterColumns"
      >{{$t('action.comfirm')}}</el-button>
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: "FilterColumns",
  props: {
    columns: {
      type: Array,
      default: []
    },
    size: {
      type: String,
      default: "mini"
    },
    columnDialogVisible: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    visible: {
      get() {
        return this.columnDialogVisible;
      },
      set(val) {
        this.$emit("visible", val);
      }
    }
  },
  data() {
    return {
      columnSelections: [] // 选择显示项
    };
  },
  model: {
    prop: "columnDialogVisible", // get v-model
    event: "visible" // set v-model
  },
  methods: {
    // 选择切换
    ColumnSelectionChange: function(selections) {
      this.columnSelections = selections;
    },
    // 处理表格列过滤显示
    handleFilterColumns: function() {
      this.visible = false;
      let hasColumn = column => {
        for (let i = 0; i < this.columnSelections.length; i++) {
          let col = this.columnSelections[i];
          if (column.prop == col.prop) {
            return true;
          }
        }
        return false;
      };
      var columns = this.columns.concat();
      for (let i = 0; i < columns.length; i++) {
        columns[i].if = hasColumn(columns[i]);
      }
      this.$emit("action", columns);
    }
  }
};
</script>

<style>
</style>