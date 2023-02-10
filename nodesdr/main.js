const rtljs = require("rtljs");
const fs = require("fs");

console.log(rtljs.getDeviceCount()); // 1
console.log(rtljs.getDeviceName(0)); // Generic RTL R820T2

let device = rtljs.open(0);
device.setCenterFreq(92 * rtljs.mhz);
device.setTunerGain(1);
device.setSampleRate(2.4 * rtljs.mhz)

let samples = "";

for (let j = 0; j < 10; j++) {
    console.log("j = " + j);

    // raw IQ data
    device.resetBuffer(); // reset buffer to prevent communication data from appearing as radio data
    let data = device.readSync(256*1024); // read 512b

    for (let i = 0; i < data.length/2; i++) {
        let I = Number(data[2*i])/(255/2) - 1;
        let Q = Number(data[2*i + 1])/(255/2) - 1;

        if (Q > 0) {
            samples = samples + I + "+" + Q + "i, "
        } else {
            samples = samples + I + "" + Q + "i, "
        }
    }

    samples = samples + "\n";
}

rtljs.close(device);

fs.writeFileSync("./data.dat", samples);
