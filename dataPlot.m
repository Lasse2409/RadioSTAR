%% plot data
clear;

figure(1);
clf;
hold on;

for i = 0:399
    data = readtable("data/data-" + i + ".dat");
    
    ps = table2array(data(:, 1));
    freq = table2array(data(:, 2));
    
    %figure(1);
    %clf;
    %hold on;
    plot(freq, ps);
end

%% plot map
clear;

N = 20;

map = zeros(N, N);

for i = 1:N
    for j = 1:N

        if mod(i, 2) == 0 
            k = i*N - j + 1;
        else
            k = (i-1)*N + j;
        end

        data = readtable("data/data-" + (k-1) + ".dat");
    
        ps = table2array(data(:, 1));
        %freq = table2array(data(:, 2));

        map(i, j) = max(ps);

        k = k + 1;
    end
end

figure(1);
clf;
%hold on;
%plot(freq, ps);
imagesc(map);
colormap("gray");