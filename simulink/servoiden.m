sin2_dat = readtable("sina20w2.csv");
sin2_dat = table2array(sin2_dat);
T = sin2_dat(:,2)* .001;
U = sin2_dat(:,3);
Y = sin2_dat(:,4);
sin2_dat = iddata(U, Y, 10 * .001);

sin4_dat = readtable("sina20w2.csv");
sin4_dat = table2array(sin4_dat);
T = sin4_dat(:,2)* .001;
U = sin4_dat(:,3);
Y = sin4_dat(:,4);
sin4_dat = iddata(U, Y, 10* .001);

sin8_dat = readtable("sina20w2.csv");
sin8_dat = table2array(sin8_dat);
T = sin8_dat(:,2)* .001;
U = sin8_dat(:,3);
Y = sin8_dat(:,4);
sin8_dat = iddata(U, Y, 10* .001);

sin16_dat = readtable("sina20w2.csv");
sin16_dat = table2array(sin16_dat);
T = sin16_dat(:,2)* .001;
U = sin16_dat(:,3);
Y = sin16_dat(:,4);
sin16_dat = iddata(U, Y, 10* .001);

allsins = merge(sin2_dat, sin4_dat, sin8_dat, sin16_dat);

tfest(allsins, 2, 0)



models = [];
legends = [];
MSEs = zeros(5, 5);
STDs  = zeros(5, 5);

for npoles = 1:4
    for nzeros = 0:npoles
        model = tfest(allsins, npoles, nzeros );
        models = [models; model];
        lstr = strcat("Poles: ", string(npoles), " Zeros: ", string(nzeros));
        legends = [legends; lstr];
        normalizedMSE = model.report.Fit.FPE; %/ (y_all.' * y_all/ length (y_all));
        maxStdDev = max(sqrt(diag( model.report.parameters.FreeParCovariance)));
        MSEs(npoles, nzeros+1) = normalizedMSE;
        STDs(npoles, nzeros+1) = maxStdDev;
    end
end

figure
rlocus(models(3), models(4), models(5), models(6), models(7), models(8), models(9))
legend(legends(3:9))

%Choosing 3p2z NVM response is nonsense
%Choosing 2p1z, again nonsense response to sin wave.. what is happening?
%it eventually does something reasonable, but the rise time is way too
%high!
models(3)
models(4)
models(5)
models(6)
models(7)
models(8)
models(9)

figure
heatmap(0:4,1:5,log(MSEs))
xlabel("Zeros")
ylabel("Poles")
title("Log Normalized MSE for various Poles, Zeros counts")
colorbar;

figure
heatmap(0:4,1:5,log(STDs))
xlabel("Zeros")
ylabel("Poles")
title("Log Max STDEV for various Poles, Zeros counts")
colorbar;

