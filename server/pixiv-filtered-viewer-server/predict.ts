import axios from "axios";
import * as FormData from "form-data";
import { getPixivImageAsStream } from "./pixiv";

export async function predictImage(url) {
  let img = await getPixivImageAsStream(url);
  const form = new FormData();
  form.append("photo", img.data);
  return await axios.post("/predict", form, {
    headers: {
      "Content-Type": `multipart/form-data; boundary=${form._boundary}`
    }
  });
}

export async function addToDataset(image, rank) {
  const form = new FormData();
  form.append("photo", image);
  form.append("rank", rank);
  return await axios.post("/add", form, {
    headers: {
      "Content-Type": `multipart/form-data; boundary=${form._boundary}`
    }
  });
}

export async function retrain() {
  return await axios.get("/retrain");
}
