const express = require("express");
const app = express();
const http = require("http");
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

const rtljs = require("rtljs");

let device = rtljs.open(0);
device.setCenterFreq(92 * rtljs.mhz);
device.setTunerGain(49.5);
device.setSampleRate(2.4 * rtljs.mhz);

let IID = setInterval(() => {
    device.resetBuffer();
    let data = device.readSync(256*64);

    let signal = new Array();

    for (let i = 0; i < data.length/2; i++) {
        let I = Number(data[2*i])/(255/2) - 1;
        let Q = Number(data[2*i + 1])/(255/2) - 1;

        if (isNaN(I)) I = 0;
        if (isNaN(Q)) Q = 0;

        signal.push(I);
        signal.push(Q);
    }

    io.emit("data", signal);
}, 5000);

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

app.get("/fft.js", (req, res) => {
  res.sendFile(__dirname + "/fft.js");
});

io.on("connection", (socket) => {
  console.log("a user connected");
});

server.listen(3000, () => {
  console.log("listening on *:3000");
});
