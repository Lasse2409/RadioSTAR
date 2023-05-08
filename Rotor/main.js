let net = require("net");
let prompt = require("prompt-sync")({ sigint: true });

class Rotor {
	constructor(IP, port) {
		this.IP = IP;
		this.port = port;

		this.az = 0;
		this.el = 0;

		this.PH = 10;
		this.PV = 10;

		this.client = new net.Socket();
		this.client.connect(this.port, this.IP, () => {
			console.log("Rotor connected");
		
			this.status();
		});

		this.client.on("data", data => {
			this.az =  Number(data[1])*100 + Number(data[2])*10 + Number(data[3]) + Number(data[4])*0.1 - 360;
			this.el =  Number(data[6])*100 + Number(data[7])*10 + Number(data[8]) + Number(data[9])*0.1 - 360;

			this.PH = Number(data[5]);
			this.PV = Number(data[10]);

			console.log("Az = " + this.az + ", El = " + this.el); // + ", PH = " + this.PH + ", PV = " + this.PV
		});

		this.client.on("close", () => {
			console.log("Rotor disconnected");
		});
	}

	set(az, el) {
		let H = this.PH*(360 + az);
		let V = this.PV*(360 + + el);
	
		let HString = H.toString();
		let VString = V.toString();
	
		while (HString.length < 4) {
			HString = "0" + HString;
		}
	
		while (VString.length < 4) {
			VString = "0" + VString;
		}
	
		this.client.write(Buffer.from([
			0x57,
			48 + Number(HString.substring(0, 1)),
			48 + Number(HString.substring(1, 2)),
			48 + Number(HString.substring(2, 3)),
			48 + Number(HString.substring(3, 4)),
			this.PH,
			48 + Number(VString.substring(0, 1)),
			48 + Number(VString.substring(1, 2)),
			48 + Number(VString.substring(2, 3)),
			48 + Number(VString.substring(3, 4)),
			this.PV,
			0x2F,
			0x20
		]));
	}
	
	stop() {
		this.client.write(Buffer.from([0x57, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0F, 0x20]));
	}
	
	status() {
		this.client.write(Buffer.from([0x57, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0x20]));
	}

	disconnect() {
		this.client.destroy();
	}
}

function getCommand() {
	let raw = prompt("");
	let command = raw.split(" ");

	switch (command[0]) {
		case "status":
			R.status();
			break;
		case "set":
			R.set(Number(command[1]), Number(command[2]));
			break;
		case "disconnect":
			R.disconnect();
			break;
		case "stop":
			R.stop();
			break;
		default:
			console.log("Unknown command!");
	}

	setTimeout(() => {
		getCommand();
	}, 100);
}

let R = new Rotor("192.168.1.104", 23);

setTimeout(() => {
	getCommand();
}, 1000);