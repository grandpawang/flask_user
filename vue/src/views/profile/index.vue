<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-calendar"></i> 个人中心
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="app-container">
      <el-row :gutter="10">
        <el-col :xs="9" :sm="8" :md="7" :lg="6" :xl="5">
          <user-card :user="user" class="user-card" />
        </el-col>
        <el-col :xs="15" :sm="16" :md="17" :lg="18" :xl="19">
          <el-card class="user-tab">
            <el-tabs v-model="activeTab">
              <el-tab-pane label="Activity" name="activity">
                <!-- <activity /> -->
              </el-tab-pane>
              <el-tab-pane label="Timeline" name="timeline">
                <!-- <timeline /> -->
              </el-tab-pane>
              <el-tab-pane label="Account" name="account">
                <!-- <account :user="user" /> -->
              </el-tab-pane>
            </el-tabs>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import UserCard from "./components/UserCard";
export default {
  name: "profile",
  components: {
    UserCard
  },
  data: function() {
    return {};
  },
  computed: {
    ...mapState({
      user: state => state.user.info
    })
  },
  methods: {}
};
</script>

<style scoped lang="scss">

</style>