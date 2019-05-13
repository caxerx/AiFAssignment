import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    id: null,
    baseUrl: "https://srvbest.1lo.li",
    saneMode: true,
    showUnwanted: false,
    darksideMode: false,
    showRank: false,
    rerankMode: false
  },
  mutations: {
    id(state, payload) {
      state.id = payload;
    },
    unwanted(state, opt) {
      state.showUnwanted = opt;
      if (opt == false) {
        state.darksideMode = false;
      }
    },
    rank(state, opt) {
      state.showRank = opt;
      if (opt == false) {
        state.rerankMode = false;
      }
    },
    rerank(state, opt) {
      state.rerankMode = opt;
    },
    darkside(state, opt) {
      state.darksideMode = opt;
    },
    sane(state, opt) {
      state.saneMode = opt;
    }
  },
  actions: {}
});
