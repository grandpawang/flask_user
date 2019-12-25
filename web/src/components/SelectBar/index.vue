<template>
  <div class="toolbar">
    <el-form :inline="true" :model="select" :size="size">
      <el-form-item>
        <el-select
          v-model="select.column"
          :placeholder="$t('select.columns')"
          @change="selectChange"
        >
          <el-option
            v-for="(column, index) in columns"
            :label="column.label"
            :value="column.prop"
            v-if="column.selectAble"
            :key="index.toString()"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <component
          :is="select_item.type"
          ref="selection"
          v-model="select.word"
          :placeholder="$t('select.key')"
          v-bind="select_item.props"
        />
      </el-form-item>
      <el-form-item>
        <el-button
          :size="size"
          icon="el-icon-search"
          @click="handleSearch"
          type="primary"
        >{{$t('select.action')}}</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  props: {
    labels: {
      type: Object,
      default: () => {},
    },
    columns: {
      type: Array,
      default: () => [],
    },
    size: {
      type: String,
      default: "mini",
    }

  },
  data() {
    return {
      select: {
        column: "",
        word: ""
      }, // selection information
      select_item: {
        type: "el-input", // selection component
        props: {}
      }
    };
  },
  methods: {
    // 搜索
    handleSearch: function() {
      this.$emit("action", {
        data: this.select
      });
    },
    // 根据列切换搜索输入框类型
    selectChange: function(val) {
      this.select_item.type = this.labels[val].edit;
      this.select_item.props = this.labels[val].edit_props;
      this.select.word = "";
    }
  },

};
</script>

<style>
</style>