import Vue from "vue";
import store from "./store";
import "./plugins/vuetify";
import "./plugins/axios";
import App from "./App.vue";
import router from "./router";
import "roboto-fontface/css/roboto/roboto-fontface.css";
import "material-design-icons-iconfont/dist/material-design-icons.css";

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
