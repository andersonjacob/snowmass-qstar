/* -*- mode: c++ -*- *********************************************************
 * Project: RooFit                                                           *
 *                                                                           *
  * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/

#ifndef ROOERFPDF
#define ROOERFPDF

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"
 
class RooErfPdf : public RooAbsPdf {
public:
  RooErfPdf() {} ; 
  RooErfPdf(const char *name, const char *title,
	    RooAbsReal& _x,
	    RooAbsReal& _turnOn,
	    RooAbsReal& _width);
  RooErfPdf(const RooErfPdf& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new RooErfPdf(*this,newname); }
  inline virtual ~RooErfPdf() { }

  Int_t getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName=0) const ;
  Double_t analyticalIntegral(Int_t code, const char* rangeName=0) const ;

protected:

  double indefIntegral(double val) const ;

  RooRealProxy x ;
  RooRealProxy turnOn ;
  RooRealProxy width ;
  double _onoff ;
  
  Double_t evaluate() const ;

private:

  ClassDef(RooErfPdf,1) // Your description goes here...
};
 
#endif
