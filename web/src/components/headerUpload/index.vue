<template>
  <div>
    <img-upload v-model="upload_show" :width="300" :height="300" @crop-success="cropSuccess" @src-file-set="fileSet" />
    <el-avatar size="large" :src="img" v-if="img"></el-avatar>
    <el-avatar size="large" icon="el-icon-user-solid" v-else></el-avatar>

    <el-button type="primary" icon="el-icon-upload" style="position: absolute;bottom: 15px;margin-left: 30px;" @click="upload_show = true;">
      更换头像
    </el-button>
  </div>
</template>

<script>
import ImgUpload from 'vue-image-crop-upload';
export default {
  name: "headerUpload",
  props: {
    width: {
      type: Number,
      default: 300
    },
    hight: {
      type: Number,
      default: 300
    },
    img: {

    }
  },
  components: { ImgUpload },
  data() {
    return {
      upload_show: false,
    }
  },
  methods: {
    fileSet(fileName, fileType, fileSize) {
      console.log("fileSet", fileName, fileType, fileSize);
    },
    cropSuccess(imageDataUrl, field) {
      this.$emit('update:img', imageDataUrl);
    }
  }
};
</script>


<style>
</style>