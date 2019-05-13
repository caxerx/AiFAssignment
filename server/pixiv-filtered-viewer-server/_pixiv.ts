import { config } from "dotenv";
import axios from "axios";
let PixivAppApi = require("pixiv-app-api");
var FormData = require("form-data");

config();

var pixiv = new PixivAppApi(process.env.pixiv_user, process.env.pixiv_pw);
var pixiv_rank = new PixivAppApi(process.env.pixiv_user, process.env.pixiv_pw);

export async function getIllusts(next) {
  let illusts = null;
  try {
    if (pixiv.hasNext() && next) {
      illusts = await pixiv.next({
        filter: null
      });
    } else {
      illusts = await pixiv.illustRecommended({
        filter: null
      });
    }
  } catch (e) {
    return { error: e };
  }

  console.log(illusts);
  for (let i in illusts.illusts) {
    try {
      let pred = await imgPred(illusts.illusts[i].imageUrls.large);
      illusts.illusts[i].rank = pred.data.predict;
      illusts.illusts[i].fromCache = pred.data.fromCache;
    } catch (e) {
      illusts.error = e;
    }
  }
  return illusts;
}

export async function rankIllust(id, rank) {
  let detail = await pixiv_rank.illustDetail(id);
  let img = await getPixivImgStream(detail.illust.imageUrls.large);

  const form = new FormData();
  form.append("photo", img.data);
  form.append("rank", rank);
  return await axios.post("/add", form, {
    headers: {
      "Content-Type": `multipart/form-data; boundary=${form._boundary}`
    }
  });
}

async function imgPred(url) {
  let img = await getPixivImgStream(url);
  const form = new FormData();
  form.append("photo", img.data);
  return await axios.post("/predict", form, {
    headers: {
      "Content-Type": `multipart/form-data; boundary=${form._boundary}`
    }
  });
}

async function getPixivImgStream(url) {
  return await axios({
    method: "get",
    headers: {
      Referer: "http://www.pixiv.net/"
    },
    responseType: "stream",
    url: url
  });
}

export async function getPixivImgBuffer(url) {
  return await axios({
    method: "get",
    headers: {
      Referer: "http://www.pixiv.net/"
    },
    responseType: "arraybuffer",
    url: url
  });
}
