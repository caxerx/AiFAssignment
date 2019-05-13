<template>
  <v-layout>
    <v-flex xs2 style="background-color: rgba(255,255,255,.5)">
      <v-btn icon @click="setScore(1)" :disabled="!$store.state.rerankMode">
        <v-icon :color="color">{{score(1)}}</v-icon>
      </v-btn>
    </v-flex>
    <v-flex xs2 style="background-color: rgba(255,255,255,.5)">
      <v-btn icon @click="setScore(2)" :disabled="!$store.state.rerankMode">
        <v-icon :color="color">{{score(2)}}</v-icon>
      </v-btn>
    </v-flex>

    <v-flex xs2 style="background-color: rgba(255,255,255,.5)">
      <v-btn icon @click="setScore(3)" :disabled="!$store.state.rerankMode">
        <v-icon :color="color">{{score(3)}}</v-icon>
      </v-btn>
    </v-flex>

    <v-flex xs2 style="background-color: rgba(255,255,255,.5)">
      <v-btn icon @click="setScore(4)" :disabled="!$store.state.rerankMode">
        <v-icon :color="color">{{score(4)}}</v-icon>
      </v-btn>
    </v-flex>

    <v-flex xs2 style="background-color: rgba(255,255,255,.5)">
      <v-btn icon @click="setScore(5)" :disabled="!$store.state.rerankMode">
        <v-icon :color="color">{{score(5)}}</v-icon>
      </v-btn>
    </v-flex>
  </v-layout>
</template>
<script>
export default {
  props: ["value", "from-cache"],
  computed: {
    color() {
      return this.fromCache ? "blue" : "yellow darken-1";
    }
  },
  methods: {
    setScore(i) {
      this.$emit("input", i);
      this.$emit("click");
    },
    score(i) {
      if (this.value >= i) {
        return "star";
      } else {
        return "star_border";
      }
    }
  }
};
</script>