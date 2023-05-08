%% load data
clc
close all
clear;

N = 400;
P = 256;

ps = zeros(P, N);
freq = zeros(P,N);

for i = 1:N
    filename= sprintf("data/data-%d.dat",i-1);
    data = readtable(filename);
    
    ps(:,i) = table2array(data(:, 1));
    freq(:,i) = table2array(data(:, 2));

end

%% Plotting individual measurements
for i = 1:N
    figure(1);
    clf;
    hold on;
    plot(freq(:,i), ps(:,i));
    ylim([0 1E-2])
    i
    pause(0.05)
end
%% Fitting all
close all
ps_cal = zeros(size(ps))

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


%% Plotting all measurements
for i = 1:N
    figure(2);
    clf;
    hold on;
    plot(freq(:,i), ps_cal(:,i));
    ylim([-2E-3 3E-3])
    pause(0.05)
end

%% Fitting
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


N = 20;

map = zeros(N, N);

for i = 1:N
    for j = 1:N

        if mod(i, 2) == 0 
            k = i*N - j + 1;
        else
            k = (i-1)*N + j;
        end

        %data = readtable("data/data-" + (k-1) + ".dat");
    
        %ps = table2array(data(:, 1));
        %freq = table2array(data(:, 2));

        map(i, j) = max(ps_cal(:,k));
        %k
        k = k + 1;
        %pause(0.5)
    end
end

figure(1);
clf;
%hold on;
%plot(freq, ps);
imagesc(map);
colormap("gray");