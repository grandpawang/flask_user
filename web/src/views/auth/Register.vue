<template>
<div class="login-wrap">
    <div class="ms-login">
        <div class="ms-title">后台管理系统</div>
        <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="0px" class="ms-content">
            <el-form-item prop="username">
                <el-input v-model="ruleForm.username" placeholder="用户名">
                    <el-button slot="prepend" icon="el-icon-lx-people"></el-button>
                </el-input>
            </el-form-item>

            <el-form-item prop="password">
                <el-input type="password" placeholder="密码" v-model="ruleForm.password" @keyup.enter.native="submitForm('ruleForm')">
                    <el-button slot="prepend" icon="el-icon-lx-lock"></el-button>
                </el-input>
            </el-form-item>

            <el-form-item prop="fullname">
                <el-input v-model="ruleForm.fullname" placeholder="真实姓名">
                    <el-button slot="prepend" icon="el-icon-lx-profile"></el-button>
                </el-input>
            </el-form-item>

            <el-form-item prop="phone">
                <el-input v-model="ruleForm.phone" placeholder="电话号码">
                    <el-button slot="prepend" icon="el-icon-lx-mobile"></el-button>
                </el-input>
            </el-form-item>

            <div class="login-btn">
                <el-button type="primary" @click="submitForm('ruleForm')">注册/登录</el-button>
            </div>
        </el-form>
    </div>
</div>
</template>

<script>
import {
    validatePhoneTwo
} from "@/utils/validate";
import Cookies from "js-cookie";
export default {
    data: function () {
        return {
            ruleForm: {
                username: "",
                password: "",
                fullname: "",
                phone: ""
            },
            rules: {
                username: [{
                    required: true,
                    message: "请输入用户名",
                    trigger: "blur"
                }],
                password: [{
                    required: true,
                    message: "请输入密码",
                    trigger: "blur"
                }],
                fullname: [{
                    required: true,
                    message: "请输入真实姓名",
                    trigger: "blur"
                }],
                phone: [
                    // {validator:验证方法,trigger:验证触发}
                    {
                        required: true,
                        message: "请输入手机号码",
                        trigger: "blur"
                    },
                    {
                        validate: validatePhoneTwo,
                        trigger: "blur"
                    }
                ]
            }
        };
    },
    methods: {
        submitForm(formName) {
            // ref 被用来给元素或子组件注册引用信息。引用信息将会注册在父组件的 $refs 对象上。
            // 如果在普通的 DOM 元素上使用，引用指向的就是 DOM 元素
            this.$refs[formName].validate(valid => {
                if (valid) {
                    this.$api.auth.register(this.ruleForm)
                        .then(response => {
                            console.log(response)
                            if (response.data.status === true) {
                                // 注册成功
                                this.$api.auth.login({
                                        username: this.ruleForm.username,
                                        password: this.ruleForm.password
                                    })
                                    .then(response => {
                                        Cookies.set('authenticate', `jwt ${response.data.access_token}`, 1 / 12)
                                        this.$store.commit('updateUserInfo', res.data.data);
                                        // console.log(res.data.data)   
                                        this.$router.push("/")
                                    })
                            } else {
                                // 注册失败
                                alert(response.data.msg);
                            }
                        });
                    // localStorage.setItem('ms_username',this.ruleForm.username);
                    // this.$router.push('/');
                } else {
                    console.log("error submit!!");
                    return false;
                }
            });
        }
    }
};
</script>

<style scoped>
.login-wrap {
    position: relative;
    width: 100%;
    height: 100%;
    background-image: '@/assets/img/login-bg.jpg';
    background-size: 100%;
}

.ms-title {
    width: 100%;
    line-height: 50px;
    text-align: center;
    font-size: 20px;
    color: #fff;
    border-bottom: 1px solid #ddd;
}

.ms-login {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 350px;
    margin: -190px 0 0 -175px;
    border-radius: 5px;
    background: rgba(22, 211, 117, 0.3);
    overflow: hidden;
}

.ms-content {
    padding: 30px 30px;
}

.login-btn {
    text-align: center;
}

.login-btn button {
    width: 100%;
    height: 36px;
    margin-bottom: 10px;
}

.login-tips {
    font-size: 12px;
    line-height: 30px;
    color: #fff;
}
</style>
