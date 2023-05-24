%% load data
clc
close all
clear;

P = 256;
c = 3E5;

ps = zeros(P, 1);
psCalibration = zeros(P, 1);
freq = zeros(P,1);


BWPerElement = (freq(end,1) - freq(1,1))/P;

Hline = 1.420405e+3;
line1 = 1.42045e+3;
line2 = 1.42080e+3;

ElementOfFreq1 = round((line1 - freq(1,1))/BWPerElement);
ElementOfFreq2 = round((line2 - freq(1,1))/BWPerElement);
ElementOfFreqH = round((Hline - freq(1,1))/BWPerElement);

filename= "data/calibration/calibrationData-1.dat";
data = readtable(filename);
psCalibration(:,1) = table2array(data(:, 1));

filename= "data/rotationcurve/rotationcurveData-110.dat";
%filename= "data/single/s7Data-[132  -1].dat";
data = readtable(filename);


ps(:,1) = table2array(data(:, 1));
freq(:,1) = table2array(data(:, 2));

%vel = (c * (Hline-freq) ./ freq);
vel = (c * (freq-Hline) ./ freq);

%% Plotting raw spectrum
figure();
plot(freq,ps)

%% Calibrating raw data by fitting

ps_cal = zeros(size(ps));    

v = 1:length(ps(:,1));
l = v.'

start1 = 90;
end1 = 150;
start2 = 230;

d = ps(:,1);

figure();
plot(l,d)
hold on
plot(ones(1,10)*start1, linspace(0,max(ps),10))
hold on
plot(ones(1,10)*end1, linspace(0,max(ps),10))
hold on
plot(ones(1,10)*start2, linspace(0,max(ps),10))
hold on
plot(ones(1,10)*l(end), linspace(0,max(ps),10))
hold on

fit_x = [l(start1:end1).', l(start2:end).'];
fit_y = [d(start1:end1).', d(start2:end).'];

p1 = polyfit(fit_x,fit_y,6);
y1 = polyval(p1,l(start1:end));

plot(l(start1:end), y1)
hold on
d(start1:end) = y1; %replace second half with fitted data (to avoid the h line)

p2 = polyfit(l.', d, 10);
y2 = polyval(p2,l.').';
plot(l,y2)
hold on 

ps_cal(:,1) = ps(:,1) - y2;

plot(l,ps_cal)

%% Calibrating by subtracting calibration measurement

precission = 0.1*(1E-3);
k = 0;
for i = 1:1000
    psCalibrationScaled = k*psCalibration;
    a = ps(121) - psCalibrationScaled(121)

    if abs(a)<precission
        break
    else
        k = k + 0.01
    end
end

figure();
plot(freq, psCalibrationScaled)
hold on 
plot(freq, ps)
hold on 
plot(freq, ps-psCalibrationScaled)


%% Comparing two calibration methods
figure();
plot(vel,ps_cal)
hold on
plot(vel, ps-psCalibration)
