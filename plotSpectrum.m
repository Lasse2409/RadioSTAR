%% load data
clc
close all
clear;

P = 256;

ps = zeros(P, 1);
freq = zeros(P,1);

BWPerElement = (freq(end,1) - freq(1,1))/P;

Hline = 1.4204e+3;
line1 = 1.42045e+3;
line2 = 1.42080e+3;

ElementOfFreq1 = round((line1 - freq(1,1))/BWPerElement);
ElementOfFreq2 = round((line2 - freq(1,1))/BWPerElement);
ElementOfFreqH = round((Hline - freq(1,1))/BWPerElement);


filename= "data/single/singleData-1.dat";
data = readtable(filename);

ps(:,1) = table2array(data(:, 1));
freq(:,1) = table2array(data(:, 2));

figure();
plot(freq,ps)

%% Fit raw data

ps_cal = zeros(size(ps));    

v = 1:length(ps(:,1));
l = v.'

start1 = 90;
end1 = 170;
start2 = 220;

d = ps(:,1);

fit_x = [l(start1:end1).', l(start2:end).'];
fit_y = [d(start1:end1).', d(start2:end).'];

p1 = polyfit(fit_x,fit_y,6);
y1 = polyval(p1,l(start1:end));
d(start1:end) = y1; %replace second half with fitted data (to avoid the h line)

p2 = polyfit(l.', d, 10);
y2 = polyval(p2,l.').';

ps_cal(:,1) = ps(:,1) - y2;

figure();
plot(freq,ps_cal)
