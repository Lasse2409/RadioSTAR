%% load data
clc
close all
clear;

numMeasurements = 21;
angIncrometn = 1;
P = 256;

psAz = zeros(P, numMeasurements);
freqAz = zeros(P,numMeasurements);

psEl = zeros(P, numMeasurements);
freqEl = zeros(P,numMeasurements);

for i = 1:numMeasurements
    filename= sprintf("data/pointing/sun/sunPointingData-Az%d.dat",i-1);
    dataAz = readtable(filename);
    filename= sprintf("data/pointing/sun/sunPointingData-El%d.dat",i-1);
    dataEl = readtable(filename);

    psAz(:,i) = table2array(dataAz(:, 1));
    freqAz(:,i) = table2array(dataAz(:, 2));

    psEl(:,i) = table2array(dataEl(:, 1));
    freqEl(:,i) = table2array(dataEl(:, 2));

end



%% Plotting raw spectra from drift scan
for i = 1:numMeasurements
    figure(1);
    %clf;
    hold on;
    %plot(freqAz(:,i), psAz(:,i));
    plot(freqEl(:,i), psEl(:,i));
    title('Spectra from azimuth drift scan (+- 14 degrees)')
    ylabel('gain')
    xlabel('frequency [MHz]')
    ylim([0 2E-2])
    pause(0.1)
end


%% Plot azimuth pointing

azPeaks = zeros(numMeasurements,1);
az = zeros(numMeasurements,1);


for i = 1:numMeasurements
    az(i) = -0.5 * (numMeasurements-1) * angIncrometn + (i-1)*angIncrometn;
end

azPeaks = max(psAz)';

[azMax, azMaxIdx] = max(azPeaks);

azOffset = az(azMaxIdx)  %the amount by which there is an offset

figure();
plot(az, azPeaks)
title(['Azimuth scan gain maxima of BB radiation (Sun)'])
ylabel('gain maxima')
xlabel('frequency [MHz]')
hold on 
plot(ones(1,10)*azOffset, linspace(0,1.5E-2,10))



%% Plot elevation pointing

elPeaks = zeros(numMeasurements,1);
el = zeros(numMeasurements,1);


for i = 1:numMeasurements
    el(i) = -0.5 * (numMeasurements-1) * angIncrometn + (i-1)*angIncrometn;
end

elPeaks = max(psEl)';

[elMax, elMaxIdx] = max(elPeaks);

elOffset = el(elMaxIdx) %the amount by which there is an offset

figure();
plot(el, elPeaks)
title(['Elevation scan gain maxima of BB radiation (Sun)'])
ylabel('gain maxima')
xlabel('frequency [MHz]')
hold on 
plot(ones(1,10)*elOffset, linspace(0,1.5E-2,10))





