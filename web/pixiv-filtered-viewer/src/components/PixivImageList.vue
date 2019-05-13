<template>
  <div>
    <v-layout row wrap>
      <v-flex xs12 sm10 offset-sm1>
        <v-container grid-list-sm fluid>
          <v-layout row wrap>
            <v-flex v-for="i in imgList" :key="i.id" xs6 md4 lg3 xl2 d-flex>
              <v-card flat tile class="d-flex">
                <div style="position: absolute; z-index:1">
                  <pixiv-rating
                    :value="i.rank"
                    :from-cache="i.fromCache"
                    @input="setRank(i.id,$event)"
                    v-if="$store.state.showRank"
                  ></pixiv-rating>
                </div>
                <v-img
                  :src="`${$store.state.baseUrl}/img?url=${i.imageUrls.squareMedium}`"
                  aspect-ratio="1"
                  class="grey lighten-2"
                  @click="pixiv(i.id)"
                >
                  <template v-slot:placeholder>
                    <v-layout fill-height align-center justify-center ma-0>
                      <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
                    </v-layout>
                  </template>
                </v-img>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-flex>
      <v-flex xs12>
        <infinite-loading @infinite="getImages"></infinite-loading>
      </v-flex>
    </v-layout>
  </div>
</template>
<script>
import io from "socket.io-client";
import PixivRating from "@/components/PixivRating.vue";
import InfiniteLoading from "vue-infinite-loading";
export default {
  components: {
    "pixiv-rating": PixivRating,
    "infinite-loading": InfiniteLoading
  },
  data() {
    return {
      state: null,
      imgs: []
    };
  },
  computed: {
    imgList() {
      let filtered;
      if (this.$store.state.showUnwanted) {
        if (this.$store.state.darksideMode) {
          filtered = this.imgs.filter(i => i.rank <= 2);
        } else {
          filtered = this.imgs;
        }
      } else {
        filtered = this.imgs.filter(i => i.rank > 2);
      }

      if (this.$store.state.saneMode) {
        filtered = filtered.filter(i => i.sanityLevel <= 2);
      }
      return filtered;
    }
  },
  mounted() {
    const socket = io(this.$store.state.baseUrl);
    socket.on(this.$store.state.id + "_item", this.itemAttached);
    socket.on(this.$store.state.id + "_end", this.loadFinish);
  },
  methods: {
    pixiv(id) {
      window.open(`https://pixiv.net/i/${id}`, "_blank");
    },
    async setRank(id, e) {
      let ill = this.imgList.find(i => i.id == id);
      ill.rank = e;
      ill.fromCache = true;
      this.axios.post("/api/rank", {
        id: id,
        rank: e
      });
    },
    getImages(state) {
      this.state = state;
      this.axios.get("/api/image");
    },
    itemAttached(payload) {
      if (!this.imgs.some(i => i.id == payload.id)) {
        this.imgs.push(payload);
      }
    },
    loadFinish() {
      console.log("end");
      if (this.state) {
        setTimeout(() => {
          this.state.loaded();
          this.state = null;
        }, 1000);
      }
    }
  }
};
</script>
