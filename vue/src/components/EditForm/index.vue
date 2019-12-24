<template>
  <!-- 编辑界面 -->
  <el-dialog
	:title="operation?$t('action.add'):$t('action.edit')"
	width="500px"
	:visible.sync="visible"
	:close-on-click-modal="false"
  >
	<el-form v-model="form" label-width="80px" :rules="dataFormRules" label-position="right">
	  <el-form-item
		:label="column.label"
		:prop="column.prop"
		v-for="(column, index) in columns"
		v-if="column.user_edit"
		:key="index"
	  >
	  	<div v-if="column.edit_slot">
			<!-- 添加edit_slot -->
			<slot :name="column.prop" :data="form[column.prop]" />
		</div>
		<div v-else>
			<component :is="column.edit" v-bind="column.edit_props" v-model="form[column.prop]" />
		</div>
	  </el-form-item>
	</el-form>
	<!-- <slot name="edit-dialog" :data="dataForm" /> -->
	<div slot="footer" class="dialog-footer">
	  <el-button :size="size" @click="visible = false">{{$t('action.cancel')}}</el-button>
	  <el-button
		:size="size"
		@click="handleEdit"
		type="primary"
		:loading="editLoading"
	  >{{$t('action.submit')}}</el-button>
	</div>
  </el-dialog>
</template>

<script>
export default {
  data() {
	return {
	  editLoading: false
	};
  },
  computed: {
	visible: {
	  get() {
		return this.dialogVisible;
	  },
	  set(val) {
		this.$emit("update:dialogVisible", val);
	  }
	},
	form: {
	  get() {
		return this.dataForm;
	  },
	  set(val) {
		this.$emit("SetDataForm", val);
	  }
	}
  },
  model: {
	prop: "dataForm",
	event: "SetDataForm"
  },
  props: {
	dialogVisible: {
	  type: Boolean,
	  default: false
	},
	size: {
	  type: String,
	  default: "mini"
	},
	operation: {
	  type: Boolean,
	  default: false
	},
	dataForm: Object,
	dataFormRules: Object,
	columns: Array
  },
  methods: {
	// 编辑
	handleEdit: function() {
	  let callback = res => {
		this.editLoading = false;
		this.visible = false;
		if (res.data.status) {
		  this.$message({
			message: this.$t("message.sucess_edit"),
			type: "success"
		  });
		  this.$emit("update");
		} else {
		  this.$message({
			message: this.$t("message.fail_edit") + res.msg,
			type: "error"
		  });
		}
	  };

	  this.$confirm(
		this.$t("message.sure_edit"),
		this.$t("message.tips"),
		{}
	  ).then(() => {
		this.editLoading = true;
		this.$emit("action", callback);
	  });
	}
  }
};
</script>

<style>
</style>