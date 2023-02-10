data = readmatrix("datadown.dat");

%I = data(:, 1);
%Q = data(:, 2);

%iq = I + 1i*Q;

data(isnan(data)) = 0;

s = size(data);

temp = pwelch(data(1, :));

x = zeros(s(1), length(temp));

for n = 1:s(1)
    x(n, 1:length(temp)) = pwelch(data(n, :));
end

figure(1);
hold on;
%plot(temp);
plot(log(mean(x)));

background = mean(x);


%% asd

figure(2);
clf;
hold on;
plot(log(foreground-background));


%% manuel
clear;

fs = 2.4;%*10^6;
cf = 92;%*10^6;

data = readmatrix("data.dat");
data(isnan(data)) = 0;
n = length(data(1, :));

s = size(data);

X = zeros(s(1), n);

for i = 1:s(1)
    Y = fft(data(1, :));
    Y(1) = 0;
    X(i, :) = fftshift(Y);
end

power = abs(mean(X)).^2/n;
fshift = (-n/2:n/2-1)*(fs/n) + cf;

figure(1);
clf;
hold on;
plot(fshift, power);
xlabel("Frequency [MHZ]", "Interpreter", "Latex");
ylabel("Power [arb. units]", "Interpreter", "Latex");
