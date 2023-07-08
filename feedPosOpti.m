%% load data
clc
close all
clear;

N = 10;
P = 256;

ps = zeros(P, N);
freqz = zeros(P,N);


for i = 1:N
    filename= sprintf("data/single/singleData-%d.dat",i);
    data = readtable(filename);

    ps(:,i) = table2array(data(:, 1));
    freq(:,i) = table2array(data(:, 2));


end
%% Plotting raw spectra from drift scan
for i = 1:N
    figure(1);
    %clf;
    hold on;
    plot(freq(:,i), ps(:,i), "DisplayName", "a" + i);
    ylabel('gain')
    xlabel('frequency [MHz]')
    %ylim([0 2E-2])
    pause(0.1)
end

legend

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
