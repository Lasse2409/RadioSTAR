const rtljs = require("rtljs");
const fs = require("fs");

console.log(rtljs.getDeviceCount()); // 1
console.log(rtljs.getDeviceName(0)); // Generic RTL R820T2

let device = rtljs.open(0);
device.setCenterFreq(1420 * rtljs.mhz);
device.setTunerGain(496); //STUPID GAIN CONVENTION!!!!! );
device.setSampleRate(2.4 * rtljs.mhz)

let samples = "";

let printCounter = 0;

let N = 100;

let writer = fs.createWriteStream("data.dat", {
    flags: "w"
});

for (let j = 0; j < N; j++) {
    printCounter++;

    if (printCounter > N/100) {
        printCounter = 0;

        console.log(j/N*100 + " %");
    }

    device.resetBuffer();
    let data = device.readSync(512*1024);
    //let data = device.readSync(512);

    for (let i = 0; i < data.length/2; i++) {
        let I = Number(data[2*i]);
        //let I = Number(data[2*i])/(255/2) - 1;
        let Q = Number(data[2*i + 1]);
        //let Q = Number(data[2*i + 1])/(255/2) - 1;

        if (Q > 0) {
            samples = samples + I + "+" + Q + "i"
        } else {
            samples = samples + I + "" + Q + "i"
        }

        if (i < data.length/2 - 1) {
            samples = samples + ", "
        }

        //saveCounter++;

        //if (saveCounter > 512) {
        //    saveCounter = 0;
        //    samples = samples + "\n";
        //}
    }

    writer.write(samples);
    samples = "";

    //samples = samples + "\n";
}

rtljs.close(device);

writer.close();

//fs.writeFileSync("./data.dat", samples);
