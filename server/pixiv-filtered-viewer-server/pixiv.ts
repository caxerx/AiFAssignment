import axios from "axios";
import PixivSession from "./session";
import { io } from "./index";
import { predictImage, addToDataset } from "./predict";
import * as FormData from "form-data";

export async function getIllusts(session: PixivSession, next) {
  let illusts = null;
  try {
    if (session.pixiv.hasNext() && next) {
      illusts = await session.pixiv.next({
        filter: null
      });
    } else {
      illusts = await session.pixiv.illustRecommended({
        filter: null
      });
    }
  } catch (e) {
    console.error(e);
    return { success: false };
  }

  _socketData(illusts, session);
  return { success: true };
}

async function _socketData(illusts, session) {
  let promises = [];

  for (let i in illusts.illusts) {
    try {
      promises.push(
        predictImage(illusts.illusts[i].imageUrls.large)
          .then(pred => {
            illusts.illusts[i].rank = pred.data.predict;
            illusts.illusts[i].fromCache = pred.data.fromCache;
            io.emit(session.id + "_item", illusts.illusts[i]);
          })
          .catch(e => {
            io.emit(session.id + "_error", e);
          })
      );
    } catch (e) {
      console.error(e);
      io.emit(session.id + "_end", e);
    }
  }

  Promise.all(promises).then(() => {
    io.emit(session.id + "_end", "finished");
  });
}

export async function rankIllust(id, rank, session: PixivSession) {
  let detail = await session.pixiv_rank.illustDetail(id);
  let img = await getPixivImageAsStream(detail.illust.imageUrls.large);
  return await addToDataset(img.data, rank);
}

export async function getPixivImageAsStream(url) {
  return await axios({
    method: "get",
    headers: {
      Referer: "http://www.pixiv.net/"
    },
    responseType: "stream",
    url: url
  });
}

export async function getPixivImageAsBuffer(url) {
  return await axios({
    method: "get",
    headers: {
      Referer: "http://www.pixiv.net/"
    },
    responseType: "arraybuffer",
    url: url
  });
}
