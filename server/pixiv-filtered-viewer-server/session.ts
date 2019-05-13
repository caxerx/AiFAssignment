let PixivAppApi = require("pixiv-app-api");
export default class PixivSession {
  id: any;
  pixiv: any;
  pixiv_rank: any;
  constructor(id, username, password) {
    this.id = id;
    this.pixiv = new PixivAppApi(username, password);
    this.pixiv_rank = new PixivAppApi(username, password);
  }
}
