<template>
  <v-layout justify-center align-center>
    <v-flex xs1></v-flex>
    <v-flex xs2>
      <v-btn icon @click="setScore(1)">
        <v-icon :color="color">{{score(1)}}</v-icon>
      </v-btn>
    </v-flex>
    <v-flex xs2>
      <v-btn icon @click="setScore(2)">
        <v-icon :color="color">{{score(2)}}</v-icon>
      </v-btn>
    </v-flex>

    <v-flex xs2>
      <v-btn icon @click="setScore(3)">
        <v-icon :color="color">{{score(3)}}</v-icon>
      </v-btn>
    </v-flex>

    <v-flex xs2>
      <v-btn icon @click="setScore(4)">
        <v-icon :color="color">{{score(4)}}</v-icon>
      </v-btn>
    </v-flex>

    <v-flex xs2>
      <v-btn icon @click="setScore(5)">
        <v-icon :color="color">{{score(5)}}</v-icon>
      </v-btn>
    </v-flex>

    <v-flex xs1></v-flex>
  </v-layout>
</template>
<script>
export default {
  props: ["value"],
  computed: {
    color() {
      return "yellow darken-1";
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