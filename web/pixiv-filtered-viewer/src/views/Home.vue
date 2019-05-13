<template>
  <v-fade-transition>
    <PixivImageList v-if="loaded"/>
  </v-fade-transition>
</template>

<script>
import PixivImageList from "../components/PixivImageList";

export default {
  components: {
    PixivImageList
  },
  data() {
    return {
      loaded: false
    };
  },
  methods: {
    async checkLogin() {
      try {
        let resp = await this.axios.get("/api/loginstatus");
        if (resp.data.loggedIn) {
          this.loaded = true;
        } else {
          this.$router.replace("/login");
        }
      } catch {
        this.$router.replace("/login");
      }
    }
  },
  mounted() {
    this.checkLogin();
  }
};
</script>
