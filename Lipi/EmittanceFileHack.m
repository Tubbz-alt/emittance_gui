%{
f = '/u1/lcls/matlab/data/2018/2018-12/2018-12-18/Emittance-scan-OTRS_IN20_571-2018-12-18-165216.mat';
f = '~/nneveu/test_astra10pC.mat';
load(f);


[twiss, twissstd, parP, parPStd] = 
emittance_process(val, rMat, data, dataStd, plane, cal, energy, twiss0, charge, varargin);

for k = 1:5
    data.beam(k,method).stats(3) = data.beam(k,method).stats(3)/2;
end
%}
%%

%f = '/u1/lcls/matlab/data/2019/2019-06/2019-06-25/Emittance-scan-YAGS_GUNB_753-2019-06-25-155331.mat'; 
%f = '/u1/lcls/matlab/data/2019/2019-07/2019-07-01/Emittance-scan-YAGS_GUNB_753-2019-07-01-140311.mat'; 
%f = '/u1/lcls/matlab/data/2019/2019-07/2019-07-02/Emittance-scan-YAGS_GUNB_753-2019-07-02-153032.mat'; 
%f = load('~/nneveu/fakeScanData.mat');
%f = load('~/nneveu/emittance_gui/Emittance-scan-1fC-760keV-9points.mat')
%load(f);

%leff     = 0.1342;

%sigma    =  [0.89319, 0.73666, 0.58642, 0.44727, 0.32949, 0.25769, 0.2679,  0.35855, 0.50235, 0.68483, 0.89274, 1.1161, 1.3454 ]*10^3;
%soltesla =  [0.054, 0.0545, 0.055, 0.0555, 0.056, 0.0565, 0.057, 0.0575, 0.058, 0.0585, 0.059, 0.0595, 0.06];
% astra emittance at sol  [1.5059 1.5199 1.534  1.5481 1.5623 1.5766 1.5909 1.6052 1.6197 1.6341 1.6487 1.6633 1.6779]
% Values in kG-m solvals = 0.0725    0.0731    0.0738    0.0745    0.0752    0.0758    0.0765 0.0772    0.0778    0.0785    0.0792    0.0798    0.0805

% Charge 20pC
%sigma   = [1.3537,  1.1928,  1.0365,  0.88698, 0.74708, 0.62154, 0.51869, 0.45195, 0.43787, 0.48424, 0.58389, 0.72757, 0.9066 ]*10^3
%soltesla =  [0.054, 0.0545, 0.055, 0.0555, 0.056, 0.0565, 0.057, 0.0575, 0.058, 0.0585, 0.059, 0.0595, 0.06]
% astra emittance at sol [1.71   1.722  1.7401 1.7552 1.7704 1.7857 1.801  1.8164 1.8319 1.8474 1.863  1.8787 1.8944]

% Charge 100pC
%sigma   = [3.5308 3.3004 3.0726 2.8483 2.6282 2.4132 2.2049 2.0047 1.8146 1.6373 1.4765 1.3372 1.2257]*10^3; 
%soltesla =  [0.054, 0.0545, 0.055, 0.0555, 0.056, 0.0565, 0.057, 0.0575, 0.058, 0.0585, 0.059, 0.0595, 0.06]
% astra emittance at sol [3.5622 3.5874 3.6128 3.6336 3.664  3.6897 3.7156 3.7415 3.7677 3.7939 3.8203 3.8467 3.8733]

% Charge 250pC
%sigma   = [5.6783 5.3245 4.9728 4.6245 4.2799 3.9402 3.6069 3.2814 2.9661 2.6632 2.3763 2.1098 1.8698]*10^3; 
%solvals =  [0.054, 0.0545, 0.055, 0.0555, 0.056, 0.0565, 0.057, 0.0575, 0.058, 0.0585, 0.059, 0.0595, 0.06]
% astra emittance at sol [7.4703 7.5273 7.5841 7.6415 7.6976 7.7562 7.814  7.8716 7.9298 7.9879 8.0458 8.1045 8.1629]

% Charge 1fC
%leff     = 0.1342;
%sigma    = [0.28052, 0.23548, 0.19618, 0.1671, 0.15452, 0.1627,  0.18925, 0.2281,  0.27428]*10^3;
%soltesla = [0.054,   0.0545,  0.055,   0.0555, 0.056,   0.0565, 0.057,     0.0575, 0.058];
%Values in kG-m
%solkg-m = [ 0.0725    0.0738    0.0752    0.0765    0.0778 ]

%Dummy setting #3 astra
%sol3 = [0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59];
%sig3 = [0.3792, 0.2807, 0.1961, 0.1545, 0.1893, 0.2741, 0.3782]*10^3;
%len3 = length(sol3);

% Dec. 13, 2019
%f = load('/u1/lcls/matlab/data/2019/2019-12/2019-12-11/Emittance-scan-YAGS_GUNB_753-2019-12-11-161626.mat');
f = load('/u1/lcls/matlab/data/2019/2019-12/2019-12-13/Emittance-scan-YAGS_GUNB_753-2019-12-13-095550.mat');
leff     = 0.086;
sigma = [0.434, 0.3327, 0.2390, 0.1692, 0.1617, 0.2248, 0.3207, 0.4289]*1e3; % um
soltesla = linspace(0.0525,0.0595,8);


solgm    = soltesla*10^4*leff;
solvals   = solgm*10^-3 % kg-m
lenpC = length(solvals);

for k = 1:lenpC
    disp(k)
    %Replace dummy sigma with Feng's (above)
    %Model assumed is #6: RMS cut Area
    %Model assumed is #1: Gaussian
    disp(f.data.beam(k,1).stats(3))
    f.data.beam(k,1).stats(3) = sigma(k);
    f.data.beamStd(k,1).stats(3) = 1e-9; 
end

%%


rMat=cat(3,f.data.rMatrix{1:numel(f.data.rMatrix)});
%rMat=reshape(repmat(rMat,1,size(data.beamList,3)),6,6,[]);
% Recompute twiss from a struct "data"

Q = {f.data.charge*1e-3,0}; %nC
opts.doPlot = 1;
opts.normPS = 0;
opts.xlab = f.data.quadName;
% Methods
% 1 = Gauss
% 2 = Asym
% 3 = Super
% 4 = RMS raw
% 5 = RMS cut peak
% 6 = RMS cut area
% 7 = RMS floor (?!)
method = 1;

[twiss, twissstd, parP, parPStd] = ...
    emittance_process(f.data.quadVal,rMat,...
    f.data.beam(:,method),f.data.beamStd(:,method),1,1e-6,f.data.energy,f.data.twiss0,Q,opts)
