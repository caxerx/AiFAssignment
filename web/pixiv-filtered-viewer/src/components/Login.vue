<template>
  <v-layout
    justify-center
    align-center
    fill-height
    :style="`background-color: ${$vuetify.theme.primary}`"
  >
    <div style="width: 300px">
      <v-layout row wrap>
        <v-flex
          xs12
          class="text-xs-center white--text display-1 font-weight-thin my-3"
        >Login to Pixiv</v-flex>
        <v-flex xs12>
          <v-form @submit.prevent="login">
            <v-text-field
              single-line
              outline
              color="white"
              dark
              prepend-inner-icon="account_circle"
              type="password"
              v-model="user"
            ></v-text-field>
          </v-form>
          <v-form @submit.prevent="login">
            <v-text-field
              single-line
              outline
              dark
              color="white"
              prepend-inner-icon="lock"
              type="password"
              v-model="pw"
            ></v-text-field>
          </v-form>
        </v-flex>
        <v-flex xs12>
          <v-layout justify-center align-center>
            <div style="height:40px">
              <v-progress-circular indeterminate color="white" width="3" v-if="loading"></v-progress-circular>
              <v-btn
                outline
                dark
                @click="login"
                :color="fail?'red lighten-3':'white'"
                v-else
              >{{fail?"Login Failed":"Login"}}</v-btn>
            </div>
          </v-layout>
        </v-flex>
      </v-layout>
    </div>
  </v-layout>
</template>

<script>
export default {
  mounted() {},
  data() {
    return {
      loading: false,
      fail: false,
      user: "",
      pw: ""
    };
  },
  methods: {
    async login() {
      this.loading = true;
      try {
        let resp = await this.axios.post("/api/login", {
          username: this.user,
          password: this.pw
        });
        if (resp.data.success) {
          this.$router.replace("/");
        }
      } catch {
        this.fail = true;
      }
      this.loading = false;
    }
  }
};
</script>
<style>
</style>
