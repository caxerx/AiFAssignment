<template>
  <v-app>
    <v-toolbar app color="primary" dark :flat="$route.name=='login'">
      <v-toolbar-title class="headline text-uppercase">
        <span>Pixiv</span>
        <span class="font-weight-light">Viewer</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon v-if="$route.name!='login'" @click="setting=true">
        <v-icon>settings</v-icon>
      </v-btn>
    </v-toolbar>

    <v-content>
      <router-view></router-view>

      <v-snackbar :timeout="0" auto-height v-model="training" right>
        <v-layout row wrap>
          <v-flex xs12>{{status}}</v-flex>
          <v-flex xs12>
            <v-progress-linear v-model="percentage"></v-progress-linear>
          </v-flex>
        </v-layout>
      </v-snackbar>
    </v-content>
    <v-dialog v-model="setting" max-width="500">
      <v-card color="primary" dark>
        <v-card-text>
          <div class="mb-2" style="color: rgba(255,255,255,.70)">Rating Setting</div>
          <v-divider></v-divider>
          <v-layout row wrap>
            <v-flex xs6>
              <v-switch
                :label="`Show Unwanted Image`"
                color="white"
                hint="Show unfiltered image list"
                persistent-hint
                v-model="$store.state.showUnwanted"
                @change="unwanted"
              ></v-switch>
            </v-flex>
            <v-flex xs6>
              <v-switch
                :label="`Darkside`"
                color="red"
                hint="Show Unwanted Image ONLY"
                persistent-hint
                :disabled="!$store.state.showUnwanted"
                v-model="$store.state.darksideMode"
                @change="darkside"
              ></v-switch>
            </v-flex>

            <v-flex xs6>
              <v-switch
                :label="`Show Rank`"
                hint="Show rank of the image"
                persistent-hint
                v-model="$store.state.showRank"
                color="white"
                @change="rank"
              ></v-switch>
            </v-flex>
            <v-flex xs6>
              <v-switch
                :label="`Rerank Mode`"
                hint="Allow adding image to dataset"
                persistent-hint
                :disabled="!$store.state.showRank"
                v-model="$store.state.rerankMode"
                color="white"
                @change="rerank"
              ></v-switch>
            </v-flex>
          </v-layout>
          <div class="mb-2 mt-4" style="color: rgba(255,255,255,.70)">Safe Setting</div>
          <v-divider></v-divider>

          <v-switch
            :label="`Sanity Mode`"
            color="white"
            v-model="$store.state.saneMode"
            @change="sane"
            hint="Safe for work (Maybe)"
            persistent-hint
          ></v-switch>
          <div class="mb-2 mt-4" style="color: rgba(255,255,255,.70)">Model Setting</div>
          <v-divider></v-divider>
          <v-layout row class="mt-2">
            <v-flex>
              <v-btn color="red" @click="retrainConfirm=true" :disabled="training">{{retrainBtn}}</v-btn>
            </v-flex>
            <v-flex>
              <span
                class="caption"
                style="color: rgba(255,255,255,.85)"
              >Retrain model will takes at least 10 minutes, you can still use the system while model training</span>
            </v-flex>
          </v-layout>
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog v-model="retrainConfirm" max-width="400">
      <v-card>
        <v-card-title>Retrain Model</v-card-title>
        <v-divider></v-divider>
        <v-card-text>Are you sure to retrain the model? This will takes at least 10 minutes.</v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat color="red" @click="confirmRetrain()">Retrain Model</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import io from "socket.io-client";
export default {
  name: "App",
  mounted() {
    this.axios.get("/api/trainstatus").then(res => {
      this.training = res.data.training;
      this.percentage = res.data.progress;
      this.status = res.data.status;
    });
    const socket = io(this.$store.state.baseUrl);
    socket.on("model", this.modelStatus);
  },
  computed: {
    retrainBtn() {
      return this.training ? "Model training" : "Retrain Model";
    }
  },
  methods: {
    unwanted(status) {
      this.$store.commit("unwanted", status || false);
    },
    darkside(status) {
      this.$store.commit("darkside", status || false);
    },
    rank(status) {
      this.$store.commit("rank", status || false);
    },
    rerank(status) {
      this.$store.commit("rerank", status || false);
    },
    sane(status) {
      this.$store.commit("sane", status || false);
    },
    modelStatus(payload) {
      if (payload.status == "Finished") {
        this.training = false;
      } else {
        this.training = true;
      }
      this.status = payload.status;
      this.percentage = payload.progress;
    },
    async confirmRetrain() {
      this.training = true;
      this.setting = false;
      this.retrainConfirm = false;
      await this.axios.get("/api/retrain");
    }
  },
  data() {
    return {
      status: "Waiting",
      training: false,
      percentage: 0,
      setting: false,
      retrainConfirm: false
    };
  }
};
</script>
