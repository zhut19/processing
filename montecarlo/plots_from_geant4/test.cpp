#define test_cxx
#include "test.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TRandom3.h>

void test::Loop()
{
char cSource[7][10] = {"U238","Ra226","Th232","Th228","Co60","K40","Cs137"};
  cout << " Gammas from " << cSource[FlagIsotope] << " decay " << endl;

  TH1D * hcounts = new TH1D("hcounts","hcounts",3000,0,3000);
  TH1D * hEd_1t = new TH1D("hEd_1t","Electromagnetic recoil energy in 1 ton FV",3000 ,0. ,3000.);
  TH1D * hEd_400kg = new TH1D("hEd_400kg","Electromagnetic recoil energy in 400 kg FV",3000 ,0. ,3000.);
  TH1D * hEd_slice1 = new TH1D("hEd_slice1","Electromagnetic recoil energy in slice 1",3000 ,0. ,3000.);
  TH1D * hEd_slice2 = new TH1D("hEd_slice2","Electromagnetic recoil energy in slice 2",3000 ,0. ,3000.);
  TH1D * hEd_slice3 = new TH1D("hEd_slice3","Electromagnetic recoil energy in slice 3",3000 ,0. ,3000.);
  TH1D * hEd_slice4 = new TH1D("hEd_slice4","Electromagnetic recoil energy in slice 4",3000 ,0. ,3000.);
  TH1D * hEd_slice5 = new TH1D("hEd_slice5","Electromagnetic recoil energy in slice 5",3000 ,0. ,3000.);
  TH1D * hEd_slice6 = new TH1D("hEd_slice6","Electromagnetic recoil energy in slice 6",3000 ,0. ,3000.);
  TH1D * hEd_slice7 = new TH1D("hEd_slice7","Electromagnetic recoil energy in slice 7",3000 ,0. ,3000.);
  TH1D * hEd_slice8 = new TH1D("hEd_slice8","Electromagnetic recoil energy in slice 8",3000 ,0. ,3000.);
  TH1D * hEd_slice9 = new TH1D("hEd_slice9","Electromagnetic recoil energy in slice 9",3000 ,0. ,3000.);
  TH1D * hEd_slice10 = new TH1D("hEd_slice10","Electromagnetic recoil energy in slice 10",3000 ,0. ,3000.);
  
  TH1D * hEd_slice1_a = new TH1D("hEd_slice1_a","Electromagnetic recoil energy in slice 1 a",3000 ,0. ,3000.);
  TH1D * hEd_slice1_b = new TH1D("hEd_slice1_b","Electromagnetic recoil energy in slice 1 b",3000 ,0. ,3000.);
  TH1D * hEd_slice1_c = new TH1D("hEd_slice1_c","Electromagnetic recoil energy in slice 1 c",3000 ,0. ,3000.);
  TH1D * hEd_slice1_d = new TH1D("hEd_slice1_d","Electromagnetic recoil energy in slice 1 d",3000 ,0. ,3000.);
  TH1D * hEd_slice1_e = new TH1D("hEd_slice1_e","Electromagnetic recoil energy in slice 1 e",3000 ,0. ,3000.);
  
  TH1D * hEd_slice10_a = new TH1D("hEd_slice10_a","Electromagnetic recoil energy in slice 10 a",3000 ,0. ,3000.);
  TH1D * hEd_slice10_b = new TH1D("hEd_slice10_b","Electromagnetic recoil energy in slice 10 b",3000 ,0. ,3000.);
  TH1D * hEd_slice10_c = new TH1D("hEd_slice10_c","Electromagnetic recoil energy in slice 10 c",3000 ,0. ,3000.);
  TH1D * hEd_slice10_d = new TH1D("hEd_slice10_d","Electromagnetic recoil energy in slice 10 d",3000 ,0. ,3000.);
  TH1D * hEd_slice10_e = new TH1D("hEd_slice10_e","Electromagnetic recoil energy in slice 10 e",3000 ,0. ,3000.);

  // 2d histo: position of the scatter
  Int_t nbinZ=100, nbinR2=235, nZbinsSubSlices = 120;
  Double_t Zmin=-1100., Zmax=100.; //mm
  Double_t R2min=0., R2max=235225.; //mm
  
  TH2D * h2d = new TH2D("h2d","Position of ER single scatter interactions, energy range [1,200] keV",nbinR2, R2min, R2max, nbinZ, Zmin, Zmax);
  Double_t BinVolume = 3.14159 * 0.01*(R2max-R2min)/nbinR2 * 0.1*(Zmax-Zmin)/nbinZ; //cm3
  Double_t BinMass = BinVolume * 2.827 * 1.e-3;// in kg
  Double_t Emin = 1.; 
  Double_t Emax = 200.; 
  Double_t EnergyRange = Emax-Emin;
  
  // 2d plot in a smaller energy range (ROI ... valid also for outer fiducial volumes)
  TH2D * h2dROI = new TH2D("h2dROI","Position of ER single scatter interactions, energy range [1,100] keV",nbinR2, R2min, R2max, nbinZ, Zmin, Zmax);  
  TH2D * h2dROI_2 = new TH2D("h2dROI_2","Position of ER single scatter interactions, energy range [2,12] keV",nbinR2, R2min, R2max, nbinZ, Zmin, Zmax);
  TH2D * h2dROI_2_1t = new TH2D("h2dROI_2_1t","Position of ER single scatter interactions, energy range [2,12] keV",nbinR2, R2min, R2max, nbinZ, Zmin, Zmax);
  TH2D * h2dROI_2_400kg = new TH2D("h2dROI_2_400kg","Position of ER single scatter interactions, energy range [2,12] keV",nbinR2, R2min, R2max, nbinZ, Zmin, Zmax);
  
  TH2D * h2d_slice1 = new TH2D("h2d_slice1","Position of ER single scatter interactions, slice 1",nbinR2, R2min, R2max, nbinZ, Zmin, Zmax);
  TH2D * h2d_slice2 = new TH2D("h2d_slice2","Position of ER single scatter interactions, slice 2",nbinR2, R2min, R2max, nbinZ, Zmin, Zmax);
  TH2D * h2d_slice3 = new TH2D("h2d_slice3","Position of ER single scatter interactions, slice 3",nbinR2, R2min, R2max, nbinZ, Zmin, Zmax);
  TH2D * h2d_slice4 = new TH2D("h2d_slice4","Position of ER single scatter interactions, slice 4",nbinR2, R2min, R2max, nbinZ, Zmin, Zmax);
  TH2D * h2d_slice5 = new TH2D("h2d_slice5","Position of ER single scatter interactions, slice 5",nbinR2, R2min, R2max, nbinZ, Zmin, Zmax);
  TH2D * h2d_slice6 = new TH2D("h2d_slice6","Position of ER single scatter interactions, slice 6",nbinR2, R2min, R2max, nbinZ, Zmin, Zmax);
  TH2D * h2d_slice7 = new TH2D("h2d_slice7","Position of ER single scatter interactions, slice 7",nbinR2, R2min, R2max, nbinZ, Zmin, Zmax);
  TH2D * h2d_slice8 = new TH2D("h2d_slice8","Position of ER single scatter interactions, slice 8",nbinR2, R2min, R2max, nbinZ, Zmin, Zmax);
  TH2D * h2d_slice9 = new TH2D("h2d_slice9","Position of ER single scatter interactions, slice 9",nbinR2, R2min, R2max, nbinZ, Zmin, Zmax);
  TH2D * h2d_slice10 = new TH2D("h2d_slice10","Position of ER single scatter interactions, slice 10",nbinR2, R2min, R2max, nbinZ, Zmin, Zmax);
  
  TH2D * h2d_slice1_a = new TH2D("h2d_slice1_a","Position of ER single scatter interactions, slice 1 a",nbinR2, R2min, R2max, nZbinsSubSlices, Zmin, Zmax);
  TH2D * h2d_slice1_b = new TH2D("h2d_slice1_b","Position of ER single scatter interactions, slice 1 b",nbinR2, R2min, R2max, nZbinsSubSlices, Zmin, Zmax);
  TH2D * h2d_slice1_c = new TH2D("h2d_slice1_c","Position of ER single scatter interactions, slice 1 c",nbinR2, R2min, R2max, nZbinsSubSlices, Zmin, Zmax);
  TH2D * h2d_slice1_d = new TH2D("h2d_slice1_d","Position of ER single scatter interactions, slice 1 d",nbinR2, R2min, R2max, nZbinsSubSlices, Zmin, Zmax);
  TH2D * h2d_slice1_e = new TH2D("h2d_slice1_e","Position of ER single scatter interactions, slice 1 e",nbinR2, R2min, R2max, nZbinsSubSlices, Zmin, Zmax);
  
  TH2D * h2d_slice10_a = new TH2D("h2d_slice10_a","Position of ER single scatter interactions, slice 10 a",nbinR2, R2min, R2max, nZbinsSubSlices, Zmin, Zmax);
  TH2D * h2d_slice10_b = new TH2D("h2d_slice10_b","Position of ER single scatter interactions, slice 10 b",nbinR2, R2min, R2max, nZbinsSubSlices, Zmin, Zmax);
  TH2D * h2d_slice10_c = new TH2D("h2d_slice10_c","Position of ER single scatter interactions, slice 10 c",nbinR2, R2min, R2max, nZbinsSubSlices, Zmin, Zmax);
  TH2D * h2d_slice10_d = new TH2D("h2d_slice10_d","Position of ER single scatter interactions, slice 10 d",nbinR2, R2min, R2max, nZbinsSubSlices, Zmin, Zmax);
  TH2D * h2d_slice10_e = new TH2D("h2d_slice10_e","Position of ER single scatter interactions, slice 10 e",nbinR2, R2min, R2max, nZbinsSubSlices, Zmin, Zmax);

  Double_t EminROI = 1.; 
  Double_t EmaxROI = 100.; 
  Double_t EnergyRangeROI = EmaxROI-EminROI;
  Double_t EminROI_2 = 1.;
  Double_t EmaxROI_2 = 12.;
  Double_t EnergyRangeROI_2 = EmaxROI_2-EminROI_2;

  // show plot in dru
  Float_t LiveTimePlot = GeneratedEvents / GammaYield[FlagIsotope] / (ScreenedActivity[FlagIsotope]*1.e-3) / Mass;
  
  Double_t sliceMass    = 88.;
  Double_t subSliceMass = 17.6;
  Double_t FV400kgMass  = 400.;
  Double_t FV1tmass     = 1000.;
  
  Double_t ScaleFactorEr_1tFV       = 1./(LiveTimePlot/86400.)/FV1tmass; 
  Double_t ScaleFactorEr_400kgFV    = 1./(LiveTimePlot/86400.)/FV400kgMass;
  Double_t ScaleFactorEr_sliceFV    = 1./(LiveTimePlot/86400.)/sliceMass;
  Double_t ScaleFactorEr_subSliceFV = 1./(LiveTimePlot/86400.)/subSliceMass;
  
  Double_t ScaleFactor2d = 1./BinMass * 1./(LiveTimePlot/86400.) * 1./EnergyRange;
  Double_t ScaleFactor2dROI = 1./BinMass * 1./(LiveTimePlot/86400.) * 1./EnergyRangeROI;
  Double_t ScaleFactor2dROI_2 = 1./BinMass * 1./(LiveTimePlot/86400.) * 1./EnergyRangeROI_2;

  // 2d histo: origin of the Gamma
  TH2D * h2dPri = new TH2D("h2dPri","Position of the origin of the Gamma: 1tonFV, [1, 200] keV",200,0.,2000,200,-1500.,1500.);
  TH2D * h2dPri_2 = new TH2D("h2dPri_2","Position of the origin of the Gamma: 1tonFV, [2, 12] keV",200,0.,2000,200,-1500.,1500.);
  TH2D * h2dPri_noCondition = new TH2D("h2d_noCond","Position of the confined isotopes",200,0.,2000,3000,-1500,1500);
  
  TH1D * N_R = new TH1D("N_R in [1,200]","N_R in [1,200]",10,0.,10.);	
  TH1D * N_R_p = new TH1D("N_R_p in [1,200]","N_R_p in [1,200]",10,0.,10.);	
  TH1D * N_R_ROI_2 = new TH1D("N_R in [2,12]","N_R in [2,12]",10,0.,10.);	
  TH1D * N_G = new TH1D("N_G","N_G",10,0.,10.);	
  
  Double_t ScaleFactor2dPri = 1./(LiveTimePlot/(86400.*365.)); // in ev / y  
  
  Double_t TotBkgEvents = 0., TotBkgEventsNoW = 0., TotBkgEvents_ROI_2 = 0.;

  TRandom3 * r = new TRandom3();
  Double_t sigma=5.;
  Double_t rposNs;
  Double_t rS;
  Double_t rCut = 150000.;
  Double_t cutSubSliceStep = -967./50.;
  Double_t cutSliceStep = -967./10.;
  Double_t bottomSubSlicesOffset = cutSliceStep*9;
  Double_t fvZshift = 483.5;
  Double_t zPrime;
  Double_t r2pri;

  if (fChain == 0) return;
  
  Long64_t nentries = fChain->GetEntriesFast();
  
  Long64_t nbytes = 0, nb = 0;
  for (Long64_t jentry=0; jentry<nentries;jentry++) {

    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;

    nb = fChain->GetEntry(jentry);   nbytes += nb;

    // if (Cut(ientry) < 0) continue;
  
    // Gamma Production point
    Double_t r2pri = xpri*xpri+ypri*ypri;
    Double_t rpri = sqrt(r2pri);
    
    // Cut on the position of the primary particle
    // cuts for the v300 Cryostat
    Bool_t cFromInnerCryo = (sqrt(r2pri)<555. && ( zpri>0 && zpri<sqrt(pow(1200,2)-0.8*r2pri) || ( zpri<0 && zpri>-sqrt(pow(900,2)-0.9*r2pri)  ) ) );//(sqrt(r2pri)<555. && ( zpri>0 && zpri<sqrt(pow(1200,2)-0.8*r2pri) || ( zpri<0 && zpri>-sqrt(pow(940,2)-0.95*r2pri)  ) ) );
    Bool_t cFromInnerFlange = (sqrt(r2pri)>555. && sqrt(r2pri)<620. && zpri>650 && zpri<800);//(sqrt(r2pri)>555. && sqrt(r2pri)<640. && zpri>650 && zpri<780);
    Bool_t cFromOuterCryo = (sqrt(r2pri)<815) && !cFromInnerFlange && !cFromInnerCryo;
    Bool_t cFromOuterFlange = (sqrt(r2pri)>815); 
    Bool_t cFromFlanges = cFromInnerFlange || cFromOuterFlange;
    Bool_t cFromShells = cFromInnerCryo || cFromOuterCryo;
    
    //components in the TPC
    Bool_t cFromBottomFiller = zpri < -700.;
    Bool_t cFromTopPlate = zpri>720.5;
    //       Bool_t cFromMiddlePlate = (zpri>420 && zpri<470);
    //       Bool_t cFromElectrodeRings = !cFromBottomFiller && !cFromTopPlate && !cFromMiddlePlate;
    Bool_t cFromMiddlePlate    = zpri>-520 && zpri<500 && rpri<522.;//cathode & anode ring, ss_plate+ss_ring_lxe
    Bool_t cFromOtherPlate     = (zpri>530 && zpri<545 && rpri<523.) || (zpri>-580 && zpri<-560);//bottom & top ring
    Bool_t cFromLateralBell    = rpri>523.5;
    
    Bool_t cU238  = 0;
    Bool_t cTh232 = 0;
    
    //selection of the first/second part of U238 and Th232 decay chain
    if(FlagIsotope==0)
      {
	cU238  = (*type)[0]=="U238[0.0]" || (*type)[0]=="Th234[0.0]" || (*type)[0]=="Pa234[73.9]" || (*type)[0]=="U234[0.0]" || (*type)[0]=="Th230[0.0]";
	cTh232 = true;
      }
    if(FlagIsotope==1)
      {
	cU238  = !((*type)[0]=="U238[0.0]" || (*type)[0]=="Th234[0.0]" || (*type)[0]=="Pa234[73.9]" || (*type)[0]=="U234[0.0]" || (*type)[0]=="Th230[0.0]");
	  cTh232 = true;
      }
    if(FlagIsotope==2)
      {
	cU238  = true;
	cTh232 = (*type)[0]=="Th232[0.0]" || (*type)[0]=="Ra228[0.0]" || (*type)[0]=="Ac228[0.0]";
      }
    if(FlagIsotope==3)
	{
	  cU238  = true;
	  cTh232 = !((*type)[0]=="Th232[0.0]" || (*type)[0]=="Ra228[0.0]" || (*type)[0]=="Ac228[0.0]");
	}
    if(FlagIsotope==4)
      {
	cU238  = true;
	cTh232 = true;
      }
    if(FlagIsotope==5)
      {
	cU238  = true;
	cTh232 = true;
      }
    if(FlagIsotope==6)
      {
	cU238  = true;
	  cTh232 = true;
      }
    
    
    //___________________________________________________________________________________________________________
    
    switch(FlagSource)
      {
	case(1): // Cryostat Shells
	  if (!cFromShells) continue;
	  break;
      case(2): // Cryostat Flanges
	if (!cFromFlanges) continue;
	// 	case(10): // TPC SS 
	// 	  if (cFromBottomFiller) continue;
	break;
	/*	case(11): // Bottom Filler
		if (!cFromBottomFiller) continue;
		break;*/
      case(12): // Cathode & Anode ring, ss_plate+ss_ring_lxe
          if (!cFromMiddlePlate) continue;
          break;
      case(13): // lateral Bell
	if (!cFromLateralBell) continue;
	break;
      case(14): // Bottom & Top ring
	if (!cFromOtherPlate) continue;
	break;
      case(15): // Top Bell
	if (!cFromTopPlate) continue;
	break;
	
      }
    
    //      cout << "EventID  " << eventid << endl;
    
    // Selection Cuts
    Bool_t cFiducialVolume_400kg = 0;
    Bool_t cFiducialVolume_1t    = 0;
    
    Bool_t cFiducialVolume_slice1   = 0;
    Bool_t cFiducialVolume_slice2   = 0;
    Bool_t cFiducialVolume_slice3   = 0;
    Bool_t cFiducialVolume_slice4   = 0;
    Bool_t cFiducialVolume_slice5   = 0;
    Bool_t cFiducialVolume_slice6   = 0;
    Bool_t cFiducialVolume_slice7   = 0;
    Bool_t cFiducialVolume_slice8   = 0;
    Bool_t cFiducialVolume_slice9   = 0;
    Bool_t cFiducialVolume_slice10  = 0;
    
    Bool_t cFiducialVolume_slice1_a = 0;
    Bool_t cFiducialVolume_slice1_b = 0;
    Bool_t cFiducialVolume_slice1_c = 0;
    Bool_t cFiducialVolume_slice1_d = 0;
    Bool_t cFiducialVolume_slice1_e = 0;

    Bool_t cFiducialVolume_slice10_a = 0;
    Bool_t cFiducialVolume_slice10_b = 0;
    Bool_t cFiducialVolume_slice10_c = 0;
    Bool_t cFiducialVolume_slice10_d = 0;
    Bool_t cFiducialVolume_slice10_e = 0;

    Bool_t cSingleScatter    = 0;
    Bool_t cEnergyRange      = 0;
    Bool_t cEnergyRangeROI   = 0;
    Bool_t cEnergyRangeROI_2 = 0;
    
    // compute weight
    // Double_t w = gScalingFactor->Eval(epri/1000.);
    
    // Fiducial Volume cut
    Double_t r2pos = xpos*xpos+ypos*ypos;
    zpos = zpos+14.5; // redefine Z as for v300
    
    rposNs = sqrt(r2pos);
    rS = r->Gaus(rposNs, sigma);
    r2pos = rS*rS;

    if( (pow(TMath::Abs((zpos)/399.),3.0)+pow(TMath::Abs((r2pos)/160000.),3.0)) < 1 ) cFiducialVolume_1t = 1;
    //cout << zpos << "  " << r2pos << "  " << cFiducialVolume_1t << endl;
    
    zPrime = zpos - fvZshift;
        
    // FV = 400 kg                                                                      
    if( zPrime>-750. && zPrime<-330. && r2pos<rCut) cFiducialVolume_400kg = 1;
    
    // 10 cm Z slices                                                                   
    if( zPrime>=cutSliceStep    && zPrime<0.             && r2pos<rCut) cFiducialVolume_slice1 = 1;
    if( zPrime>=cutSliceStep*2  && zPrime<cutSliceStep   && r2pos<rCut) cFiducialVolume_slice2 = 1;
    if( zPrime>=cutSliceStep*3  && zPrime<cutSliceStep*2 && r2pos<rCut) cFiducialVolume_slice3 = 1;
    if( zPrime>=cutSliceStep*4  && zPrime<cutSliceStep*3 && r2pos<rCut) cFiducialVolume_slice4 = 1;
    if( zPrime>=cutSliceStep*5  && zPrime<cutSliceStep*4 && r2pos<rCut) cFiducialVolume_slice5 = 1;
    if( zPrime>=cutSliceStep*6  && zPrime<cutSliceStep*5 && r2pos<rCut) cFiducialVolume_slice6 = 1;
    if( zPrime>=cutSliceStep*7  && zPrime<cutSliceStep*6 && r2pos<rCut) cFiducialVolume_slice7 = 1;
    if( zPrime>=cutSliceStep*8  && zPrime<cutSliceStep*7 && r2pos<rCut) cFiducialVolume_slice8 = 1;
    if( zPrime>=cutSliceStep*9  && zPrime<cutSliceStep*8 && r2pos<rCut) cFiducialVolume_slice9 = 1;
    if( zPrime>=cutSliceStep*10 && zPrime<cutSliceStep*9 && r2pos<rCut) cFiducialVolume_slice10 = 1;
    
    // top subslices                                                                                                                                                                 
    if( zPrime>=cutSubSliceStep    && zPrime<0.                && r2pos<rCut) cFiducialVolume_slice1_a = 1;
    if( zPrime>=cutSubSliceStep*2  && zPrime<cutSubSliceStep   && r2pos<rCut) cFiducialVolume_slice1_b = 1;
    if( zPrime>=cutSubSliceStep*3  && zPrime<cutSubSliceStep*2 && r2pos<rCut) cFiducialVolume_slice1_c = 1;
    if( zPrime>=cutSubSliceStep*4  && zPrime<cutSubSliceStep*3 && r2pos<rCut) cFiducialVolume_slice1_d = 1;
    if( zPrime>=cutSubSliceStep*5  && zPrime<cutSubSliceStep*4 && r2pos<rCut) cFiducialVolume_slice1_e = 1;

    // bot subslices                                                                                                                                                                 
    if( zPrime>=cutSubSliceStep+bottomSubSlicesOffset    && zPrime<bottomSubSlicesOffset                   && r2pos<rCut) cFiducialVolume_slice10_a = 1;
    if( zPrime>=bottomSubSlicesOffset+cutSubSliceStep*2  && zPrime<bottomSubSlicesOffset+cutSubSliceStep   && r2pos<rCut) cFiducialVolume_slice10_b = 1;
    if( zPrime>=bottomSubSlicesOffset+cutSubSliceStep*3  && zPrime<bottomSubSlicesOffset+cutSubSliceStep*2 && r2pos<rCut) cFiducialVolume_slice10_c = 1;
    if( zPrime>=bottomSubSlicesOffset+cutSubSliceStep*4  && zPrime<bottomSubSlicesOffset+cutSubSliceStep*3 && r2pos<rCut) cFiducialVolume_slice10_d = 1;
    if( zPrime>=bottomSubSlicesOffset+cutSubSliceStep*5  && zPrime<bottomSubSlicesOffset+cutSubSliceStep*4 && r2pos<rCut) cFiducialVolume_slice10_e = 1;

    // Single inelastic Scatter cut 
    if( inel_hits==1 && er_ed>0 && er_ed<3000) 
      cSingleScatter = 1;
    else 
      cSingleScatter = 0;

    // Energy Range cut
    if( er_ed>=Emin && er_ed<=Emax ) cEnergyRange = 1;
    if( er_ed>=EminROI && er_ed<=EmaxROI ) cEnergyRangeROI = 1;
    if( er_ed>=EminROI_2 && er_ed<=EmaxROI_2 ) cEnergyRangeROI_2 = 1;
    
    //_______________________________ Fill Plots ______________________________________________
    
    // to nove the ground to z = 0
    zpos = zpos - fvZshift;
    
    if(cSingleScatter && cU238 && cTh232){
      
      if(cFiducialVolume_1t)
	hEd_1t->Fill(er_ed);
      
      if(cFiducialVolume_400kg){
	hEd_400kg->Fill(er_ed);
	if(cEnergyRangeROI_2) 
	  h2dROI_2_400kg->Fill(r2pos,zpos);
      }
      
      if(cFiducialVolume_slice1){
        hEd_slice1->Fill(er_ed);
        h2d_slice1->Fill(r2pos,zpos);
      }

      if(cFiducialVolume_slice2){
        hEd_slice2->Fill(er_ed);
        h2d_slice2->Fill(r2pos,zpos);
      }

      if(cFiducialVolume_slice3){
        hEd_slice3->Fill(er_ed);
        h2d_slice3->Fill(r2pos,zpos);
      }

      if(cFiducialVolume_slice4){
        hEd_slice4->Fill(er_ed);
        h2d_slice4->Fill(r2pos,zpos);
      }

      if(cFiducialVolume_slice5){
        hEd_slice5->Fill(er_ed);
        h2d_slice5->Fill(r2pos,zpos);
      }

      if(cFiducialVolume_slice6){
        hEd_slice6->Fill(er_ed);
        h2d_slice6->Fill(r2pos,zpos);
      }

      if(cFiducialVolume_slice7){
        hEd_slice7->Fill(er_ed);
        h2d_slice7->Fill(r2pos,zpos);
      }

      if(cFiducialVolume_slice8){
        hEd_slice8->Fill(er_ed);
        h2d_slice8->Fill(r2pos,zpos);
      }

      if(cFiducialVolume_slice9){
        hEd_slice9->Fill(er_ed);
        h2d_slice9->Fill(r2pos,zpos);
      }

      if(cFiducialVolume_slice10){
        hEd_slice10->Fill(er_ed);
        h2d_slice10->Fill(r2pos,zpos);
      }

      ////// top subslices /////                                                                                                                    
      if(cFiducialVolume_slice1_a){
        hEd_slice1_a->Fill(er_ed);
        h2d_slice1_a->Fill(r2pos,zpos);
      }if(cFiducialVolume_slice1_b){
        hEd_slice1_b->Fill(er_ed);
        h2d_slice1_b->Fill(r2pos,zpos);
      }if(cFiducialVolume_slice1_c){
        hEd_slice1_c->Fill(er_ed);
        h2d_slice1_c->Fill(r2pos,zpos);
      }if(cFiducialVolume_slice1_d){
        hEd_slice1_d->Fill(er_ed);
        h2d_slice1_d->Fill(r2pos,zpos);
      }if(cFiducialVolume_slice1_e){
        hEd_slice1_e->Fill(er_ed);
        h2d_slice1_e->Fill(r2pos,zpos);
      }

      ////// bot subslices /////                                                                                                                                             
      if(cFiducialVolume_slice10_a){
        hEd_slice10_a->Fill(er_ed);
        h2d_slice10_a->Fill(r2pos,zpos);
      }if(cFiducialVolume_slice10_b){
	hEd_slice10_b->Fill(er_ed);
	h2d_slice10_b->Fill(r2pos,zpos);
      }if(cFiducialVolume_slice10_c){
        hEd_slice10_c->Fill(er_ed);
        h2d_slice10_c->Fill(r2pos,zpos);
      }if(cFiducialVolume_slice10_d){
        hEd_slice10_d->Fill(er_ed);
        h2d_slice10_d->Fill(r2pos,zpos);
      }if(cFiducialVolume_slice10_e){
        hEd_slice10_e->Fill(er_ed);
        h2d_slice10_e->Fill(r2pos,zpos);
      }
      
      
    }
    
    if( cFiducialVolume_1t && cSingleScatter && cEnergyRange && cU238 && cTh232 )
      {
	hcounts->Fill(er_ed);
	TotBkgEvents += 1;
	h2dPri->Fill(rpri,zpri);
	if(cEnergyRangeROI_2){
	  h2dPri_2->Fill(rpri,zpri);
	  TotBkgEvents_ROI_2 += 1;
	}
      }
    
    if( cSingleScatter && cEnergyRange && cU238 && cTh232 )
      {
	h2d->Fill(r2pos,zpos);  	  
	if(cEnergyRangeROI) 	  h2dROI->Fill(r2pos,zpos);  	  
	if(cEnergyRangeROI_2)   h2dROI_2->Fill(r2pos,zpos);
      }
    
    
    
    
    //cout << zpri << endl;
    h2dPri_noCondition->Fill(rpri,zpri);//controllo sul volume di confinamento
    //TotBkgEvents=hcounts->Integral(1,200);
    
    //__________________________________________________________________________________________
    
  }
  
  //   hEpri->Draw();
  
   // CALCULATE Background events
  //cout << " Survived events before Weight " << TotBkgEventsNoW << endl;
  cout << "survived events in [1,200] " << TotBkgEvents << endl;
  //Mass = 2.3;
  if(TotBkgEvents==0)
    {//use upper limit
      cout << "USE 95% UPPER LIMIT 3." << endl;
      TotBkgEvents = 3.;
    }
  
  Double_t SurvivedEvents = TotBkgEvents *10. / 200.;// to scale it to the [2,12] keVee range
  SurvivedEvents = SurvivedEvents;//;/400.;//discriminazione al 99.75%
  cout << "Survived Events in [2,12] senza discriminazione   " << SurvivedEvents << endl;
  
  N_R->SetBinContent(5,SurvivedEvents);
  N_R_p->SetBinContent(5,TotBkgEvents);
  N_R_ROI_2->SetBinContent(5,TotBkgEvents_ROI_2);
  
  N_G->SetBinContent(5,GeneratedEvents);
  
  SurvivedEvents = SurvivedEvents/400.;// con discriminazione al 99.75%
  cout << "Survived Events in [2,12] con discriminazione   " << SurvivedEvents << endl;

   //compute contamination
   Float_t LiveTime = GeneratedEvents / GammaYield[FlagIsotope]; //s
   Float_t LiveTimeInYear = LiveTime / 365. / 86400. ; // y
   
   cout << " LiveTime " << LiveTime << " s , " << LiveTimeInYear << " y " << endl; 
   cout << "We have " << SurvivedEvents/LiveTimeInYear << " ev/y , if the contamination is " << 1000./Mass << " mBq/kg " << endl;
   
   Float_t FixedContam = 1.; // mBq/kg
   cout << "Number of events per year with 1mBq/kg " <<  SurvivedEvents/LiveTimeInYear / ( 1000./Mass) << endl;
   cout << "CHECK Nb of ev   per year with " << FixedContam << " mBq/kg " <<  SurvivedEvents / GeneratedEvents * GammaYield[FlagIsotope] * FixedContam * 1.e-3 * 365 * 86400 * Mass << endl;
   
   Float_t FixedRate = 0.1; // ev/y
   cout << " Contamination needed to have 0.1 ev/y : " <<  1000./Mass / (   SurvivedEvents/LiveTimeInYear/0.1 ) << endl;
   cout << " CHECK Contam. needed to have " << FixedRate << " ev/y : " <<  FixedRate / 365 / 86400 * GeneratedEvents / GammaYield[FlagIsotope] / SurvivedEvents / Mass * 1000. << " mBq/kg" << endl; 
   
   cout << "Number of events per year with the screened activity of " << ScreenedActivity[FlagIsotope] << " mBq/kg : " <<  ScreenedActivity[FlagIsotope]*SurvivedEvents/LiveTimeInYear / (1000./Mass) << endl;
   
   cout << endl;

   cout << "| " << SurvivedEvents/LiveTimeInYear / ( 1000./Mass) << " | " << 1000./Mass / (   SurvivedEvents/LiveTimeInYear/0.1 ) << " | " << ScreenedActivity[FlagIsotope] << " | " <<  ScreenedActivity[FlagIsotope]*SurvivedEvents/LiveTimeInYear / ( 1000./Mass) << " | " << endl;
   
   
   h2d->Scale(ScaleFactor2d);
   h2dROI->Scale(ScaleFactor2dROI);
   h2dROI_2->Scale(ScaleFactor2dROI_2);
   h2dPri_2->Scale(ScaleFactor2dPri);
  
  // Scale background histogram, to write them normalized to 1 mBq/kg or 1 mBq/PMT
  hEd_1t->Scale(ScaleFactorEr_1tFV/ScreenedActivity[FlagIsotope]);
  hEd_400kg->Scale(ScaleFactorEr_400kgFV/ScreenedActivity[FlagIsotope]);
  hEd_slice1->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  hEd_slice2->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  hEd_slice3->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  hEd_slice4->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  hEd_slice5->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  hEd_slice6->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  hEd_slice7->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  hEd_slice8->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  hEd_slice9->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  hEd_slice10->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  
  hEd_slice1_a->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  hEd_slice1_b->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  hEd_slice1_c->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  hEd_slice1_d->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  hEd_slice1_e->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);

  hEd_slice10_a->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  hEd_slice10_b->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  hEd_slice10_c->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  hEd_slice10_d->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  hEd_slice10_e->Scale(ScaleFactorEr_sliceFV/ScreenedActivity[FlagIsotope]);
  
  h2d->Scale(1./ScreenedActivity[FlagIsotope]);
  h2dROI->Scale(1./ScreenedActivity[FlagIsotope]);
  h2dROI_2->Scale(1./ScreenedActivity[FlagIsotope]);
  
  h2dROI_2_400kg->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice1->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice2->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice3->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice4->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice5->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice6->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice7->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice8->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice9->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice10->Scale(1./ScreenedActivity[FlagIsotope]);

  h2d_slice1_a->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice1_b->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice1_c->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice1_d->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice1_e->Scale(1./ScreenedActivity[FlagIsotope]);

  h2d_slice10_a->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice10_b->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice10_c->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice10_d->Scale(1./ScreenedActivity[FlagIsotope]);
  h2d_slice10_e->Scale(1./ScreenedActivity[FlagIsotope]);

  h2dPri->Scale(1./ScreenedActivity[FlagIsotope]);
  h2dPri_2->Scale(1./ScreenedActivity[FlagIsotope]);
  N_R->Scale(1./ScreenedActivity[FlagIsotope]);
  N_R_p->Scale(1./ScreenedActivity[FlagIsotope]);
  N_R_ROI_2->Scale(1./ScreenedActivity[FlagIsotope]);
  N_G->Scale(1./ScreenedActivity[FlagIsotope]);
  
  // Write histos
  char histoname[30];
  TFile fout("ER-Gamma-mass-scaled.root","UPDATE");
  
  sprintf(histoname,"hEd_1t_%s_%s",Component,cSource[FlagIsotope]);
  hEd_1t->SetName(histoname);

  sprintf(histoname,"hEd_400kg_%s_%s",Component,cSource[FlagIsotope]);
  hEd_400kg->SetName(histoname);

  sprintf(histoname,"hEd_slice1_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice1->SetName(histoname);

  sprintf(histoname,"hEd_slice2_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice2->SetName(histoname);

  sprintf(histoname,"hEd_slice3_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice3->SetName(histoname);

  sprintf(histoname,"hEd_slice4_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice4->SetName(histoname);

  sprintf(histoname,"hEd_slice5_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice5->SetName(histoname);

  sprintf(histoname,"hEd_slice6_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice6->SetName(histoname);

  sprintf(histoname,"hEd_slice7_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice7->SetName(histoname);

  sprintf(histoname,"hEd_slice8_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice8->SetName(histoname);

  sprintf(histoname,"hEd_slice9_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice9->SetName(histoname);

  sprintf(histoname,"hEd_slice10_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice10->SetName(histoname);
  
  sprintf(histoname,"hEd_slice1_a_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice1_a->SetName(histoname);

  sprintf(histoname,"hEd_slice1_b_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice1_b->SetName(histoname);

  sprintf(histoname,"hEd_slice1_c_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice1_c->SetName(histoname);

  sprintf(histoname,"hEd_slice1_d_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice1_d->SetName(histoname);

  sprintf(histoname,"hEd_slice1_e_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice1_e->SetName(histoname);

  sprintf(histoname,"hEd_slice10_a_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice10_a->SetName(histoname);

  sprintf(histoname,"hEd_slice10_b_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice10_b->SetName(histoname);

  sprintf(histoname,"hEd_slice10_c_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice10_c->SetName(histoname);

  sprintf(histoname,"hEd_slice10_d_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice10_d->SetName(histoname);

  sprintf(histoname,"hEd_slice10_e_%s_%s",Component,cSource[FlagIsotope]);
  hEd_slice10_e->SetName(histoname);
  
  sprintf(histoname,"h2d_%s_%s",Component,cSource[FlagIsotope]);
  h2d->SetName(histoname);
  
  sprintf(histoname,"h2dROI_%s_%s",Component,cSource[FlagIsotope]);
  h2dROI->SetName(histoname);
  
  sprintf(histoname,"h2dROI_2_%s_%s",Component,cSource[FlagIsotope]);
  h2dROI_2->SetName(histoname);
  
  sprintf(histoname,"h2dROI_2_400kg_%s_%s",Component,cSource[FlagIsotope]);
  h2dROI_2_400kg->SetName(histoname);

  sprintf(histoname,"h2d_slice1_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice1->SetName(histoname);

  sprintf(histoname,"h2d_slice2_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice2->SetName(histoname);

  sprintf(histoname,"h2d_slice3_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice3->SetName(histoname);

  sprintf(histoname,"h2d_slice4_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice4->SetName(histoname);

  sprintf(histoname,"h2d_slice5_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice5->SetName(histoname);

  sprintf(histoname,"h2d_slice6_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice6->SetName(histoname);

  sprintf(histoname,"h2d_slice7_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice7->SetName(histoname);

  sprintf(histoname,"h2d_slice8_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice8->SetName(histoname);

  sprintf(histoname,"h2d_slice9_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice9->SetName(histoname);

  sprintf(histoname,"h2d_slice10_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice10->SetName(histoname);

  sprintf(histoname,"h2d_slice1_a_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice1_a->SetName(histoname);

  sprintf(histoname,"h2d_slice1_b_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice1_b->SetName(histoname);

  sprintf(histoname,"h2d_slice1_c_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice1_c->SetName(histoname);

  sprintf(histoname,"h2d_slice1_d_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice1_d->SetName(histoname);

  sprintf(histoname,"h2d_slice1_e_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice1_e->SetName(histoname);

  sprintf(histoname,"h2d_slice10_a_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice10_a->SetName(histoname);

  sprintf(histoname,"h2d_slice10_b_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice10_b->SetName(histoname);

  sprintf(histoname,"h2d_slice10_c_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice10_c->SetName(histoname);

  sprintf(histoname,"h2d_slice10_d_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice10_d->SetName(histoname);

  sprintf(histoname,"h2d_slice10_e_%s_%s",Component,cSource[FlagIsotope]);
  h2d_slice10_e->SetName(histoname);

  sprintf(histoname,"h2dPri_%s_%s",Component,cSource[FlagIsotope]);
  h2dPri->SetName(histoname);
  
  sprintf(histoname,"h2dPri_2_%s_%s",Component,cSource[FlagIsotope]);
  h2dPri_2->SetName(histoname);
  
  sprintf(histoname,"check_confinement_%s_%s",Component,cSource[FlagIsotope]);
  h2dPri_noCondition->SetName(histoname);
  
  sprintf(histoname,"N_R_%s_%s",Component,cSource[FlagIsotope]);
  N_R->SetName(histoname);
  
  sprintf(histoname,"N_R_p_%s_%s",Component,cSource[FlagIsotope]);
  N_R_p->SetName(histoname);
  
  sprintf(histoname,"N_R_ROI_2_%s_%s",Component,cSource[FlagIsotope]);
  N_R_ROI_2->SetName(histoname);
  
  sprintf(histoname,"N_G_%s_%s",Component,cSource[FlagIsotope]);
  N_G->SetName(histoname);
  
  hEd_1t->Write();
  hEd_400kg->Write();
  hEd_slice1->Write();
  hEd_slice2->Write();
  hEd_slice3->Write();
  hEd_slice4->Write();
  hEd_slice5->Write();
  hEd_slice6->Write();
  hEd_slice7->Write();
  hEd_slice8->Write();
  hEd_slice9->Write();
  hEd_slice10->Write();
  h2d->Write();
  h2dROI->Write();
  
  h2dROI_2_400kg->Write();
  
  h2d_slice1->Write();
  h2d_slice2->Write();
  h2d_slice3->Write();
  h2d_slice4->Write();
  h2d_slice5->Write();
  h2d_slice6->Write();
  h2d_slice7->Write();
  h2d_slice8->Write();
  h2d_slice9->Write();
  h2d_slice10->Write();

  h2d_slice1_a->Write();
  h2d_slice1_b->Write();
  h2d_slice1_c->Write();
  h2d_slice1_d->Write();
  h2d_slice1_e->Write();

  h2d_slice10_a->Write();
  h2d_slice10_b->Write();
  h2d_slice10_c->Write();
  h2d_slice10_d->Write();
  h2d_slice10_e->Write();
  
  h2dROI_2->Write();
  h2dPri->Write();
  h2dPri_2->Write();
  h2dPri_noCondition->Write();
  N_R->Write();
  N_R_p->Write();
  N_R_ROI_2->Write();
  N_G->Write();
}

int main(int argv, char **argc){
  test m(atoi(argc[1]), atoi(argc[2]));
  m.Loop();
  return 0;
}
