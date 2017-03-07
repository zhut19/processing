//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Thu Feb 16 17:28:38 2017 by ROOT version 5.34/32
// from TTree tmc/Monte Carlo results
// found on file:
//////////////////////////////////////////////////////////

#ifndef test_h
#define test_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include <vector>
#include <iostream>

using namespace std;

// Fixed size dimensions of array or collections stored in the TTree if any.

class test {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
   Int_t           eventid;
   Float_t         nr_ed;
   Float_t         er_ed;
   Float_t         xpos;
   Float_t         ypos;
   Float_t         zpos;
   Int_t           fid_hits;
   Int_t           elas_hits;
   Int_t           inel_hits;
   Int_t           NeutCapt;
   Float_t         xpri;
   Float_t         ypri;
   Float_t         zpri;
   Float_t         epri;
   vector<string>  *type;
   Float_t         TotNrgVeto;
   Float_t         TotNrgBc;

   // List of branches
   TBranch        *b_eventid;   //!
   TBranch        *b_nr_ed;   //!
   TBranch        *b_er_ed;   //!
   TBranch        *b_xpos;   //!
   TBranch        *b_ypos;   //!
   TBranch        *b_zpos;   //!
   TBranch        *b_fid_hits;   //!
   TBranch        *b_elas_hits;   //!
   TBranch        *b_inel_hits;   //!
   TBranch        *b_NeutCapt;   //!
   TBranch        *b_xpri;   //!
   TBranch        *b_ypri;   //!
   TBranch        *b_zpri;   //!
   TBranch        *b_epri;   //!
   TBranch        *b_type;   //!
   TBranch        *b_TotNrgVeto;   //!
   TBranch        *b_TotNrgBc;   //!

   test(Int_t FlagSource, Int_t FlagIsotope, TTree *tree=0);
   virtual ~test();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);

    // variables for Background estimation
   char Component[10];
   Double_t Mass, GeneratedEvents;
   Double_t GammaYield[10];
   Double_t ScreenedActivity[10];
   char Material[10];
   Int_t FlagSource;
   Int_t FlagIsotope;
};

#endif

#ifdef test_cxx
test::test(Int_t FlagSource_, Int_t FlagIsotope_, TTree *tree) : fChain(0) 
{
  FlagSource = FlagSource_;
  FlagIsotope = FlagIsotope_;
  
  
  if (tree == 0) {

#ifdef SINGLE_TREE
      // The following code should be used if you want this class to access
      // a single tree instead of a chain
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("/Users/selvi/xenon/geant4/xenon1t/data/neutrons/CryoSS-Acrylic5cm-Flat/neutron-CryoSS-flat-100_sort.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("/Users/selvi/xenon/geant4/xenon1t/data/neutrons/CryoSS-Acrylic5cm-Flat/neutron-CryoSS-flat-100_sort.root");
      }
      f->GetObject("tmc",tree);

#else // SINGLE_TREE
      
      // The following code should be used if you want this class to access a chain
      // of trees.
      char Isot[7][8] = {"U238","Ra226","Th232","Th228","Co60","K40","Cs137"};
      char isot[10];
      
      //_____selezione del file da utilizzaere ________________________________________________________
      if(FlagIsotope==0)
	sprintf(isot,Isot[0]);
	
      if(FlagIsotope==1)
	sprintf(isot,Isot[0]);
	
      if(FlagIsotope==2)
	sprintf(isot,Isot[2]);
	
      if(FlagIsotope==3)
	sprintf(isot,Isot[2]);
	
      if(FlagIsotope==4)
	sprintf(isot,Isot[4]);
	
      if(FlagIsotope==5)
	sprintf(isot,Isot[5]);
      
      if(FlagIsotope==6)
	sprintf(isot,Isot[6]);
      
      //_______________________________________________________________________________________________
     
      
      switch(FlagSource)
	{
	case(1): // stainless steel from Cryostat Shells
	  {TChain * chain = new TChain("tmc","");
	  Int_t Nfiles = 500;
	  Int_t contatore = 0;
	  Int_t start = 1;
	  
	  if(FlagIsotope==0 || FlagIsotope==1) Nfiles = 800;
	  if(FlagIsotope==6)
	    {
	      start  = 306;
	      Nfiles = 405;
	    }
	      
	  Int_t CorruptedFiles=0;
	  
	  TFile *f;
	  for(Int_t i=start; i<=Nfiles; ++i)
	    {
	      if(i<101 || i>300)
		{ 
		  contatore++;
		  char filename[200];
		  sprintf(filename,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/Cryostat/%s/Cryostat-%s-%d_sort.root/tmc",isot,isot,i);
		  
		  char filename2[200];
		  sprintf(filename2,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/Cryostat/%s/Cryostat-%s-%d_sort.root",isot,isot,i);
		  f = new TFile(filename2);
		  if(f->IsZombie()) CorruptedFiles++;
		  f->Close();
		  
		  chain->Add(filename);
		  tree = chain;
		}
	    }
	  cout << "CorruptedFiles = " << CorruptedFiles << endl;
	  Mass = 1440.;
	  
	  Double_t dScreenedActivity[7] = { 2.4, 0.64, 0.21, 0.36, 9.7, 2.7, 0.64};
	  Double_t dTotalSteps[7]      = { 14, 14, 10, 10, 1, 1, 1.97};
	  Double_t dGammaYield[7]     = { 5, 9, 3, 7, 1, 1, 1};
	  
	  if(FlagIsotope==4)
	    GeneratedEvents = 5.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  else
	    GeneratedEvents = 1.e7 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  for(Int_t i5=0; i5<7; ++i5){
	    ScreenedActivity[i5]=dScreenedActivity[i5];
	    GammaYield[i5]=dGammaYield[i5];
	  }
	  
	  sprintf( Material, "steel");
	  sprintf( Component, "Shell");
	  cout << "Component: " << Component << ", Material: " << Material << endl;
	  cout << "Isotope [0,6]:  " << FlagIsotope << endl;
	  }break;
	  
	case(2): // stainless steel from Cryostat Flanges
	  {TChain * chain = new TChain("tmc","");
	  Int_t Nfiles = 500;
	  Int_t CorruptedFiles=0;
	  Int_t contatore = 0;
	  Int_t start = 1;
	  
	  if(FlagIsotope==0 || FlagIsotope==1) Nfiles = 800;
	   if(FlagIsotope==6)
	    {
	      start  = 306;
	      Nfiles = 405;
	    }
	  
	  TFile *f;
	  for(Int_t i=start; i<=Nfiles; ++i)
	    {
	      if(i<101 || i>300) 
		{ 
		  contatore++;
		  char filename[200];
		  sprintf(filename,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/Cryostat/%s/Cryostat-%s-%d_sort.root/tmc",isot,isot,i);
		  
		  char filename2[200];
		  sprintf(filename2,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/Cryostat/%s/Cryostat-%s-%d_sort.root",isot,isot,i);
		  f = new TFile(filename2);
		  if(f->IsZombie()) CorruptedFiles++;
		  f->Close();
		  
		  chain->Add(filename);
		  tree = chain;
		}
	    }
	  Mass = 1440.;
	  
	  cout << "CorruptedFiles = " << CorruptedFiles << endl;
	  Double_t dScreenedActivity[7] = {1.4, 4.0, 0.21, 4.5, 37.3, 5.6, 1.5};
	  Double_t dTotalSteps[7]      = { 14, 14, 10, 10, 1, 1, 1.97};
	  Double_t dGammaYield[7]     = { 5, 9, 3, 7, 1, 1, 1};
	  
	  if(FlagIsotope==4)
	    GeneratedEvents = 5.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  else
	    GeneratedEvents = 1.e7 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  for(Int_t i5=0; i5<7; ++i5){
	    ScreenedActivity[i5]=dScreenedActivity[i5];
	    GammaYield[i5]=dGammaYield[i5];
	  }
	  
	  sprintf( Material, "steel");
	  sprintf( Component, "Flange");
	  cout << "Component: " << Component << ", Material: " << Material << endl;
	  cout << "Isotope [0,6]:  " << FlagIsotope << endl;
	  }break;
	  
	case(3): // PMTs
	  {TChain * chain = new TChain("tmc","");
	  Int_t Nfiles = 300;
	  Int_t CorruptedFiles=0;
	  Int_t contatore = 0;
	  Int_t start = 1;

	   if(FlagIsotope==6)
	    {
	      start  = 306;
	      Nfiles = 405;
	    }

	  //Th232=68 ; Co60=74 ; U238=100 ; K40=137 ;
	
	  TFile *f;
	  for(Int_t i=start; i<=Nfiles; ++i){
	    contatore++;
	    char filename[200];
	    sprintf(filename,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/Pmt/%s/Pmt-%s-%d_sort.root/tmc",isot,isot,i);
	    
	    char filename2[200];
	    sprintf(filename2,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/Pmt/%s/Pmt-%s-%d_sort.root",isot,isot,i);
	    f = new TFile(filename2);
	    if(f->IsZombie()) CorruptedFiles++;
	    f->Close();
	    
	    chain->Add(filename);
	    tree = chain;
	  }
	  Mass = 248.;
	  
	  cout << "CorruptedFiles = " << CorruptedFiles << endl;
	  Double_t dScreenedActivity[7] = {8., 0.5, 0.5, 0.50, 0.71, 13., 0.18};
	  Double_t dTotalSteps[7]      = { 14, 14, 10, 10, 1, 1, 1.97};
	  Double_t dGammaYield[7]     = { 5, 9, 3, 7, 1, 1, 1};
	  
	  if(FlagIsotope==4)
	    GeneratedEvents = 2.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  if(FlagIsotope==6)
	    GeneratedEvents = 5.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  if(FlagIsotope!=4 && FlagIsotope!=6)
	    GeneratedEvents = 1.e7 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  for(Int_t i5=0; i5<7; ++i5){
	    ScreenedActivity[i5]=dScreenedActivity[i5];
	    GammaYield[i5]=dGammaYield[i5];
	  }
	  
	  sprintf( Material, "Pmt");
	  sprintf( Component, "Pmt");
	  cout << "Component: " << Component << ", Material: " << Material << endl;
	  cout << "Isotope [0,6]:  " << FlagIsotope << endl;
	  }break;
	  
	case(4): // PMT Bases
	  {TChain * chain = new TChain("tmc","");
	  Int_t Nfiles = 300;
	  Int_t CorruptedFiles=0;
	  Int_t contatore = 0;
	  Int_t start = 1;
	  
	   if(FlagIsotope==6)
	    {
	      start  = 306;
	      Nfiles = 405;
	    }

	  if(FlagIsotope==5)  Nfiles=500;
	  
	  TFile *f;
	  for(Int_t i=start; i<=Nfiles; ++i){
	    contatore++;
	    char filename[200];
	    sprintf(filename,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/Cirlex/%s/Cirlex-%s-%d_sort.root/tmc",isot,isot,i);
	    
	    char filename2[200];
	    sprintf(filename2,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/Cirlex/%s/Cirlex-%s-%d_sort.root",isot,isot,i);
	    f = new TFile(filename2);
	    if(f->IsZombie()) CorruptedFiles++;
	    f->Close();
	    
	    chain->Add(filename);
	    tree = chain;
	  }
	  Mass = 248;
	  
	  cout << "CorruptedFiles = " << CorruptedFiles << endl;
	  Double_t dScreenedActivity[7] = {4.6, 0.46, 0.23, 0.12, 0.016, 0.45, 0.0098};
	  Double_t dTotalSteps[7]      = { 14, 14, 10, 10, 1, 1, 1.97};
	  Double_t dGammaYield[7]     = { 5, 9, 3, 7, 1, 1, 1};
	  
	  if(FlagIsotope==4)
	    GeneratedEvents = 2.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  if(FlagIsotope==6)
	    GeneratedEvents = 5.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  if(FlagIsotope!=4 && FlagIsotope!=6)
	    GeneratedEvents = 1.e7 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  for(Int_t i5=0; i5<7; ++i5){
	    ScreenedActivity[i5]=dScreenedActivity[i5];
	    GammaYield[i5]=dGammaYield[i5];
	  }
	  
	  sprintf( Material, "cirlex");
	  sprintf( Component, "PMTbases");
	  cout << "Component: " << Component << ", Material: " << Material << endl;
	  cout << "Isotope [0,6]:  " << FlagIsotope << endl;
	  }break;

	case(5): // TPC PTFE
	  {TChain * chain = new TChain("tmc","");
	  Int_t Nfiles = 400;
	  Int_t CorruptedFiles=0;
	  Int_t contatore = 0;
	  Int_t start = 1;
	  
	   if(FlagIsotope==6)
	    {
	      start  = 306;
	      Nfiles = 405;
	    }

	  //Th232=233 ; Co60=227 ; U238=238 ; K40=219 ;
	  
	  TFile *f;
	  for(Int_t i=start; i<=Nfiles; ++i){
	    contatore++;
	    char filename[200];
	    sprintf(filename,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/PTFE/%s/PTFE-%s-%d_sort.root/tmc",isot,isot,i);

	    char filename2[200];
	    sprintf(filename2,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/PTFE/%s/PTFE-%s-%d_sort.root",isot,isot,i);
	    f = new TFile(filename2);
	    if(f->IsZombie()) CorruptedFiles++;
	    f->Close();
	    
	    chain->Add(filename);
	    tree = chain;
	  }
	  Mass = 91.5;
	  
	  cout << "CorruptedFiles = " << CorruptedFiles << endl;
	  Double_t dScreenedActivity[7] = {3.0, 0.06, 0.16, 0.10, 0.03, 0.075, 0.170};
	  Double_t dTotalSteps[7]      = { 14, 14, 10, 10, 1, 1, 1.97};
	  Double_t dGammaYield[7]     = {  5,   9,  3,  7, 1, 1, 1};
	  
	  if(FlagIsotope==4)
	    GeneratedEvents = 2.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	 
	  if(FlagIsotope==6)
	    GeneratedEvents = 5.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  if(FlagIsotope!=4 && FlagIsotope!=6)
	    GeneratedEvents = 1.e7 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];

	  for(Int_t i5=0; i5<7; ++i5){
	    ScreenedActivity[i5]=dScreenedActivity[i5];
	    GammaYield[i5]=dGammaYield[i5];
	  }
	  
	  sprintf( Material, "teflon");
	  sprintf( Component, "PTFE");
	  cout << "Component: " << Component << ", Material: " << Material << endl;
	  cout << "Isotope [0,6]:  " << FlagIsotope << endl;
	  cout << " dGammaYield " << dGammaYield[FlagIsotope] << endl;
	  cout << "dTotalSteps " << dTotalSteps[FlagIsotope] << endl;
	  cout << "Generated events " << GeneratedEvents << endl;
	  }break;
	  
	case(6): // TPC Copper
	  {TChain * chain = new TChain("tmc","");
	  Int_t Nfiles = 400;
	  Int_t CorruptedFiles=0;
	  Int_t contatore = 0;
	  Int_t start = 1;
	  
	   if(FlagIsotope==6)
	    {
	      start  = 306;
	      Nfiles = 405;
	    }

	  TFile *f;
	  for(Int_t i=start; i<=Nfiles; ++i){
	    contatore++;
	    char filename[200];
	    sprintf(filename,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/Copper/%s/Copper-%s-%d_sort.root/tmc",isot,isot,i);
	    
	    char filename2[200];
	    sprintf(filename2,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/Copper/%s/Copper-%s-%d_sort.root",isot,isot,i);
	    f = new TFile(filename2);
	    if(f->IsZombie()) CorruptedFiles++;
	    f->Close();
	    
	    chain->Add(filename);
	    tree = chain;
	  }
	  Mass = 166.;
	  
	  cout << "CorruptedFiles = " << CorruptedFiles << endl;
	  Double_t dScreenedActivity[7] = {0.07, 0.07, 0.021, 0.021, 0.002, 0.023, 0.14};//mettere il Cs giusto
	  Double_t dTotalSteps[7]      = { 14, 14, 10, 10, 1, 1, 1.97};
	  Double_t dGammaYield[7]     = { 5, 9, 3, 7, 1, 1, 1};
	  
	  if(FlagIsotope==4)
	    GeneratedEvents = 2.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  if(FlagIsotope==6)
	    GeneratedEvents = 5.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  	  
	  if(FlagIsotope!=4 && FlagIsotope!=6)
	    GeneratedEvents = 1.e7 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];

	  for(Int_t i5=0; i5<7; ++i5){
	    ScreenedActivity[i5]=dScreenedActivity[i5];
	    GammaYield[i5]=dGammaYield[i5];
	  }
	  
	  sprintf( Material, "copper");
	  sprintf( Component, "TPCcopper");
	  cout << "Component: " << Component << ", Material: " << Material << endl;
	  cout << "Isotope [0,6]:  " << FlagIsotope << endl;
	  }break;

	  /*	case(11): // Bottom Filler SS
	  {TChain * chain = new TChain("tmc","");
	  Int_t Nfiles = 600;
	  Int_t CorruptedFiles=0;
	  Int_t contatore = 0;
	  Int_t start = 300;
	  
	   if(FlagIsotope==6)
	    {
	      start  = 206;
	      Nfiles = 405;
	    }

	  TFile *f;
	  for(Int_t i=start; i<=Nfiles; ++i){
	    contatore++;
	    char filename[200];
	    
	    if(FlagIsotope==6)
	      sprintf(filename,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/SS/%s/SS-%s-%d_sort.root/tmc",isot,isot,i);
	    else
	      sprintf(filename,"/archive_lngs100TB/mc/xe1tsim/selvi/GridMirror/v300/SS/%s/SS-%s-%d_sort.root/tmc",isot,isot,i);
	    char filename2[200];

	    if(FlagIsotope==6)
	      sprintf(filename2,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/SS/%s/SS-%s-%d_sort.root",isot,isot,i);
	    else
	      sprintf(filename2,"/archive_lngs100TB/mc/xe1tsim/selvi/GridMirror/v300/SS/%s/SS-%s-%d_sort.root",isot,isot,i);
	    f = new TFile(filename2);
	    if(f->IsZombie()) CorruptedFiles++;
	    f->Close();
	    
	    chain->Add(filename);
	    tree = chain;
	  }
	  Mass = 149.;//169.3;

	  cout << "CorruptedFiles = " << CorruptedFiles << endl;
	  Double_t dScreenedActivity[7] = {11, 1.2, 1.2, 2.0, 5.5, 1.3, 0.58};
	  Double_t dTotalSteps[7]      = { 14, 14, 10, 10, 1, 1, 1.97};
	  Double_t dGammaYield[7]     = { 5, 9, 3, 7, 1, 1, 1};
	  
	  if(FlagIsotope==4)
	    GeneratedEvents = 2.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];

	  if(FlagIsotope==6)
	    GeneratedEvents = 5.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  	  
	  if(FlagIsotope!=4 && FlagIsotope!=6)
	    GeneratedEvents = 1.e7 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];

	  for(Int_t i5=0; i5<7; ++i5){
	    ScreenedActivity[i5]=dScreenedActivity[i5];
	    GammaYield[i5]=dGammaYield[i5];
	  }
	  
	  sprintf( Material, "steel");
	  sprintf( Component, "BottomFiller");
	  cout << "Component: " << Component << ", Material: " << Material << endl;
	  cout << "Isotope [0,6]:  " << FlagIsotope << endl;
	  }break;*/
	
	case(12): // Cathode & Anode ring, ss_plate+ss_ring_lxe
	  {TChain * chain = new TChain("tmc","");
	  Int_t Nfiles = 600;
	  Int_t CorruptedFiles=0;
	  Int_t contatore = 0;
	  Int_t start = 300;

	   if(FlagIsotope==6)
	    {
	      start  = 206;
	      Nfiles = 405;
	    }
	  
	  TFile *f;
	  for(Int_t i=start; i<=Nfiles; ++i){
	    contatore++;
	    char filename[200];
	    if(FlagIsotope==6)
	      sprintf(filename,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/SS/%s/SS-%s-%d_sort.root/tmc",isot,isot,i);
	    else
	      sprintf(filename,"/archive_lngs100TB/mc/xe1tsim/selvi/GridMirror/v300/SS/%s/SS-%s-%d_sort.root/tmc",isot,isot,i);
	    char filename2[200];
	    if(FlagIsotope==6)
	      sprintf(filename2,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/SS/%s/SS-%s-%d_sort.root",isot,isot,i);
	    else
	      sprintf(filename2,"/archive_lngs100TB/mc/xe1tsim/selvi/GridMirror/v300/SS/%s/SS-%s-%d_sort.root",isot,isot,i);
	      
	    f = new TFile(filename2);
	    if(f->IsZombie()) CorruptedFiles++;
	    f->Close();
	    
	    chain->Add(filename);
	    tree = chain;
	  }
	  Mass = 78.;//149.;

	  cout << "CorruptedFiles = " << CorruptedFiles << endl;
	  Double_t dScreenedActivity[7] = {1.4, 4.0, 0.21, 4.5, 37.3, 5.6, 0.58};
	  Double_t dTotalSteps[7]      = { 14, 14, 10, 10, 1, 1, 1.97};
	  Double_t dGammaYield[7]     = { 5, 9, 3, 7, 1, 1, 1};
	  
	  if(FlagIsotope==4)
	    GeneratedEvents = 2.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  if(FlagIsotope==6)
	    GeneratedEvents = 5.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  	  
	  if(FlagIsotope!=4 && FlagIsotope!=6)
	    GeneratedEvents = 1.e7 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];

	  for(Int_t i5=0; i5<7; ++i5){
	    ScreenedActivity[i5]=dScreenedActivity[i5];
	    GammaYield[i5]=dGammaYield[i5];
	  }
	  
	  sprintf( Material, "steel");
	  sprintf( Component, "MiddleSS");
	  cout << "Component: " << Component << ", Material: " << Material << endl;
	  cout << "Isotope [0,6]:  " << FlagIsotope << endl;
	  } break;

	case(13): // lateral Bell
	  {TChain * chain = new TChain("tmc","");
	  Int_t Nfiles = 600;
	  Int_t CorruptedFiles=0;
	  Int_t contatore = 0;
	  Int_t start = 300;
	  
	  if(FlagIsotope==6)
	    {
	      start  = 206;
	      Nfiles = 405;
	    }
	  
	  TFile *f;
	  for(Int_t i=start; i<=Nfiles; ++i){
	    contatore++;
	    
	    char filename[200];
	    if(FlagIsotope==6)
	      sprintf(filename,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/SS/%s/SS-%s-%d_sort.root/tmc",isot,isot,i);
	    else
	      sprintf(filename,"/archive_lngs100TB/mc/xe1tsim/selvi/GridMirror/v300/SS/%s/SS-%s-%d_sort.root/tmc",isot,isot,i);
	    char filename2[200];
	    if(FlagIsotope==6)
	      sprintf(filename2,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/SS/%s/SS-%s-%d_sort.root",isot,isot,i);
	    else
	      sprintf(filename2,"/archive_lngs100TB/mc/xe1tsim/selvi/GridMirror/v300/SS/%s/SS-%s-%d_sort.root",isot,isot,i);

	    f = new TFile(filename2);
	    if(f->IsZombie()) CorruptedFiles++;
	    f->Close();
	    
	    chain->Add(filename);
	    tree = chain;
	  }
	  Mass = 78.;//149.;

	  cout << "CorruptedFiles = " << CorruptedFiles << endl;
	  Double_t dScreenedActivity[7] = {50., 3.6, 0.81, 1.8, 7., 5.7, 0.58};
	  Double_t dTotalSteps[7]      = { 14, 14, 10, 10, 1, 1, 1.97};
	  Double_t dGammaYield[7]     = { 5, 9, 3, 7, 1, 1, 1};
	  
	  if(FlagIsotope==4)
	    GeneratedEvents = 2.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  if(FlagIsotope==6)
	    GeneratedEvents = 5.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  if(FlagIsotope!=4 && FlagIsotope!=6)
	    GeneratedEvents = 1.e7 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  for(Int_t i5=0; i5<7; ++i5){
	    ScreenedActivity[i5]=dScreenedActivity[i5];
	    GammaYield[i5]=dGammaYield[i5];
	  }
	  
	  sprintf( Material, "steel");
	  sprintf( Component, "LateralBell");
	  cout << "Component: " << Component << ", Material: " << Material << endl;
	  cout << "Isotope [0,6]:  " << FlagIsotope << endl;
	  }break;
	  
	case(14): // Bottom & Top ring
	  {TChain * chain = new TChain("tmc","");
	  Int_t Nfiles = 600;
	  Int_t CorruptedFiles=0;
	  Int_t contatore = 0;
	  Int_t start = 300;

	   if(FlagIsotope==6)
	    {
	      start  = 206;
	      Nfiles = 405;
	    }
	  
	  TFile *f;
	  for(Int_t i=start; i<=Nfiles; ++i){
	    contatore++;
	    char filename[200];
	    
	    if(FlagIsotope==6)
	      sprintf(filename,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/SS/%s/SS-%s-%d_sort.root/tmc",isot,isot,i);
	    else
	      sprintf(filename,"/archive_lngs100TB/mc/xe1tsim/selvi/GridMirror/v300/SS/%s/SS-%s-%d_sort.root/tmc",isot,isot,i);
	      
	    char filename2[200];
	    if(FlagIsotope==6)
	      sprintf(filename2,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/SS/%s/SS-%s-%d_sort.root",isot,isot,i);
	    else
	      sprintf(filename2,"/archive_lngs100TB/mc/xe1tsim/selvi/GridMirror/v300/SS/%s/SS-%s-%d_sort.root",isot,isot,i);
	      
	    f = new TFile(filename2);
	    if(f->IsZombie()) CorruptedFiles++;
	    f->Close();
	    
	    chain->Add(filename);
	    tree = chain;
	  }
	  Mass = 78.;//149.;

	  cout << "CorruptedFiles = " << CorruptedFiles << endl;
	  Double_t dScreenedActivity[7] = {2.4, 0.64, 0.21, 0.36, 9.7, 2.7, 0.58};
	  Double_t dTotalSteps[7]      = { 14, 14, 10, 10, 1, 1, 1.97};
	  Double_t dGammaYield[7]     = { 5, 9, 3, 7, 1, 1, 1};
	  
	  if(FlagIsotope==4)
	    GeneratedEvents = 2.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  if(FlagIsotope==6)
	    GeneratedEvents = 5.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  if(FlagIsotope!=4 && FlagIsotope!=6)
	    GeneratedEvents = 1.e7 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  for(Int_t i5=0; i5<7; ++i5){
	    ScreenedActivity[i5]=dScreenedActivity[i5];
	    GammaYield[i5]=dGammaYield[i5];
	  }
	  
	  
	  sprintf( Material, "steel");
	  sprintf( Component, "BottomTopRing");
	  cout << "Component: " << Component << ", Material: " << Material << endl;
	  cout << "Isotope [0,6]:  " << FlagIsotope << endl;
	  }break;

	case(15): // Top Bell
	  {TChain * chain = new TChain("tmc","");
	  Int_t Nfiles = 600;
	  Int_t CorruptedFiles=0;
	  Int_t contatore = 0;
	  Int_t start = 300;

	   if(FlagIsotope==6)
	    {
	      start  = 206;
	      Nfiles = 405;
	    }
	  
	  TFile *f;
	  for(Int_t i=start; i<=Nfiles; ++i){
	    contatore++;
	    char filename[200];
	    
	    if(FlagIsotope==6)
	      sprintf(filename,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/SS/%s/SS-%s-%d_sort.root/tmc",isot,isot,i);
	    else
	      sprintf(filename,"/archive_lngs100TB/mc/xe1tsim/selvi/GridMirror/v300/SS/%s/SS-%s-%d_sort.root/tmc",isot,isot,i);
	      
	    char filename2[200];
	    if(FlagIsotope==6)
	      sprintf(filename2,"/archive_lngs100TB/mc/xe1tsim/massoli/GridMirror/v300/SS/%s/SS-%s-%d_sort.root",isot,isot,i);
	    else
	      sprintf(filename2,"/archive_lngs100TB/mc/xe1tsim/selvi/GridMirror/v300/SS/%s/SS-%s-%d_sort.root",isot,isot,i);
	  
	    f = new TFile(filename2);
	    if(f->IsZombie()) CorruptedFiles++;
	    f->Close();
	    
	    chain->Add(filename);
	    tree = chain;
	  }
	  Mass = 78.;//149.;

	  cout << "CorruptedFiles = " << CorruptedFiles << endl;
	  Double_t dScreenedActivity[7] = {2.4, 0.64, 0.21, 0.36, 9.7, 2.7, 0.58};
	  Double_t dTotalSteps[7]      = { 14, 14, 10, 10, 1, 1, 1.97};
	  Double_t dGammaYield[7]     = { 5, 9, 3, 7, 1, 1, 1};
	  
	  if(FlagIsotope==4)
	    GeneratedEvents = 2.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  if(FlagIsotope==6)
	    GeneratedEvents = 5.e6 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  if(FlagIsotope!=4 && FlagIsotope!=6)
	    GeneratedEvents = 1.e7 * (contatore-CorruptedFiles) * dGammaYield[FlagIsotope]/dTotalSteps[FlagIsotope];
	  
	  for(Int_t i5=0; i5<7; ++i5){
	    ScreenedActivity[i5]=dScreenedActivity[i5];
	    GammaYield[i5]=dGammaYield[i5];
	  }
	  
	  sprintf( Material, "steel");
	  sprintf( Component, "TopBell");
	  cout << "Component: " << Component << ", Material: " << Material << endl;
	  cout << "Isotope [0,6]:  " << FlagIsotope << endl;
	  }break;
	  
	default :
	  cout << " Flag " << FlagSource << " is NOT a defined Source " << endl;
	  
	}

#endif // SINGLE_TREE
        
   }
   Init(tree);
}

test::~test()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t test::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t test::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void test::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   type = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("eventid", &eventid, &b_eventid);
   fChain->SetBranchAddress("nr_ed", &nr_ed, &b_nr_ed);
   fChain->SetBranchAddress("er_ed", &er_ed, &b_er_ed);
   fChain->SetBranchAddress("xpos", &xpos, &b_xpos);
   fChain->SetBranchAddress("ypos", &ypos, &b_ypos);
   fChain->SetBranchAddress("zpos", &zpos, &b_zpos);
   fChain->SetBranchAddress("fid_hits", &fid_hits, &b_fid_hits);
   fChain->SetBranchAddress("elas_hits", &elas_hits, &b_elas_hits);
   fChain->SetBranchAddress("inel_hits", &inel_hits, &b_inel_hits);
   fChain->SetBranchAddress("NeutCapt", &NeutCapt, &b_NeutCapt);
   fChain->SetBranchAddress("xpri", &xpri, &b_xpri);
   fChain->SetBranchAddress("ypri", &ypri, &b_ypri);
   fChain->SetBranchAddress("zpri", &zpri, &b_zpri);
   fChain->SetBranchAddress("epri", &epri, &b_epri);
   fChain->SetBranchAddress("typepri", &type, &b_type);
   fChain->SetBranchAddress("TotNrgVeto", &TotNrgVeto, &b_TotNrgVeto);
   fChain->SetBranchAddress("TotNrgBc", &TotNrgBc, &b_TotNrgBc);
   Notify();
}

Bool_t test::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void test::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t test::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef test_cxx
