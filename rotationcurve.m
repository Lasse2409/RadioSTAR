%% load data
clc
close all
clear;

dataIncroments = 1;
dataStart = 3;
dataEnd = 155;
datapoints = (dataEnd-dataStart)/dataIncroments +1;

P = 2^8; %8 bit ADC: RTL2832U 8-bits


ps = zeros(P, datapoints);
freq = zeros(P,datapoints);

%BWPerElement = (freq(end,1) - freq(1,1))/P;

%Hline = 1.4204e+3;
%line1 = 1.42045e+3;
%line2 = 1.42080e+3;

%ElementOfFreq1 = round((line1 - freq(1,1))/BWPerElement);
%ElementOfFreq2 = round((line2 - freq(1,1))/BWPerElement);
%ElementOfFreqH = round((Hline - freq(1,1))/BWPerElement);

k = 0;
for i = dataStart:dataIncroments:dataEnd
    k = k+1;
    filename= sprintf("data/rotationcurve/rotationcurveData-%d.dat",i);
    data = readtable(filename);
    
    ps(:,k) = table2array(data(:, 1));
    freq(:,k) = table2array(data(:, 2));
   
end

%% Plotting raw spectra 
for i = 1:datapoints
    figure(1);
    %clf;
    hold on;
    plot(freq(:,i), ps(:,i));
    title('Raw spectra from rotationcurve datapoints')
    ylabel('gain')
    xlabel('frequency [MHz]')
    %ylim([0 2E-2])
    pause(0.2)
end
%%
figure();
plot(freq(:,30), ps(:,30));
hold on 
plot(freq(:,end), 0.9*ps(:,end))
hold on 
plot(freq(:,end), ps(:,30) - 0.9*ps(:,end))


%% Fitting all spectra

ps_cal = zeros(size(ps));    

v = 1:length(ps(:,1));
l = v.'

start1 = 90;
end1 = 170;
start2 = 220;

for t = 1:datapoints
    d = ps(:,t);

    fit_x = [l(start1:end1).', l(start2:end).'];
    fit_y = [d(start1:end1).', d(start2:end).'];
    
    p1 = polyfit(fit_x,fit_y,6);
    y1 = polyval(p1,l(start1:end));
    d(start1:end) = y1; %replace second half with fitted data (to avoid the h line)

    p2 = polyfit(l.', d, 10);
    y2 = polyval(p2,l.').';
    
    ps_cal(:,t) = ps(:,t) - y2;
end

%% x axis to velocity


%% Plotting all fitted spectra


for i = 1:datapoints
    figure(2);
    %clf;
    hold on;
    plot(freq(:,i), ps_cal(:,i));
    %ylim([-2E-3 3E-3])
    %plot(ones(10,1)*(Hline), linspace(0,1E-3,10))
    %hold on 
    %plot(ones(10,1)*(line1), linspace(0,1E-3,10))
    %hold on 
    %plot(ones(10,1)*(line2), linspace(0,1E-3,10))
    pause(0.5)
end

%%
