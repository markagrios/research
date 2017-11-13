/*  Vector field function and events for Radau integrator.
  This code was automatically generated by PyDSTool, but may be modified by hand. */

#include <math.h>
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "events.h"
#include "maxmin.h"
#include "signum.h"
#include "vfield.h"

extern double *gICs;
extern double **gBds;
extern double globalt0;

static double pi = 3.1415926535897931;

double signum(double x)
{
  if (x<0) {
    return -1;
  }
  else if (x==0) {
    return 0;
  }
  else if (x>0) {
    return 1;
  }
  else {
    /* must be that x is Not-a-Number */
    return x;
  }
}


/* Variable, aux variable, parameter, and input definitions: */ 
#define I	p_[0]
#define Vo	p_[1]
#define a	p_[2]
#define b	p_[3]
#define c	p_[4]
#define d	p_[5]
#define g	p_[6]
#define lam	p_[7]
#define r	p_[8]
#define s	p_[9]
#define thet	p_[10]
#define xR	p_[11]
#define x1	Y_[0]
#define x2	Y_[1]
#define y1	Y_[2]
#define y2	Y_[3]
#define z1	Y_[4]
#define z2	Y_[5]


double __maxof2(double e1_, double e2_, double *p_, double *wk_, double *xv_);
double __maxof3(double e1_, double e2_, double e3_, double *p_, double *wk_, double *xv_);
double __maxof4(double e1_, double e2_, double e3_, double e4_, double *p_, double *wk_, double *xv_);
double __minof2(double e1_, double e2_, double *p_, double *wk_, double *xv_);
double __minof3(double e1_, double e2_, double e3_, double *p_, double *wk_, double *xv_);
double __minof4(double e1_, double e2_, double e3_, double e4_, double *p_, double *wk_, double *xv_);
double __rhs_if(int cond_, double e1_, double e2_, double *p_, double *wk_, double *xv_);
double gam(double __X__, double *p_, double *wk_, double *xv_);
double getbound(char *name, int which_bd, double *p_, double *wk_, double *xv_);
double globalindepvar(double t, double *p_, double *wk_, double *xv_);
double initcond(char *varname, double *p_, double *wk_, double *xv_);
int getindex(char *name, double *p_, double *wk_, double *xv_);
int heav(double x_, double *p_, double *wk_, double *xv_);

int N_EVENTS = 0;
void assignEvents(EvFunType *events){
 
}

void auxvars(unsigned, unsigned, double, double*, double*, double*, unsigned, double*, unsigned, double*);
void jacobian(unsigned, unsigned, double, double*, double*, double**, unsigned, double*, unsigned, double*);
void jacobianParam(unsigned, unsigned, double, double*, double*, double**, unsigned, double*, unsigned, double*);
int N_AUXVARS = 0;


int N_EXTINPUTS = 0;


void vfieldfunc(unsigned n_, unsigned np_, double t, double *Y_, double *p_, double *f_, unsigned wkn_, double *wk_, unsigned xvn_, double *xv_){

f_[0] = y1-a*x1*x1*x1+b*x1*x1+I-z1-g*(x1-Vo)*gam(x2, p_, wk_, xv_);
f_[1] = y2-a*x2*x2*x2+b*x2*x2+I-z2-g*(x2-Vo)*gam(x1, p_, wk_, xv_);
f_[2] = c-d*x1*x1-y1;
f_[3] = c-d*x2*x2-y2;
f_[4] = r*(s*(x1-xR)-z1);
f_[5] = r*(s*(x2-xR)-z2);

}




double __maxof2(double e1_, double e2_, double *p_, double *wk_, double *xv_) {
if (e1_ > e2_) {return e1_;} else {return e2_;};
}


double __maxof3(double e1_, double e2_, double e3_, double *p_, double *wk_, double *xv_) {
double temp_;
if (e1_ > e2_) {temp_ = e1_;} else {temp_ = e2_;};
if (e3_ > temp_) {return e3_;} else {return temp_;};
}


double __maxof4(double e1_, double e2_, double e3_, double e4_, double *p_, double *wk_, double *xv_) {
double temp_;
if (e1_ > e2_) {temp_ = e1_;} else {temp_ = e2_;};
if (e3_ > temp_) {temp_ = e3_;};
if (e4_ > temp_) {return e4_;} else {return temp_;};
}


double __minof2(double e1_, double e2_, double *p_, double *wk_, double *xv_) {
if (e1_ < e2_) {return e1_;} else {return e2_;};
}


double __minof3(double e1_, double e2_, double e3_, double *p_, double *wk_, double *xv_) {
double temp_;
if (e1_ < e2_) {temp_ = e1_;} else {temp_ = e2_;};
if (e3_ < temp_) {return e3_;} else {return temp_;};
}


double __minof4(double e1_, double e2_, double e3_, double e4_, double *p_, double *wk_, double *xv_) {
double temp_;
if (e1_ < e2_) {temp_ = e1_;} else {temp_ = e2_;};
if (e3_ < temp_) {temp_ = e3_;};
if (e4_ < temp_) {return e4_;} else {return temp_;};
}


double __rhs_if(int cond_, double e1_, double e2_, double *p_, double *wk_, double *xv_) {
  if (cond_) {return e1_;} else {return e2_;};
}


double gam(double __X__, double *p_, double *wk_, double *xv_) {


return 1/(1+exp((-1*lam*(__X__-thet))));

}


double getbound(char *name, int which_bd, double *p_, double *wk_, double *xv_) {
  return gBds[which_bd][getindex(name, p_, wk_, xv_)];
}


double globalindepvar(double t, double *p_, double *wk_, double *xv_) {
  return globalt0+t;
}


double initcond(char *varname, double *p_, double *wk_, double *xv_) {

  if (strcmp(varname, "x1")==0)
	return gICs[0];
  else if (strcmp(varname, "x2")==0)
	return gICs[1];
  else if (strcmp(varname, "y1")==0)
	return gICs[2];
  else if (strcmp(varname, "y2")==0)
	return gICs[3];
  else if (strcmp(varname, "z1")==0)
	return gICs[4];
  else if (strcmp(varname, "z2")==0)
	return gICs[5];
  else {
	fprintf(stderr, "Invalid variable name %s for initcond call\n", varname);
	return 0.0/0.0;
	}
}


int getindex(char *name, double *p_, double *wk_, double *xv_) {

  if (strcmp(name, "x1")==0)
	return 0;
  else if (strcmp(name, "x2")==0)
	return 1;
  else if (strcmp(name, "y1")==0)
	return 2;
  else if (strcmp(name, "y2")==0)
	return 3;
  else if (strcmp(name, "z1")==0)
	return 4;
  else if (strcmp(name, "z2")==0)
	return 5;
  else if (strcmp(name, "I")==0)
	return 6;
  else if (strcmp(name, "Vo")==0)
	return 7;
  else if (strcmp(name, "a")==0)
	return 8;
  else if (strcmp(name, "b")==0)
	return 9;
  else if (strcmp(name, "c")==0)
	return 10;
  else if (strcmp(name, "d")==0)
	return 11;
  else if (strcmp(name, "g")==0)
	return 12;
  else if (strcmp(name, "lam")==0)
	return 13;
  else if (strcmp(name, "r")==0)
	return 14;
  else if (strcmp(name, "s")==0)
	return 15;
  else if (strcmp(name, "thet")==0)
	return 16;
  else if (strcmp(name, "xR")==0)
	return 17;
  else {
	fprintf(stderr, "Invalid name %s for getindex call\n", name);
	return 0.0/0.0;
	}
}


int heav(double x_, double *p_, double *wk_, double *xv_) {
  if (x_>0.0) {return 1;} else {return 0;}
}

void auxvars(unsigned n_, unsigned np_, double t, double *Y_, double *p_, double *f_, unsigned wkn_, double *wk_, unsigned xvn_, double *xv_){


}


void massMatrix(unsigned n_, unsigned np_, double t, double *Y_, double *p_, double **f_, unsigned wkn_, double *wk_, unsigned xvn_, double *xv_) {
}

void jacobian(unsigned n_, unsigned np_, double t, double *Y_, double *p_, double **f_, unsigned wkn_, double *wk_, unsigned xvn_, double *xv_) {
}

void jacobianParam(unsigned n_, unsigned np_, double t, double *Y_, double *p_, double **f_, unsigned wkn_, double *wk_, unsigned xvn_, double *xv_) {
}
