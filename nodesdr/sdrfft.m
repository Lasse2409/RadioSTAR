data = readmatrix("data.dat");

%I = data(:, 1);
%Q = data(:, 2);

%iq = I + 1i*Q;

data(isnan(data)) = 0;

s = size(data);

temp = pwelch(data(1, :));

x = zeros(s(1), length(temp));

for N = 1:s(1)
    x(N, 1:length(temp)) = pwelch(data(N, :));
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
cf = 1420;%*10^6;

fulldata = readmatrix("data.dat");
fulldata(isnan(fulldata)) = 0;

figure(1);
clf;
hold on;

q = 256;
Q = floor(length(fulldata)/q);

power = zeros(Q, q);

for k = 1:Q
    data = fulldata((q*(k-1)+1):(q*k));
    
    N = length(data);
    
    %s = size(data);
    
    %X = zeros(s(1), N);
    
    %N = s(1);
    
    a0 = 0.3635819;
    a1 = 0.4891775;
    a2 = 0.1365995;
    a3 = 0.0106411;
    
    n = 0:(N-1);
    
    w = a0 - a1*cos(2*pi*n/N)+a2*cos(4*pi*n/N)-a3*cos(6*pi*n/N);
    
    %for i = 1:s(1)
    %    Y = fft(data(1, :));
    %    Y(1) = 0;
    %    X(i, :) = fftshift(Y);
    %end
    
    Y = fft(w.*data);
    %Y(1) = 0;
    X = fftshift(Y);
    
    %power = abs(mean(X)).^2/n;
    power(k, :) = abs(X).^2/N;
end

power = 10*log10(mean(power));

%power(power > 20) = mean(power(20:30));
pTemp = power(power < 20);

fshift = (-N/2:N/2-1)*(fs/N) + cf;

fshift = fshift(power < 20);
power = pTemp;

plot(fshift, power);

xlabel("Frequency [MHZ]", "Interpreter", "Latex");
ylabel("Power [arb. units]", "Interpreter", "Latex");
