import * as express from "express";
import * as bodyParser from "body-parser";
import * as socketio from "socket.io";
import * as cors from "cors";
import * as PixivAppApi from "pixiv-app-api";
import PixivSession from "./session";
import axios from "axios";
import { getIllusts, getPixivImageAsBuffer, rankIllust } from "./pixiv";
import { retrain } from "./predict";
axios.defaults.baseURL = "http://127.0.0.1:5000";

const app: express.Application = express();
app.set("port", process.env.PORT || 3000);

let http = require("http").Server(app);
export let io = socketio(http);

let pixivSession = {};

let trainStatus = { training: false, status: "", progress: 0 };

app.use(bodyParser.json());
app.use(cors());

app.get("/img", (req, res) => {
  let url = req.query.url;
  getPixivImageAsBuffer(url).then(data => {
    res.set(data.headers);
    res.send(data.data);
  });
});

app.get("/api/image", (req, res) => {
  let id;
  let session;
  let next = req.query.next || false;
  if ((id = req.headers["id"])) {
    if ((session = pixivSession[id])) {
      getIllusts(session, next);
      res.send({ success: true });
    } else {
      res.status(401).send({ success: false });
    }
  } else {
    res.status(400).send({ success: false });
  }
});

app.get("/api/trainstatus", (req, res) => {
  res.send(trainStatus);
});

app.get("/api/loginstatus", (req, res) => {
  let id;

  if ((id = req.headers["id"])) {
    if (pixivSession[id]) {
      res.send({ loggedIn: true });
    } else {
      res.send({ loggedIn: false });
    }
  } else {
    res.status(400).send({ loggedIn: false });
  }
});

app.post("/api/status", (req, res) => {
  console.log("train status updated");
  let payload = req.body;
  console.log(payload);
  if (payload.status != "Finished") {
    trainStatus.training = true;
  } else {
    trainStatus.training = false;
  }
  trainStatus.status = payload.status;
  trainStatus.progress = payload.progress;
  modelStatus(payload.status, payload.progress);
  res.send({ success: true });
});

app.post("/api/rank", (req, res) => {
  let id = req.body.id;
  let rank = req.body.rank;

  let sessid;
  let session;
  if ((sessid = req.headers["id"])) {
    if ((session = pixivSession[sessid])) {
      rankIllust(id, rank, session).then(resp => {
        res.send(resp.data);
      });
    } else {
      res.status(401).send({ success: false });
    }
  } else {
    res.status(400).send({ success: false });
  }
});

app.post("/api/login", (req, res) => {
  let id;
  if ((id = req.headers["id"])) {
    new PixivAppApi()
      .login(req.body.username, req.body.password)
      .then(r => {
        pixivSession[id] = new PixivSession(
          id,
          req.body.username,
          req.body.password
        );
        res.send({ success: true });
      })
      .catch(e => {
        res.status(400).send({ success: false });
      });
  } else {
    res.status(400).send({ success: false });
  }
});

app.get("/api/retrain", (req, res) => {
  retrain().then(resp => {
    res.send(resp.data);
  });
});

io.on("connection", function(socket: any) {
  console.log("a user connected");
});

const server = http.listen(3000, function() {
  console.log("listening on *:3000");
});

async function modelStatus(status, progress) {
  io.emit("model", { status: status, progress: progress });
}
