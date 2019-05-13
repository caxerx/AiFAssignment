import express = require("express");
import axios from "axios";
import {
  getIllusts as getIll,
  rankIllust as rankIll,
  getPixivImgBuffer
} from "./_pixiv";
import * as bodyParser from "body-parser";
const cors = require("cors");

const app: express.Application = express();
//var io = require('socket.io')(app);
app.use(bodyParser.json());
app.use(cors());

app.get("/api/res", (req, res) => {
  let next = req.query.next;
  getIll(next).then(ills => {
    if (ills.error) {
      res.status(500).send(ills.error.toString());
    } else {
      res.send(ills);
    }
  });
});

app.post("/api/rank", (req, res) => {
  let id = req.body.id;
  let rank = req.body.rank;
  rankIll(id, rank).then(resp => {
    res.send(resp.data);
  });
});

app.get("/api/img", (req, res) => {
  let url = req.query.url;
  axios({
    method: "get",
    headers: {
      Referer: "http://www.pixiv.net/"
    },
    responseType: "arraybuffer",
    url: url
  }).then(data => {
    res.set(data.headers);
    res.send(data.data);
  });
});

app.post("/api/img", (req, res) => {
  let url = req.body.url;
  getPixivImgBuffer(url).then(data => {
    res.set(data.headers);
    res.send(data.data);
  });
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Listening on port ${port}...`);
});
