clear
close all

root = char(java.lang.System.getProperty('user.name'));

relative_path_fig = '..\..\Paper\Figures\';

if strcmp(root,'ffalcon') == 1
    pathData = 'C:\Users\ffalcon\Dropbox\small-biz-2020\data\us\raw\survey_responses';
    pathCode = 'C:\Users\ffalcon\Documents\GitHub\covid19-small-biz\';
else 
    pathCode='C:\Users\cneilson\Documents\GitHub\small-biz-2020\';
    pathData='C:\Dropbox\morestuff..';
end


%% Parameters
date='09_10_2019';  % Last run of data prep files. 
% Basic parameters used for generating graphs with same color scheme and dimensions. 

% Colors
princeton = [1.00,0.56,0.00];                            
harvard   = [0.68,0.00,0.00];
uchile    = [0.13,0.13,0.44];
gray      = [0.75,0.75,0.75];

CC = parula(10);

MarkerS=5; 
LineW=2;
scrsz = get(0,'ScreenSize');
pos=[1 0.85*scrsz(4)/2 1.2*scrsz(3)/2 scrsz(4)/2.5];
set(0,'DefaultFigurePosition',pos)
posBig=[2000 0.1*scrsz(4) 0.9*scrsz(3)/2 scrsz(4)/1.2];

Color3=[0.6350, 0.0780, 0.1840];
Color1 = CC(6,:);
Color2 = CC(4,:);

%% Start with figures:
Data = readtable([pathData '2020-biz-survey-us_March 30, 2020_10.24 - Copy.csv'],'TreatAsEmpty',{'.','NA'});
Data.totWorkers = Data.Q2_1_1 +  Data.Q2_1_2;
Data = Data(~(Data.totWorkers == 0 | Data.totWorkers > 300 | isnan(Data.totWorkers)) ,:) ; %Keep people with more than zero workers and eliminate NANs

% Number of Wokers
nFullTimeWorkers = Data.Q2_1_1;
nPartTimeWorkers = Data.Q2_1_2;
nWorkers = nFullTimeWorkers + nPartTimeWorkers ;
qtiles = prctile(nWorkers,[25 50 75]);
firmSize = NaN(size(Data,1),1);
firmSize(nWorkers < qtiles(1)) = 1; %[One Worker]
firmSize(nWorkers>= qtiles(1) & nWorkers <qtiles(2)) = 2; %2 workers
firmSize(nWorkers>= qtiles(2) & nWorkers <qtiles(3)) = 3; %[3 6] workers
firmSize(nWorkers>= qtiles(3)) = 4; %[more than 7 workers]
tabulate(firmSize)

%Probability bankruptcy
probBankruptcy = Data.Q6_1_2;


% Number of Wokers Laid Off
ynLayOff = ones(size(Data,1),1);
ynLayOff(strcmp(Data.Q3_1,'No'),1) = 0; 

ynLayOffFuture = ones(size(Data,1),1);
ynLayOffFuture(strcmp(Data.Q4_1,'No'),1) = 0; 

noLayOffFirms = (ynLayOff == 0) & (ynLayOffFuture == 0);

% Number of workers laid off:
nLayOffFullTime = Data.Q3_2_1;
nLayOffFullTime(isnan(nLayOffFullTime)) = 0;
nLayOffPartTime = Data.Q3_2_2;
nLayOffPartTime(isnan(nLayOffPartTime)) = 0;
nWorkersLaidOff = nLayOffFullTime + nLayOffPartTime;

% Number of workers to be laid of in the next 60 days
nLayOffFullTimeFuture = Data.Q4_2_1;
nLayOffFullTimeFuture(isnan(nLayOffFullTimeFuture)) = 0;
nLayOffPartTimeFuture = Data.Q4_2_2;
nLayOffPartTimeFuture(isnan(nLayOffPartTimeFuture)) = 0;
nWorkersLaidOffFuture = nLayOffFullTimeFuture + nLayOffPartTimeFuture;


% Number of Workers Now:
nWorkersNow = nWorkers - nWorkersLaidOff;

% Figure 1: Number of workers histogram
histogram(nWorkers(nWorkers < 50), 20, 'FaceColor', CC(3,:), 'EdgeColor', CC(3,:))
ylim([0 160])
xlim([0 50])
box on
grid on
ylabel('Number of Firms')
xlabel('Number of Workers')
set(gcf, 'Units', 'Inches', 'Position', [0, 0, 9, 6], 'PaperUnits', 'Inches', 'PaperSize', [7.25, 9.125])

% Figure 2: Number of workers laid off 
histogram(nWorkersLaidOff(nWorkersLaidOff < 50), 20, 'FaceColor', CC(3,:), 'EdgeColor', CC(3,:))
%ylim([0 160])
xlim([0 50])
box on
grid on
ylabel('Number of Firms')
xlabel('Number of Workers Laid Off')
set(gcf, 'Units', 'Inches', 'Position', [0, 0, 9, 6], 'PaperUnits', 'Inches', 'PaperSize', [7.25, 9.125])


% Figure 3: Number of people employed and unemployed by firm size:
dataByFirmSize = array2table([firmSize, nWorkers, nWorkersNow, nWorkersLaidOff, nWorkersLaidOffFuture, probBankruptcy, noLayOffFirms]);
dataByFirmSize.Properties.VariableNames = {'firmSize' 'nWorkers' 'nWorkersNow' 'nWorkersLaidOff' 'nWorkersLaidOffFuture' 'probBankruptcy' 'noLayOffFirms'};
dataByFirmSize = grpstats(dataByFirmSize,{'firmSize'}, ...
                {'sum','mean'}, ... 
                'DataVars',{'nWorkers' 'nWorkersNow' 'nWorkersLaidOff' 'nWorkersLaidOffFuture' 'probBankruptcy' 'noLayOffFirms'});


% Figure 4: Number of workers and unemployed by firm size
H = bar([dataByFirmSize.sum_nWorkers dataByFirmSize.sum_nWorkersLaidOff dataByFirmSize.sum_nWorkersLaidOffFuture]);
H(1).FaceColor  = CC(4,:);
H(2).FaceColor  = CC(2,:);
H(3).FaceColor  = CC(7,:);
H(1).EdgeColor  = CC(4,:);
H(2).EdgeColor  = CC(2,:);
H(3).EdgeColor  = CC(7,:);
%bar(dataByFirmSize.sum_nWorkersLaidOff, 'FaceColor', CC(2,:), 'EdgeColor', CC(2,:))
hold on 
grid on
ylim([0 1400])
set(gcf, 'Units', 'Inches', 'Position', [0, 0, 9, 6], 'PaperUnits', 'Inches', 'PaperSize', [7.25, 9.125])
xticklabels({'One Worker','Two Workers','[3 7[','>=7'})
ax = legend({'Number Workers','Number Laid Off','Number Laid Off Future'},'Location','northwest')
ylabel('Number of Workers')


% Figure 5: Probability to file for bankruptcy by firm size
H = bar(dataByFirmSize.mean_probBankruptcy);
H(1).FaceColor  = CC(4,:);
H(1).EdgeColor  = CC(4,:);
%bar(dataByFirmSize.sum_nWorkersLaidOff, 'FaceColor', CC(2,:), 'EdgeColor', CC(2,:))
hold on 
grid on
ylim([0 45])
set(gcf, 'Units', 'Inches', 'Position', [0, 0, 9, 6], 'PaperUnits', 'Inches', 'PaperSize', [7.25, 9.125])
xticklabels({'One Worker','Two Workers','[3 7[','>=7'})
ylabel('Probability of Bankruptcy')


% Figure 6: Probability to file for bankruptcy

fit1 = nWorkers\nWorkersLaidOff;
fit2 = nWorkers(nWorkersLaidOff>0)\nWorkersLaidOff(nWorkersLaidOff>0);
fit3 = nWorkers(nWorkersLaidOff>2)\nWorkersLaidOff(nWorkersLaidOff>2);
fit4 = nWorkers(nWorkersLaidOff>4)\nWorkersLaidOff(nWorkersLaidOff>4);

scatter(nWorkers, nWorkersLaidOff, probBankruptcy, 'MarkerFaceColor', CC(5,:), 'MarkerEdgeColor', CC(5,:))
hold on
plot(nWorkers,fit1*nWorkers, 'LineWidth',1.4)
hold on
plot(nWorkers(nWorkersLaidOff>0), fit2*nWorkers(nWorkersLaidOff>0), 'LineWidth',1.4)
hold on
plot(nWorkers(nWorkersLaidOff>2), fit3*nWorkers(nWorkersLaidOff>2), 'LineWidth',1.4)
hold on
plot(nWorkers(nWorkersLaidOff>4), fit4*nWorkers(nWorkersLaidOff>4), 'LineWidth',1.4)
grid on
box on
ax = legend({'Firms','Fit All: ' + string(round(fit1,2)), ...
    'Fit for (Unemp > 0): ' + string(round(fit2,2)),...
    'Fit for (Unemp > 1): ' + string(round(fit3,2)),...
    'Fit for (Unemp > 4): ' + string(round(fit4,2))},'Location','northwest')
set(gcf, 'Units', 'Inches', 'Position', [0, 0, 9, 6], 'PaperUnits', 'Inches', 'PaperSize', [7.25, 9.125])
xlabel('Number of Workers')
ylabel('Number of Workers Laid Off')



% Figure 7: Workers 
fit1 = nWorkersNow(nWorkersLaidOff == 0)\nWorkersLaidOffFuture(nWorkersLaidOff == 0);
fit2 = nWorkersNow(nWorkersLaidOff > 0)\nWorkersLaidOffFuture(nWorkersLaidOff > 0);

scatter(nWorkersNow(nWorkersLaidOff == 0), nWorkersLaidOffFuture(nWorkersLaidOff == 0), 'MarkerFaceColor', CC(2,:), 'MarkerEdgeColor', CC(2,:))
hold on 
plot(nWorkersNow(nWorkersLaidOff == 0),fit1*nWorkersNow(nWorkersLaidOff == 0), 'LineWidth',1.4, 'Color', CC(2,:))
hold on
scatter(nWorkersNow(nWorkersLaidOff > 0), nWorkersLaidOffFuture(nWorkersLaidOff > 0), 'MarkerFaceColor', CC(7,:), 'MarkerEdgeColor', CC(7,:))
hold on
plot(nWorkersNow(nWorkersLaidOff > 0),fit2*nWorkersNow(nWorkersLaidOff > 0), 'LineWidth',1.4, 'Color', CC(7,:))
legend({'Did no fire', 'Did no fire Fit','Fired','Fired Fit'},'Location','northwest')
set(gcf, 'Units', 'Inches', 'Position', [0, 0, 9, 6], 'PaperUnits', 'Inches', 'PaperSize', [7.25, 9.125])
xlabel('Number of Workers')
ylabel('Number of Workers Laid Off')
box on
grid on
ylim([0 45])
xlim([0 45])


% 

probBankruptcy(probBankruptcy==0) = .01;

scatter(nWorkers, nWorkersLaidOff, ones(size(nWorkersLaidOff,1),1)*20, probBankruptcy/100, 'filled')
colormap fdc


histogram(probBankruptcy)



scatter(nWorkers, (nWorkersLaidOff./nWorkers),probBankruptcy/5, 'filled')


x=randn(100,1);y=randn(100,1);  % sample data
scatter(x,y,20*abs(y),'filled')
colormap(hsv)




[~,bin]=histc(y,linspace(min(y),max(y),10));  % location of nth bin 
scatter(x,y,20*abs(y),bin,'filled')

%%


x1=nWorkers;
y1=nWorkersLaidOff;
y2=probBankruptcy;

XBin=3*round(x1/3);
Xbin=unique(XBin);
Ybin1=NaN(size(Xbin));
for i=1:length(Xbin)
    pickx=Xbin(i);
    r=find(XBin==pickx);
    Ybin1(i,1)=nanmean(y1(r));
    Ybin2(i,1)=nanmean(y2(r));
end

xx1=[XBin y1 y2];

xx1(sum(isnan(xx1),2)>0,:)=[];

xx = {};
xx{1} = xx1;


%1. Compute Exit Exam Correlations:

for ii = 1
    
    % 1: PCD ; 2: PCP ; 3: PCE ; 4: TICS
    xGrid=Xbin;
    scatter(xGrid,Ybin1(:,ii),Ybin2(:,ii),'filled')
    q = polyfit((xx{ii}(:,1)),xx{ii}(:,2),1);
    h = refcurve(q);
    h.Color = Color2;
    h.LineWidth = LineW;
    xlabel('Average College Entrance Exam Score')
    grid on
    box on
    set(gcf, 'Units', 'Inches', 'Position', [0, 0, 7, 6], 'PaperUnits', 'Inches', 'PaperSize', [7.25, 9.125])
    
end






