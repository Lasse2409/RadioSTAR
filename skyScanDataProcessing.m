%% load data
clc
close all
clear;


gridSize = [20, 20];

az_start = 160;
az_stop = 250;

el_start = 10;
el_stop = 50;


N = gridSize(1)*gridSize(2);
P = 256;

ps = zeros(P, N);
freq = zeros(P,N);



for i = 1:N
    filename= sprintf("data/maps/1/data-%d.dat",i-1);
    data = readtable(filename);
    
    ps(:,i) = table2array(data(:, 1));
    freq(:,i) = table2array(data(:, 2));

end


BWPerElement = (freq(end,1) - freq(1,1))/P;

Hline = 1.4204e+3;
line1 = 1.42045e+3;
line2 = 1.42080e+3;

ElementOfFreq1 = round((line1 - freq(1,1))/BWPerElement);
ElementOfFreq2 = round((line2 - freq(1,1))/BWPerElement);
ElementOfFreqH = round((Hline - freq(1,1))/BWPerElement);

%% Plotting raw spectra
for i = 1:N
    figure(1);
    clf;
    hold on;
    plot(freq(:,i), ps(:,i));
    ylim([0 1E-2])
    plot(ones(10,1)*(Hline), linspace(0,1E-2,10))
    i
    pause(0.05)
end
%% Fitting all spectra

ps_cal = zeros(size(ps));    

v = 1:length(ps(:,1));
l = v.'

start1 = 90;
end1 = 170;
start2 = 220;

for t = 1:N
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


%% Plotting all fitted spectra


for i = 1:N
    figure(2);
    clf;
    hold on;
    plot(freq(:,i), ps_cal(:,i));
    ylim([-2E-3 3E-3])
    plot(ones(10,1)*(Hline), linspace(0,1E-3,10))
    hold on 
    plot(ones(10,1)*(line1), linspace(0,1E-3,10))
    hold on 
    plot(ones(10,1)*(line2), linspace(0,1E-3,10))
    pause(0.1)
end


%% Fitting individual
close all
t = 83;


d = ps(:,t);
v = 1:length(d);
l = v.'

start1 = 90;
end1 = 170;
start2 = 220;

fit_x = [l(start1:end1).', l(start2:end).'];
fit_y = [d(start1:end1).', d(start2:end).'];

p1 = polyfit(fit_x,fit_y,6);
y1 = polyval(p1,l(start1:end));
d(start1:end) = y1 %replace second half with fitted data (to avoid the h line)


% plot 
figure;
plot(l.', ps(:,t)); %Plot raw data on simple x axis
hold on

plot(l.',d) %plot raw data with halffitted data
hold on

% fitting the M shape 
p2 = polyfit(l.', d, 10);
y2 = polyval(p2,l.');

plot(l.',y2); %plot the final fit og M shape


figure();
plot(freq(:,t),ps(:,t)-y2.');


%% plot map



map = zeros(gridSize(1), gridSize(2));

for i = 1:gridSize(1)  %column (az)
    for j = 1:gridSize(2) %row (el)

        if mod(i, 2) == 0 
            k = i*gridSize(2) - j + 1;
        else
            k = (i-1)*gridSize(2) + j;
        end

        %data = readtable("data/data-" + (k-1) + ".dat");
    
        %ps = table2array(data(:, 1));
        %freq = table2array(data(:, 2));

        %map(j, i) = max(ps_cal(:,k));
        map(j, i) = max(ps_cal(ElementOfFreq1:ElementOfFreq2,k));
        %k
        k = k + 1;
        %pause(0.5)
    end
end

figure();
clf;
x = [az_start az_stop];
y = [el_start el_stop];
imagesc(x,y,flipud(map));
set(gca,'YDir','normal')

colorbar;
%colormap("gray");