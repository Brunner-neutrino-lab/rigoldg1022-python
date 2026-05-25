# Rigol DG1022 Programming Guide (Extracted)

Generated from DG1022_ProgrammingGuide_EN.pdf via PyMuPDF.

Page numbers refer to the original PDF.


## Table of Contents

- p.7: Programming Overview
  - p.8: Communication Interfaces
  - p.9: Commands Introduction
    - p.9: Commands Format
    - p.10: Symbol Instruction
    - p.11: Parameter Types
    - p.12: Commands Abbreviation
- p.13: DG1022 Commands System
  - p.14: IEEE 488.2
  - p.15: APPLy
  - p.22: FUNCtion
  - p.28: FREQuency
  - p.32: VOLTage
  - p.38: OUTPut
  - p.43: PULSe
  - p.47: AM
  - p.50: FM
  - p.53: PM
  - p.56: FSKey
  - p.59: SWEep
  - p.62: TRIGger
  - p.65: BURSt
  - p.69: DATA
  - p.73: MEMory
  - p.76: SYSTem
  - p.79: PHASe
  - p.81: DISPlay
  - p.82: COUPling
- p.85: Application Examples
  - p.86: Example 1: To Generate a Sine Wave
  - p.87: Example 2: To Generate a Built-in Arbitrary Wave
  - p.88: Example 3: To Generate an User-defined Arbitrary Wave
  - p.90: Example 4: To Generate a FSK Wave
  - p.91: Example 5: To Generate a Linear Sweep Wave
  - p.92: Example 6: To Generate a Burst Wave
  - p.93: Example 7: To Output Waves via Dual Channels
  - p.94: Example 8: Channel Coupling
  - p.95: Example 9: Channel Copy
- p.97: Appendix: Commands Reference A-Z

---


<!-- page 1 -->

 
 
RIGOL 
Programming Guide 
 
 
 
 
 
 
 
 
 
 
 
    DG1022 Function/Arbitrary  
           Waveform Generator 
    
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
August 2009 
RIGOL Technologies, Inc. 


<!-- page 2 -->



<!-- page 3 -->

RIGOL 
 
Programming Guide for DG1022 
I
Copyright  
© 2009 RIGOL Technologies, Inc. All Rights Reserved. 
 
Trademark Information 
RIGOL is registered trademark of RIGOL Technologies, Inc. 
 
Notices 
 
RIGOL products are protected by patent law in and outside of P.R. China. 
 
RIGOL Technologies, Inc. reserves the right to modify or change part of or all 
the specifications and pricing policies at company’s sole decision. 
 
Information in this publication replaces all previously corresponding material. 
 
RIGOL shall not be liable for losses caused no matter by incidental or by 
consequential in connection with the furnishing, use or performance of this 
manual as well as any information contained.  
 
Any part of this document is forbidden to copy, photocopy or rearrange without 
the express written approval of RIGOL.  
 
Product Certification 
RIGOL guarantees this product conforms to the standards of national and industrial. 
Meanwhile, the related standards conform to other ISO will get further. At present, 
DG1022 has passed CE, GOST and cTUVus certification.


<!-- page 4 -->

RIGOL 
                                                                                
 Programming Guide for DG1022 
II 
Structure of this Document 
 
Chapter 1  Programming Overview  
This chapter introduces you how to programme DG1022 generator using commands 
and how to input the commands in right format. 
 
Chapter 2  DG1022 Commands System 
This chapter gives detailed information on each command supported by DG1022, 
including command format, function description, considerations when using command 
as well as some application examples.   
 
Chapter 3  Application Examples 
This chapter shows you how to realize the examples in《DG1022 User’s Guide》via 
command lines. 
 
Appendix: Commands Reference A-Z 
The Appendix lists all the commands alphabetically in favor of quick reference. 
 
 
 
 
 


<!-- page 5 -->

                                                                         RIGOL 
 Programming Guide for DG1022 
III
Table of Contents 
Chapter 1 Programming Overview ........................................................... 1-1 
Communication Interfaces.......................................................................... 1-2 
Commands Introduction ............................................................................. 1-3 
Commands Format .............................................................................. 1-3 
Symbol Instruction .............................................................................. 1-4 
Parameter Types ................................................................................. 1-5 
Commands Abbreviation ...................................................................... 1-6 
Chapter 2 DG1022 Commands System .................................................... 2-1 
IEEE 488.2 ................................................................................................ 2-2 
APPLy ....................................................................................................... 2-3 
FUNCtion ................................................................................................ 2-10 
FREQuency ............................................................................................. 2-16 
VOLTage ................................................................................................. 2-20 
OUTPut .................................................................................................. 2-26 
PULSe .................................................................................................... 2-31 
AM ......................................................................................................... 2-35 
FM ......................................................................................................... 2-38 
PM ......................................................................................................... 2-41 
FSKey ..................................................................................................... 2-44 
SWEep ................................................................................................... 2-47 
TRIGger ................................................................................................. 2-50 
BURSt .................................................................................................... 2-53 
DATA ...................................................................................................... 2-57 
MEMory .................................................................................................. 2-61 
SYSTem .................................................................................................. 2-64 
PHASe .................................................................................................... 2-67 
DISPlay .................................................................................................. 2-69 
COUPling ................................................................................................ 2-70 
Chapter 3 Application Examples .............................................................. 3-1 
Example 1: To Generate a Sine Wave .......................................................... 3-2 
Example 2: To Generate a Built-in Arbitrary Wave ........................................ 3-3 
Example 3: To Generate an User-defined Arbitrary Wave .............................. 3-4 
Example 4: To Generate a FSK Wave .......................................................... 3-6 
Example 5: To Generate a Linear Sweep Wave ............................................ 3-7 


<!-- page 6 -->

RIGOL 
                                                                                
 Programming Guide for DG1022 
IV 
Example 6: To Generate a Burst Wave ........................................................ 3-8 
Example 7: To Output Waves via Dual Channels .......................................... 3-9 
Example 8: Channel Coupling ................................................................... 3-10 
Example 9: Channel Copy ........................................................................ 3-11 
Appendix: Commands Reference A-Z .......................................................... 1 
 


## Programming Overview  *(p.7)*


<!-- page 7 -->

Programming Overview                                                            RIGOL             
 
Programming Guide for DG1022 
1-1 
Chapter 1 Programming Overview 
 
This chapter introduces you how to programme DG1022 generator using commands 
and how to input commands in right format. 
 
This chapter contains the following sections: 
 
Communication Interfaces 
 
Commands Introduction 
Commands Format 
Symbol Instruction 
Parameter Types 
Commands Abbreviation 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 


### Communication Interfaces  *(p.8)*


<!-- page 8 -->

RIGOL                                                           Programming Overview                   
                                                                                
 Programming Guide for DG1022 
1-2 
Communication Interfaces 
Computers communicate with the generator by sending and receiving messages over 
an USB interface. Command word is sended and identified in the form of ASCII 
character strings for users to easily control and do user-defined development. 
 
Operations that you can do with a computer and a generator include: 
 
Set the generator. 
 
Output waveforms from the generator. 
 
Connection: 
Please connect the USB Device port of DG1022 with the corresponding USB interface 
on the computer using an USB cable. 
 
 
 


### Commands Introduction  *(p.9)*


#### Commands Format  *(p.9)*


<!-- page 9 -->

Programming Overview                                                            RIGOL 
Programming Guide for DG1022 
1-3 
Commands Introduction 
Commands Format 
The commands system of DG1022 is a tree structure, and each of sub-system is 
consists of a “root” keyword and multilayered keywords. The keywords are separated 
by “:” and aoptional parameters are permitted to follow; “?” appeared following a 
command line denotes to query this function; besides, “space” is used to divide 
command and parameter.    
 
For example: 
FUNCtion:SQUare:DCYCle {<percent>|MINimum|MAXimum} 
FUNCtion:SQUare:DCYCle? [MINimum|MAXimum] 
 
FUNCtion is the root keyword of a commmand line, SQUare and DCYCle is the 
second and third keyword, all of them are separated by “:”. <percent> denotes the 
parameters permitted to be set by user; “?” denotes to query; the command 
FUNCtion:SQUare:DCYCle and parameter are separated by “space”. 
 
 “,” is usually used to compart multiple parameters existed in one command, for 
example: 
DATA VOLATILE,<value>,<value>, . . . 
 
 


#### Symbol Instruction  *(p.10)*


<!-- page 10 -->

RIGOL                                                           Programming Overview                   
                                                                                
 Programming Guide for DG1022 
1-4 
Symbol Instruction 
Following symbols are not included in commands, but whichi are usually used to assist 
to explain the parameters containd in a command line. 
1. Braces { } 
The parameters or contents enclosed in a { } are reqired. Only one content or 
parameter could be selected every time, and all the options are separated by “|”.  
For example: {ON|OFF} indicateds that ON or OFF can be selected.   
 
2. Square brackets [ ] 
Some keywords or contents are enclosed by square bracket [ ], which indicates 
that those parameters are optional and will be execute no matter whether been 
ignored or not.  
For example:  
DATA:COPY <destination arb name>[,VOLATILE] 
This command copys the wave from volatile memory to the specified nonvolatile 
memory. Note: [,VOLATILE] may be ignored. 
 
3. Triangle Brackets < > 
An item enclosed in < > should be replaced by an effective value. 
For example: 
DISPlay:CONTRAST <value> 
Note: <value> must be a numerical value, such as: 
DISPlay:CONTRAST 25 
 
 


#### Parameter Types  *(p.11)*


<!-- page 11 -->

Programming Overview                                                            RIGOL 
Programming Guide for DG1022 
1-5 
Parameter Types 
The commands contain 5 kinds of parameters, different parameters have different 
setting methods.  
1. Boolean Parameters 
The parameters could be “OFF”, “ON” or “0”, “1”, for example: 
AM:STATE {OFF|ON} 
“OFF” denotes disable AM function. “On” denotes enable. 
 
2. Consecutive Integer Parameters  
The parameters could be a consecutive integer, for example: 
DISPlay:CONTRAST <value> 
<value> could be an integer between 0 and 31(including 0 and 31).  
 
3. Consecutive Real Number Parameters 
The parameters could be any value only in effective range and precision 
permitted, for example: 
FREQuency {<frequency>|MINimum|MAXimum} 
As a sine wave, <frequency> should be any real number between 1uHz~20MHz. 
 
4. Discrete Parameters 
The parameters could be a cited value, for example, 
MEMory:STATe:NAME? {0|1|2|3|4|5|6|7|8|9|10} 
The parameter could only be 0, 1, 2, 3, 4, 5, 6. 7, 8, 9, 10. 
 
5. ASCII Character String 
The parameters should be composed of ASCII character string, for example,   
DATA:COPY <destination arb name>[,VOLATILE] 
<destination arb name> is a character string defined by user.  
 


#### Commands Abbreviation  *(p.12)*


<!-- page 12 -->

RIGOL                                                           Programming Overview                   
                                                                                
 Programming Guide for DG1022 
1-6 
Commands Abbreviation 
All the comands are case-insensitive, so you can use any kind of them. But if use 
abbreviation, the capital letters specified in commands must be written completely. 
For example: 
FUNCtion:SQUare:DCYCle? also can be: 
FUNC:SQU:DCYC? or func:squ:dcyc? 


## DG1022 Commands System  *(p.13)*


<!-- page 13 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-1 
Chapter 2 DG1022 Commands System 
 
This chapter gives detailed information on each command supported by DG1022, 
including command format, function description, using considerations as well as some 
application examples. 
DG1022 contains following subcommands systems: 
 
IEEE 488.2 
 
APPLy 
 
FUNCtion 
 
FREQuency  
 
VOLTage 
 
OUTPut 
 
PULSe 
 
AM 
 
FM 
 
PM 
 
FSKey  
 
SWEep 
 
TRIGger 
 
BURSt 
 
DATA 
 
MEMory 
 
SYSTem 
 
PHASe 
 
DISPlay 
 
COUPling 


### IEEE 488.2  *(p.14)*


<!-- page 14 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-2 
IEEE 488.2 
IEEE standard has some common commands for querying some basic information 
about instrument or executing, which usually begins with “*” and holds 3-character 
long command keyword.  
DG1022 supports following IEEE488.2 commands: 
1. 
*IDN? 
 
1. *IDN? 
Command Format 
*IDN? 
Function 
Query ID character string of instrument, including a field 
separated by 4 “,”, manufactory, model, serial number and the 
edition number that consists of numbers and separated by 
“.” .  
Return Format 
RIGOL TECHNOLOGIES,DG1022,DG1000000002, 
00.01.00.04.00 


### APPLy  *(p.15)*


<!-- page 15 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-3 
APPLy 
APPLy commands provide the most straightforward method to program the 
generator over remote interface. Among following commands, the instrument could 
set and output waveforms if OUTPUT function is enable. 
DG1022 supports following APPLy commands: 
1. 
APPLy:SINusoid 
2. 
APPLy:SQUare 
3. 
APPLy:RAMP 
4. 
APPLy:PULSe 
5. 
APPLy:NOISe 
6. 
APPLy:DC 
7. 
APPLy:USER 
8. 
APPLy? 
9. 
APPLy:SINusoid:CH2 
10. APPLy:SQUare:CH2 
11. APPLy:RAMP:CH2 
12. APPLy:PULSe:CH2 
13. APPLy:NOISe:CH2 
14. APPLy:DC:CH2 
15. APPLy:USER:CH2 
16. APPLy:CH2? 
 


<!-- page 16 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-4 
The detailed information of each command are: 
 
1. APPLy:SINusoid 
Command 
Format 
APPLy:SINusoid [<frequency>[,<amplitude>[,<offset>]]] 
Function 
Generate a sine wave with specific frequency, amplitude and DC 
offset via CH1.  
Explanations  
If the parameters you set are less than three, the sequence 
would be: <frequency>, <amplitude>, <offset>.  
 
The default units of <frequency>, <amplitude>, <offset> are: 
Hz, Vpp, VDC. 
Example 
APPL:SIN 1000,5.0,-1.5 
 
2. APPLy:SQUare 
Command 
Format 
APPLy:SQUare [<frequency>[,<amplitude>[,<offset>]]] 
Function 
Generate a square wave with specific frequency, amplitude and DC 
offset via CH1 and cover the current duty cycle settings and select 
50% automaticly.  
Explanations  
If the parameters you set are less than three, the sequence 
would be: <frequency>, <amplitude>, <offset>.  
 
The default units of <frequency>, <amplitude>, <offset> are: 
Hz, Vpp, VDC. 
Example 
APPL:SQU 1000,5.0,-1.5 
 
3. APPLy:RAMP 
Command 
Format 
APPLy:RAMP [<frequency>[,<amplitude>[,<offset>]]] 
Function 
Generate a ramp wave with specific frequency, amplitude and DC 
offset via CH1 and cover the current symmetry settings and select 
50% automaticly. 
Explanations  
If the parameters you set are less than three, the sequence 
would be: <frequency>, <amplitude>, <offset>.  
 
The default units of <frequency>, <amplitude>, <offset> are: 
Hz, Vpp, VDC. 
Example 
APPL:RAMP 1000,5.0,-1.5 
 


<!-- page 17 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-5 
4. APPLy:PULSe 
Command 
Format 
APPLy:PULSe [<frequency>[,<amplitude>[,<offset>]]] 
Function 
Generate a pulse wave with specific frequency, amplitude and DC 
offset via CH1.  
Explanations  
If the parameters you set are less than three, the sequence 
would be: <frequency>, <amplitude>, <offset>.  
 
The default units of <frequency>, <amplitude>, <offset> are: 
Hz, Vpp, VDC. 
Example 
APPL:PULS 1000,5.0,-1.5 
 
5. APPLy:NOISe 
Command 
Format 
APPLy:NOISe [<frequency |DEFault>[,<amplitude>[,<offset>]]] 
Function  
Generate Gaussian noise with specific amplitude and DC offset.  
Explanations  
Although the frequency parameter made no impression on this 
command, a value or “DEFault” must be specified. (noise 
function has 5MHz of bandwidth) 
 
If the parameters you set are less than three, the sequence 
would be: <frequency>, <amplitude>, <offset>.  
 
The default units of <frequency>, <amplitude>, <offset> are: 
Hz, Vpp, VDC.  
Example 
APPL:NOIS DEF,5.0,2.0 
 
6. APPLy:DC 
Command 
Format 
APPLy:DC [<frequency|DEFault>[,<amplitude>|DEFault>[,< 
offset>]]]  
Function  
Generate a DC with electrical level specified by < offset > parameter 
via CH1.  
Explanations  
Although the frequency and amplitude parameter made no 
impression on this command, a value or “DEFault” must be 
specified. 
 
If the parameters you set are less than three, the sequence 
would be: <frequency>, <amplitude>, <offset>.  
 
The default units of <frequency>, <amplitude>, <offset> are: 
Hz, Vpp, VDC. 
Example 
APPL:DC DEF,DEF,-2.5 


<!-- page 18 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-6 
 
7. APPLy:USER 
Command 
Format 
APPLy:USER [<frequency>[,<amplitude>[,<offset>]]] 
Function  
Generate an arbitrary wave selected by FUNCtion:USER command 
with specific frequency, amplitude and DC offset.   
Explanations  
If the parameters you set are less than three, the sequence 
would be: <frequency>, <amplitude>, <offset>.  
 
The default units of <frequency>, <amplitude>, <offset> are: 
Hz, Vpp, VDC. 
Example 
APPL:USER 1000,5.0,-1.5 
 
8. APPLy? 
Command 
Format 
APPLy? 
Function  
Query the current configuration of CH1 and the type of waves 
outputted. 
Explanations The query returns a character string with double quotation marks, 
including function, frequency, amplitude and offset.  
Example 
CH1:"SIN,1.000000e+03,5.000000e+00,-1.500000e+00" 
 
9. APPLy:SINusoid:CH2 
Command 
Format 
APPLy:SINusoid:CH2 [<frequency>[,<amplitude>[,<offset>]]] 
Function  
Generate a sine wave with specific frequency, amplitude and DC 
offset via CH2.  
Explanations  
If the parameters you set are less than three, the sequence 
would be: <frequency>, <amplitude>, <offset>.  
 
The default units of <frequency>, <amplitude>, <offset> are: 
Hz, Vpp, VDC. 
Example 
APPL:SIN:CH2 1000,5.0,-1 
 
10. APPLy:SQUare:CH2 
Command 
Format 
APPLy:SQUare:CH2 [<frequency>[,<amplitude>[,<offset>]]] 
Function  
Generate a square wave with specific frequency, amplitude and DC 
offset via CH2 and cover the current duty cycle settings and select 


<!-- page 19 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-7 
50% automaticly.  
Explanations  
If the parameters you set are less than three, the sequence 
would be: <frequency>, <amplitude>, <offset>.  
 
The default units of <frequency>, <amplitude>, <offset> are: 
Hz, Vpp, VDC. 
Example 
APPL:SQU:CH2 1000,5.0,-1 
 
11. APPLy:RAMP:CH2 
Command 
Format 
APPLy:RAMP:CH2 [<frequency>[,<amplitude>[,<offset>]]] 
Function  
Generate a ramp wave with specific frequency, amplitude and DC 
offset via CH2 and cover the current symmetry settings and select 
50% automaticly.  
Explanations  
If the parameters you set are less than three, the sequence 
would be: <frequency>, <amplitude>, <offset>.  
 
The default units of <frequency>, <amplitude>, <offset> are: 
Hz, Vpp, VDC. 
Example 
APPL:RAMP:CH2 1000,5.0,0.5 
 
12. APPLy:PULSe:CH2 
Command 
Format 
APPLy:PULSe:CH2 [<frequency>[,<amplitude>[,<offset>]]] 
Function  
Generate a pulse wave with specific frequency, amplitude and DC 
offset via CH2.  
Explanations  
If the parameters you set are less than three, the sequence 
would be: <frequency>, <amplitude>, <offset>.  
 
The default units of <frequency>, <amplitude>, <offset> are: 
Hz, Vpp, VDC. 
Example 
APPL:PULS:CH2 1000,5.0,0.5 
 
13. APPLy:NOISe:CH2 
Command 
Format 
APPLy:NOISe:CH2[<frequency|DEFault>[,<amplitude>[,<offset>]]] 
Function 
Generate Gaussian noise with specific amplitude and DC offset via 
CH2. 
Explanations  
Although the frequency parameter made no impression on this 
command, a value or “DEFault” must be specified. (noise 


<!-- page 20 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-8 
function has 5MHz of bandwidth) 
 
If the parameters you set are less than three, the sequence 
would be: <frequency>, <amplitude>, <offset>.  
 
The default units of <frequency>, <amplitude>, <offset> are: 
Hz, Vpp, VDC. 
Example 
APPL:NOIS:CH2 DEF, 5.0, 0.5 
 
14. APPLy:DC:CH2 
Command 
Format 
APPLy:DC:CH2[<frequency|DEFault>[,<amplitude>|DEFault>[,< 
offset>]]] 
Function  
Generate a DC with electrical level specified by <offset> parameter 
via CH2. 
Explanations  
Although the frequency and amplitude parameter made no 
impression on this command, a value or “DEFault” must be 
specified. 
 
If the parameters you set are less than three, the sequence 
would be: <frequency>, <amplitude>, <offset>.  
 
The default units of <frequency>, <amplitude>, <offset> are: 
Hz, Vpp, VDC. 
Example 
APPL:DC:CH2 DEF,DEF,1.5 
 
15. APPLy:USER:CH2 
Command 
Format 
APPLy:USER:CH2 [<frequency>[,<amplitude>[,<offset>]]] 
Function  
Generate an arbitrary wave selected by FUNCtion:USER:CH2 
command with specific frequency, amplitude and DC offset. 
Explanations  
If the parameters you set are less than three, the sequence 
would be: <frequency>, <amplitude>, <offset>.  
 
The default units of <frequency>, <amplitude>, <offset> are: 
Hz, Vpp, VDC. 
Example 
APPL:USER:CH2 1000,5.0,-1.5 
 
16. APPLy:CH2? 
Command 
Format 
APPLy:CH2? 
Function  
Query the current configuration of CH2 and the type of waves 
outputted. 


<!-- page 21 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-9 
Explanations The query returns a character string with double quotation marks, 
including function, frequency, amplitude and offset. 
Example 
CH2:"SIN,1.000000e+03,5.000000e+00,-1.500000e+00" 
 
 
 
 


### FUNCtion  *(p.22)*


<!-- page 22 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-10 
FUNCtion 
FUNCtion commands are used for setting the output function and their parameters; 
selecting carrier wave function in modulation mode; choosing any one from 48 built-in 
arbitrary waveforms and 10 user-defined waveforms, or the waveform downloaded to 
volatile memory currently. 
DG1022 supports following FUNCtion commands:  
1. 
FUNCtion 
2. 
FUNCtion? 
3. 
FUNCtion:USER 
4. 
FUNCtion:USER? 
5. 
FUNCtion:SQUare:DCYCle 
6. 
FUNCtion:SQUare:DCYCle? 
7. 
FUNCtion:RAMP:SYMMetry 
8. 
FUNCtion:RAMP:SYMMetry? 
9. 
FUNCtion:CH2 
10. FUNCtion:CH2? 
11. FUNCtion:USER:CH2 
12. FUNCtion:USER:CH2? 
13. FUNCtion:SQUare:DCYCle:CH2 
14. FUNCtion:SQUare:DCYCle:CH2? 
15. FUNCtion:RAMP:SYMMetry:CH2 
16. FUNCtion:RAMP:SYMMetry:CH2? 
 


<!-- page 23 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-11
The detailed information of each command are: 
 
1. FUNCtion 
Command 
Format 
FUNCtion {SINusoid|SQUare|RAMP|PULSe|NOISe|DC|USER} 
Function 
Select the output function for CH1.  
Explanations If send FUNC DC and then FUNC USER, the output is still DC. 
Example 
FUNC SIN 
 
2. FUNCtion? 
Command 
Format 
FUNCtion? 
Function 
Query the output function from CH1. 
Explanations The query always returns CH1:ARB after sending FUNC DC or FUNC 
USER. 
Example 
The query returns CH1:SIN, CH1:SQU, CH1:RAMP, CH1:PULS, 
CH1:NOIS or CH1:ARB, the default is CH1:SIN. 
 
3. FUNCtion:USER 
Command 
Format 
FUNCtion:USER {<name of arbitrary wave>|VOLATILE} 
Function 
Separately select any one wave from built-in arbitrary waves and 10 
user-defined waves for CH1 or select the wave that has been 
downloaded into volatile memory.  
Explanations  
The built-in waves contains: 
Common: 
NegRamp/AttALT/AmpALT/StairDown/StairUp/StairUD/Cpulse/ 
PPulse/NPulse/Trapezia/RoundHalf/AbsSine/AbsSineHalf/ 
SINE_TRA/SINE_VER 
Math: 
Exp_Rise/Exp_Fall/Tan/Cot/Sqrt/X
∧2/Sinc/Gauss/HaverSine/ 
Lorentz/Dirichlet/GaussPulse/Airy 
Project: 
Cardiac/Quake/Gamma/Voice/TV/Combin/BandLimited/ 
Stepresponse/Butterworth/Chebyshev1/ Chebyshev2 
Window Function: 
Boxcar/Barlett/triang/Blackman/Hamming/Hanning/Kaiser 


<!-- page 24 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-12 
Others: 
Roundpm/DC 
 
Send FUNC DC command when use DC.  
 
Abbreviation is invalid. 
Example 
FUNC:USER VOLATILE 
 
4. FUNCtion:USER? 
Command 
Format 
FUNCtion:USER? 
Function 
Query the name of arbitrary wave generated from CH1.  
Return 
Value 
The query returns the name of built-in arbitrary wave that has been 
selected. (such as EXP_RISE), VOLATILE or returns any name of 
user-defined wave in nonvolatile memory. The default is EXP_RISE. 
 
5. FUNCtion:SQUare:DCYCle 
Command 
Format 
FUNCtion:SQUare:DCYCle {<percent>|MINimum|MAXimum} 
Function 
Set the duty cycle of square wave for CH1.  
Explanations <percent> is the percent of duty cycle selected, MIN is the 
minimum duty cycle and MAX is the maximum.  
Example 
FUNC:SQU:DCYC 50 
 
6. FUNCtion:SQUare:DCYCle? 
Command 
Format 
FUNCtion:SQUare:DCYCle? [MINimum|MAXimum] 
Function 
Query the duty cycle of square wave from CH1. 
Return 
Value 
The query returns current duty cycle settings with the format of 
percent, such as 50.000000.  
 
7. FUNCtion:RAMP:SYMMetry 
Command 
Format 
FUNCtion:RAMP:SYMMetry {<percent>|MINimum|MAXimum} 
Function 
Set the symmetry of ramp wave for CH1.  
Explanations <percent> is the selected percent of symmetry; MIN＝0％, MAX＝
100％. 
Example 
FUNC:RAMP:SYMM 50 
 


<!-- page 25 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-13
8. FUNCtion:RAMP:SYMMetry? 
Command 
Format 
FUNCtion:RAMP:SYMMetry? [MINimum|MAXimum] 
Function 
Query the symmetry of ramp wave from CH1. 
Return 
Value 
The query returns current symmetry settings with the format of 
percent, such as 50.000000. 
 
9. FUNCtion:CH2 
Command 
Format 
FUNCtion:CH2 {SINusoid|SQUare|RAMP|PULSe|NOISe|DC|USER} 
Function 
Select the output function form CH2.  
Explanations If send FUNC:CH2 DC and then FUNC:CH2 USER, the output is 
still DC. 
Example 
FUNC:CH2 SIN 
 
10. FUNCtion:CH2? 
Command 
Format 
FUNCtion:CH2? 
Function 
Query the output function from CH2. 
Explanations The query always returns CH2:ARB after sending FUNC:CH2 DC or 
FUNC:CH2 USER.  
Example 
The query returns CH2:SIN, CH2:SQU, CH2:RAMP, CH2:PULS, 
CH2:NOIS or CH2:ARB, the default is CH2:SIN. 
 
11. FUNCtion:USER:CH2 
Command 
Format 
FUNCtion:USER:CH2 {< name of arbitrary wave >|VOLATILE} 
Function 
Separately select any one wave from built-in arbitrary waves and 10 
user-defined waves for CH2 or select the wave that has been 
loaded into volatile memory. 
Explanations  
The built-in waves contains: 
Common: 
NegRamp/AttALT/AmpALT/StairDown/StairUp/StairUD/Cpulse/ 
PPulse/NPulse/Trapezia/RoundHalf/AbsSine/AbsSineHalf/ 
SINE_TRA/SINE_VER 
Math: 
Exp_Rise/Exp_Fall/Tan/Cot/Sqrt/X
∧2/Sinc/Gauss/HaverSine/ 


<!-- page 26 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-14 
Lorentz/Dirichlet/GaussPulse/Airy 
Project: 
Cardiac/Quake/Gamma/Voice/TV/Combin/BandLimited/ 
Stepresponse/Butterworth/Chebyshev1/ Chebyshev2 
Window Function: 
Boxcar/Barlett/triang/Blackman/Hamming/Hanning/Kaiser 
Others: 
Roundpm/DC 
 
Send FUNC:CH2 DC command when use DC.  
 
Abbreviation is invalid. 
Example 
FUNC:USER:CH2 SINC 
 
12. FUNCtion:USER:CH2? 
Command 
Format 
FUNCtion:USER:CH2? 
Function 
Query the name of arbitrary wave generated from CH2. 
Return 
Value 
The query returns the name of built-in arbitrary wave that has been 
selected. (such as EXP_RISE), VOLATILE or returns any name of 
user-defined wave in nonvolatile memory. The default is EXP_RISE. 
 
13. FUNCtion:SQUare:DCYCle:CH2 
Command 
Format 
FUNCtion:SQUare:DCYCle:CH2 {<percent>|MINimum|MAXimum} 
Function 
Set the duty cycle of square wave for CH2. 
Explanations <percent> is the selected percent of duty cycle, MIN is the 
minimum duty cycle and MAX is the maximum. 
Example 
FUNC:SQU:DCYC:CH2 50 
 
14. FUNCtion:SQUare:DCYCle:CH2? 
Command 
Format 
FUNCtion:SQUare:DCYCle:CH2? [MINimum | MAXimum] 
Function 
Query the duty cycle of square wave from CH2. 
Return 
Value 
The query returns current duty cycle settings with the format of 
percent, such as 50.000000. 
 
15. FUNCtion:RAMP:SYMMetry:CH2 
Command 
FUNCtion:RAMP:SYMMetry:CH2 {<percent>|MINimum|MAXimum} 


<!-- page 27 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-15
Format 
Function 
Set the symmetry of ramp wave for CH2.  
Explanations <percent> is the selected percent of symmetry; MIN＝0％, MAX＝
100％. 
Example 
FUNC:RAMP:SYMM:CH2 50 
 
16. FUNCtion:RAMP:SYMMetry:CH2? 
Command 
Format 
FUNCtion:RAMP:SYMMetry:CH2? [MINimum|MAXimum] 
Function 
Query the symmetry of ramp wave from CH2. 
Return 
Value 
The query returns current symmetry settings with the format of 
percent, such as 50.000000. 
 


### FREQuency  *(p.28)*


<!-- page 28 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-16 
FREQuency 
FREQuency commands are used for setting: the frequency of output function from 
dual channels; the start/stop frequency, the center/span frequency in sweep mode, 
the carrier frequency in modulation. Sweep and modulation are only valid for CH1.  
DG1022 supports following FREQuency commands:  
1. 
FREQuency 
2. 
FREQuency? 
3. 
FREQuency:CH2 
4. 
FREQuency:CH2? 
5. 
FREQuency:STARt 
6. 
FREQuency:STARt? 
7. 
FREQuency:STOP 
8. 
FREQuency:STOP? 
9. 
FREQuency:CENTer 
10. FREQuency:CENTer? 
11. FREQuency:SPAN 
12. FREQuency:SPAN? 
 


<!-- page 29 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-17
The detailed information of each command are: 
 
1. FREQuency 
Command 
Format 
FREQuency {<frequency>|MINimum|MAXimum} 
Function 
Set the frequency of output function for CH1.  
Explanations 
<frequency> is the frequency value set by user, the default unit is 
Hz. MIN is the minimum frequency permitted by specified function, 
MAX is the maxmum. 
Example 
FREQ MIN 
 
2. FREQuency? 
Command 
Format 
FREQuency? [MINimum|MAXimum] 
Function 
Query the frequency of output function from CH1.  
Return Value 
The query returns the frequency value that has been set in the 
form of scientific notation in Hz, such as: 1.000000e-06. 
 
3. FREQuency:CH2 
Command 
Format 
FREQuency:CH2 {<frequency>|MINimum|MAXimum} 
Function 
Set the frequency of output function for CH2. 
Explanations 
<frequency> is the frequency value set by user, the default unit is 
Hz. MIN is the minimum frequency permitted by specified function, 
MAX is the maxmum.  
Example 
FREQ:CH2 MIN 
 
4. FREQuency:CH2? 
Command 
Format 
FREQuency:CH2? [MINimum|MAXimum] 
Function 
Query the frequency of output function from CH2. 
Return Value 
The query returns the frequency value that has been set in the 
form of scientific notation in Hz, such as: CH2:1.000000e-06. 
 
5. FREQuency:STARt 
Command 
Format 
FREQuency:STARt {<frequency>|MINimum|MAXimum} 


<!-- page 30 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-18 
Function 
Set the start frequency (used in conjunction with the stop 
frequency) in sweep mode. 
Example 
FREQ:STAR MIN 
 
6. FREQuency:STARt? 
Command 
Format 
FREQuency:STARt? [MINimum|MAXimum] 
Function 
Query the start frequency in sweep mode. 
Return Value 
The query returns the start frequency that has been set in the form 
of scientific notation in Hz, such as: 1.000000e-06. 
 
7. FREQuency:STOP 
Command 
Format 
FREQuency:STOP {<frequency>|MINimum|MAXimum} 
Function 
Set the stop frequency (used in conjunction with start frequency) 
in sweep mode. 
Example 
FREQ:STOP MAX 
 
8. FREQuency:STOP? 
Command 
Format 
FREQuency:STOP? [MINimum|MAXimum] 
Function 
Query the stop frequency in sweep mode.  
Return Value 
The query returns the stop frequency that has been set in the form 
of scientific notation in Hz, such as: 2.000000e+07. 
 
9. FREQuency:CENTer 
Command 
Format 
FREQuency:CENTer {<frequency>|MINimum|MAXimum} 
Function 
Set the center frequency (used in conjunction with span 
frequency) in sweep mode.  
Example 
FREQ:CENT 10000000 
 
10. FREQuency:CENTer? 
Command 
Format 
FREQuency:CENTer? [MINimum|MAXimum] 
Function 
Query the center frequency in sweep mode. 
Return Value 
The query returns the center frequency that has been set in the 


<!-- page 31 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-19
form of scientific notation in Hz, such as: 1.000000e+07. 
 
11. FREQuency:SPAN 
Command 
Format 
FREQuency:SPAN {<frequency>|MINimum|MAXimum} 
Function 
Set the span frequency (used in conjunction with center 
frequency) in sweep mode.  
Example 
FREQ:SPAN MAX 
 
12. FREQuency:SPAN? 
Command 
Format 
FREQuency:SPAN? [MINimum|MAXimum] 
Function 
Query the span frequency in sweep mode.  
Return Value 
The query returns the span frequency that has been set in the 
form of scientific notation in Hz, such as: 2.000000e+07. 


### VOLTage  *(p.32)*


<!-- page 32 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-20 
VOLTage 
VOLTage commands are used for setting the voltage amplitude, offset, high level, 
low level, or setting the voltage unit for each channel. 
DG1022 supports following VOLTage commands: 
1. 
VOLTage 
2. 
VOLTage? 
3. 
VOLTage:HIGH 
4. 
VOLTage:HIGH? 
5. 
VOLTage:LOW 
6. 
VOLTage:LOW? 
7. 
VOLTage:OFFSet 
8. 
VOLTage:OFFSet? 
9. 
VOLTage:UNIT 
10. VOLTage:UNIT? 
11. VOLTage:CH2 
12. VOLTage:CH2? 
13. VOLTage:HIGH:CH2 
14. VOLTage:HIGH:CH2? 
15. VOLTage:LOW:CH2 
16. VOLTage:LOW:CH2? 
17. VOLTage:OFFSet:CH2 
18. VOLTage:OFFSet:CH2? 
19. VOLTage:UNIT:CH2 
20. VOLTage:UNIT:CH2? 
 


<!-- page 33 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-21
The detailed information of each command are: 
 
1. VOLTage 
Command 
Format 
VOLTage {<amplitude>|MINimum|MAXimum} 
Function 
Set the amplitude from CH1 in Vpp.  
Explanations 
MIN selects the minimum amplitude. MAX selects the maximum 
amplitude for the selected function. 
Unit 
VPP, VRMS or DBM. Note that DBM could be used only in non-high 
resistance. The unit of voltage could be changed via sending 
VOLTage:UNIT. 
Example 
VOLT MIN 
 
2. VOLTage? 
Command 
Format 
VOLTage? 
Function 
Query the amplitude from CH1.  
Return Value 
The query returns the amplitude that has been set in the form of 
scientific notation such as: 4.000000e-03. 
 
3. VOLTage:HIGH 
Command 
Format 
VOLTage:HIGH {<voltage>|MINimum|MAXimum} 
Function 
Set the high level of waves from CH1 in V. 
Explanations 
<voltage>is the high level for user to set. MIN selects the 
minimum high level. MAX selects the maximum high level.  
Example 
VOLT:HIGH MAX 
 
4. VOLTage:HIGH? 
Command 
Format 
VOLTage:HIGH? 
Function 
Query the high level of waves from CH1.  
Return Value 
The query returns the high level that has been set in the form of 
scientific notation such as: 1.000000e+01. 
 
5. VOLTage:LOW 
Command 
VOLTage:LOW {<voltage>|MINimum|MAXimum} 


<!-- page 34 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-22 
Format 
Function 
Set the low level of waves from CH1 in V.  
Explanations 
<voltage>is the low level for user to set. MIN selects the minimum 
low level. MAX selects the maximum low level. 
Example 
VOLT:LOW MIN 
 
6. VOLTage:LOW? 
Command 
Format 
VOLTage:LOW? 
Function 
Query the low level of waves from CH1. 
Return Value 
The query returns the low level that has been set in the form of 
scientific notation such as: -1.000000e+01. 
 
7. VOLTage:OFFSet 
Command 
Format 
VOLTage:OFFSet {<offset>|MINimum|MAXimum} 
Function 
Set the offset voltage of CH1 in VDC. 
Explanations 
< offset >is the offset voltage for user to set. MIN selects the 
minimum DC offset voltage for specified function and amplitude. 
MAX selects the maximum value. 
Example 
VOLT:OFFS MIN 
 
8. VOLTage:OFFSet? 
Command 
Format 
VOLTage:OFFSet? 
Function 
Query the offset voltage of CH1.  
Return Value 
The query returns the offset voltage that has been set in the form 
of scientific notation such as: -9.998000e+00. 
 
9. VOLTage:UNIT 
Command 
Format 
VOLTage:UNIT {VPP|VRMS|DBM} 
Function 
Set the unit of voltage from CH1.  
Explanations 
DBM could be used only in non-high resistance. 
Example 
VOLT:UNIT VPP 
 
10. VOLTage:UNIT? 


<!-- page 35 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-23
Command 
Format 
VOLTage:UNIT? 
Function 
Query the unit of voltage from CH1. 
Return Value 
The query returns VPP, VRMS or DBM. 
 
11. VOLTage:CH2 
Command 
Format 
VOLTage:CH2 {<amplitude>|MINimum|MAXimum} 
Function 
Set the amplitude of CH2 in Vpp. 
Explanations 
MIN selects the minimum amplitude. MAX selects the maximum 
amplitude for the selected function.  
Example 
VPP, VRMS or DBM. Note that DBM could be used only in non-high 
resistance. The unit of voltage could be changed via sending   
VOLTage:UNIT:CH2. 
Command 
Format 
VOLT:CH2 MIN 
 
12. VOLTage:CH2? 
Command 
Format 
VOLTage:CH2? 
Function 
Query the amplitude of CH2.  
Return Value 
The query returns the amplitude that has been set in the form of 
scientific notation such as: CH2: 4.000000e-03. 
 
13. VOLTage:HIGH:CH2 
Command 
Format 
VOLTage:HIGH:CH2 {<voltage>|MINimum|MAXimum} 
Function 
Set the high level of waves from CH2 in V. 
Explanations 
<voltage>is the high level for user to set. MIN selects the 
minimum high level. MAX selects the maximum high level.  
Example 
VOLT:HIGH:CH2 MAX 
 
14. VOLTage:HIGH:CH2? 
Command 
Format 
VOLTage:HIGH:CH2? 
Function 
Query the high level of waves from CH2. 
Return Value 
The query returns the high leve that has been set in the form of 


<!-- page 36 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-24 
scientific notation such as: 1.500000e+00. 
 
15. VOLTage:LOW:CH2 
Command 
Format 
VOLTage:LOW:CH2 {<voltage>|MINimum|MAXimum} 
Function 
Set the low level of waves from CH2 in V.  
Explanations 
<voltage>is the low level for user to set. MIN selects the minimum 
low level. MAX selects the maximum low level.  
Example 
VOLT:LOW:CH2 MIN 
 
16. VOLTage:LOW:CH2? 
Command 
Format 
VOLTage:LOW:CH2? 
Function 
Query the low level of waves from CH2.  
Return Value 
The query returns the low leve that has been set in the form of 
scientific notation such as: -1.500000e+00. 
 
17. VOLTage:OFFSet:CH2 
Command 
Format 
VOLTage:OFFSet:CH2 {<offset>|MINimum|MAXimum} 
Function 
Set the offset voltage from CH2 in VDC. 
Explanations 
<offset>is the offset voltage for user to set. MIN selects the 
minimum DC offset voltage for specified function and amplitude. 
MAX selects the maximum value.  
Example 
VOLT:OFFS:CH2 MIN 
 
18. VOLTage:OFFSet:CH2? 
Command 
Format 
VOLTage:OFFSet:CH2? 
Function 
Query the offset voltage from CH2. 
Return Value 
The query returns the offset voltage that has been set in the form 
of scientific notation such as: -0.000000e+00. 
 
19. VOLTage:UNIT:CH2 
Command 
Format 
VOLTage:UNIT:CH2 {VPP|VRMS|DBM} 
Function 
Set the unit of voltage from CH2. 


<!-- page 37 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-25
Explanations 
DBM could be used only in non-high resistance.  
Example 
VOLT:UNIT:CH2 VPP 
 
20. VOLTage:UNIT:CH2? 
Command 
Format 
VOLTage:UNIT:CH2? 
Function 
Query the unit of voltage from CH2. 
Return Value 
The query returns VPP, VRMS or DBM.  
 


### OUTPut  *(p.38)*


<!-- page 38 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-26 
OUTPut 
OUTPut commands are used for setting the output parameters, such as: the output 
switch, the output loads, the polarity of the waveform, the synchronous output signal 
and the trigger output from CH1.  
DG1022 supports following OUTPut commands: 
1. 
OUTPut 
2. 
OUTPut? 
3. 
OUTPut:LOAD 
4. 
OUTPut:LOAD? 
5. 
OUTPut:POLarity 
6. 
OUTPut:POLarity? 
7. 
OUTPut:SYNC 
8. 
OUTPut:SYNC? 
9. 
OUTPut:TRIGger:SLOPe 
10. OUTPut:TRIGger:SLOPe? 
11. OUTPut:TRIGger 
12. OUTPut:TRIGger? 
13. OUTPut:CH2 
14. OUTPut:CH2? 
15. OUTPut:LOAD:CH2 
16. OUTPut:LOAD:CH2? 
17. OUTPut:POLarity:CH2 
18. OUTPut:POLarity:CH2? 
 


<!-- page 39 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-27
The detailed information of each command are: 
 
1. OUTPut 
Command 
Format 
OUTPut {OFF|ON} 
Function 
Disable or enable the [Output] connector of CH1. The default is 
“OFF”.  
Example 
OUTP ON 
 
2. OUTPut? 
Command 
Format 
OUTPut? 
Function 
Query the state of the [Output] connector of CH1. 
Return Value 
The query returns OFF or ON. 
 
3. OUTPut:LOAD 
Command 
Format 
OUTPut:LOAD {<ohm>|INFinity|MINimum|MAXimum} 
Function 
Select the desired output termination of CH1. The specified value 
is only used for amplitude and offset voltage. 
Explanations 
 
Ω is the unit of <ohm>, the default is 50Ω. 
 
“INFinity” sets the output terminal as “High Z”. 
Example 
OUTP:LOAD 50 
 
4. OUTPut:LOAD? 
Command 
Format 
OUTPut:LOAD? [MINimum|MAXimum] 
Function 
Query the current load settings of CH1.  
Return Value 
The query returns the current load setting in ohms or returns 
“Infinity”. 
 
5. OUTPut:POLarity 
Command 
Format 
OUTPut:POLarity {NORMal|INVerted} 
Function 
Set the polarity of waveform for CH1.  
Example 
OUTP:POL NORM 
 


<!-- page 40 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-28 
6. OUTPut:POLarity? 
Command 
Format 
OUTPut:POLarity? 
Function 
Query the polarity of waveform from CH1. 
Return Value 
The query returns NORM or INV. 
 
7. OUTPut:SYNC 
Command 
Format 
OUTPut:SYNC {OFF|ON} 
Function 
Disable or enable the rear panel [Output] connector of CH1. The 
default is “OFF”.  
Explanations 
The signal could be output synchronously only from CH1. 
Example 
OUTP:SYNC OFF 
 
8. OUTPut:SYNC? 
Command 
Format 
OUTPut:SYNC? 
Function 
Query the state of the [Sync Out] connector of CH1 on the rear 
panel. The default is “OFF”.  
Return Value 
The query returns SYNC OFF or SYNC ON. 
 
9. OUTPut:TRIGger:SLOPe 
Command 
Format 
OUTPut:TRIGger:SLOPe {POSitive|NEGative} 
Function 
Select the edge of “tirgger output”.  
If OUTPut:TRIGger command is enabled, the square wave that 
compatibles with TTL and within specified edge will be generated 
from [Ext Trig/FSK/Burst] conncetor on the rear panel as soon as 
you start sweeping.  
Explanations 
 
The command is used in Burst and Sweep operation. 
 
Select “POS” to output a pulse with a rising edge. 
 
Select “NEG” to output a pulse with a falling edge.  
Example 
OUTP:TRIG:SLOP POS 
 
10. OUTPut:TRIGger:SLOPe? 
Command 
Format 
OUTPut:TRIGger:SLOPe? 


<!-- page 41 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-29
Function 
Query the edge of “tirgger output”. 
Return Value 
The query returns POSITIVE or NEGATIVE. 
 
11. OUTPut:TRIGger 
Command 
Format 
OUTPut:TRIGger {OFF|ON} 
Function 
Disable or enable the [Ext Trig/FSK/Burst] connector on rear panel. 
Example 
OUTP:TRIG OFF 
 
12. OUTPut:TRIGger? 
Command 
Format 
OUTPut: TRIGger? 
Function 
Query the state of the [Ext Trig/FSK/Burst] connector on rear 
panel. 
Return Value 
The query returns OFF or ON. 
13. OUTPut:CH2 
Command 
Format 
OUTPut:CH2 {OFF|ON} 
Function 
Disable or enable the front-panel [Output] connector of CH2.  
Example 
OUTP:CH2 ON 
 
14. OUTPut:CH2? 
Command 
Format 
OUTPut:CH2? 
Function 
Query the state of front-panel [Output] connector of CH2. 
Return Value 
The query returns OFF or ON. 
 
15. OUTPut:LOAD:CH2 
Command 
Format 
OUTPut:LOAD:CH2 {<ohm>|INFinity|MINimum|MAXimum} 
Function 
Select the desired output termination of CH2. The specified value 
is only used for amplitude and offset voltage. 
Explanations 
 
Ω is the unit of <ohm>, the default is 50Ω. 
 
“INFinity” sets the output terminal as “High Z”. 
Example 
OUTP:LOAD:CH2 MIN 
 
16. OUTPut:LOAD:CH2? 


<!-- page 42 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-30 
Command 
Format 
OUTPut:LOAD:CH2? [MINimum|MAXimum] 
Function 
Query the current load settings of CH2. 
Return Value 
The query returns the current load setting in ohms or returns 
“Infinity”.  
 
17. OUTPut:POLarity:CH2 
Command 
Format 
OUTPut:POLarity:CH2 {NORMal|INVerted} 
Function 
Set the polarity of waveform from CH2. 
Example 
OUTP:POL:CH2 NORM 
 
18. OUTPut:POLarity:CH2? 
Command 
Format 
OUTPut:POLarity:CH2? 
Function 
Query the polarity of waveform from CH2. 
Return Value 
The query returns NORM or INV. 


### PULSe  *(p.43)*


<!-- page 43 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-31
PULSe 
PULSe commands are used for configuring the parameters of pulse waves from dual 
channels such as: period, pulse width, duty cycle and others. Following figure is going 
to help you comprehend the parameters about pulse wave.   
 
DG1022 supports following PULSe commands: 
1. 
PULSe:PERiod 
2. 
PULSe:PERiod? 
3. 
PULSe:WIDTh 
4. 
PULSe:WIDTh? 
5. 
PULSe:DCYCle 
6. 
PULSe:DCYCle? 
7. 
PULSe:PERiod:CH2 
8. 
PULSe:PERiod:CH2? 
9. 
PULSe:WIDTh:CH2 
10. PULSe:WIDTh:CH2? 
11. PULSe:DCYCle:CH2 
12. PULSe:DCYCle:CH2? 
 
90%
90%
50%
50%
10%
10%
Pulse Width
Period
Rise Time                                                                          
Fall Time


<!-- page 44 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-32 
The detailed information of each command are: 
 
1. PULSe:PERiod 
Command 
Format 
PULSe:PERiod {<seconds>|MINimum|MAXimum} 
Function 
Set the period of pulse from CH1 in seconds.  
Example 
PULS:PER 0.01 
 
2. PULSe:PERiod? 
Command 
Format 
PULSe:PERiod? [MINimum|MAXimum] 
Function 
Query the period of pulse from CH1.  
Return Value 
The query returns the period of pulse in the form of scientific 
notation and in seconds, such as: 1.000000e-02. 
 
3. PULSe:WIDTh 
Command 
Format 
PULSe:WIDTh {<seconds>|MINimum|MAXimum} 
Function 
Set the width of pulse for CH1 in seconds.  
Example 
PULS:WIDT 0.005 
 
4. PULSe:WIDTh? 
Command 
Format 
PULSe:WIDTh? [MINimum|MAXimum] 
Function 
Query the width of pulse from CH1. 
Return Value 
The qurey returns the width of pulse in the form of scientific 
notation and in seconds, such as: 5.000000e-03. 
 
5. PULSe:DCYCle 
Command 
Format 
PULSe:DCYCle {<percent>|MINimum|MAXimum} 
Function 
Set the duty cycle of pulse for CH1.  
Example 
PULS:DCYC 50 
 
6. PULSe:DCYCle? 
Command 
Format 
PULSe:DCYCle? [MINimum|MAXimum] 


<!-- page 45 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-33
Function 
Query the duty cycle of pulse from CH1.  
Return Value 
The qurey returns the percent of duty cycle of pulse in the form of 
scientific notation such as: 5.000000e+01. 
 
7. PULSe:PERiod:CH2 
Command 
Format 
PULSe:PERiod:CH2 {<seconds>|MINimum|MAXimum} 
Function 
Set the period of pulse for CH2 in seconds. 
Example 
PULS:PER:CH2 0.01 
 
8. PULSe:PERiod:CH2? 
Command 
Format 
PULSe:PERiod:CH2? [MINimum|MAXimum] 
Function 
Query the period of pulse from CH2. 
Return Value 
The qurey returns the period of pulse in the form of scientific 
notation and in seconds, such as: 1.000000e-02. 
 
9. PULSe:WIDTh:CH2 
Command 
Format 
PULSe:WIDTh:CH2 {<seconds>|MINimum|MAXimum} 
Function 
Set the pulse width for CH2 in seconds. 
Example 
PULS:WIDT:CH2 0.005 
 
10. PULSe:WIDTh:CH2? 
Command 
Format 
PULSe:WIDTh:CH2? [MINimum|MAXimum] 
Function 
Query the pulse width from CH2. 
Return Value 
The qurey returns the pulse width in the form of scientific notation 
and in seconds, such as: 5.000000e-03. 
 
11. PULSe:DCYCle:CH2 
Command 
Format 
PULSe:DCYCle:CH2 {<percent>|MINimum|MAXimum} 
Function 
Set the duty cycle of pulse from CH2. 
Example 
PULS:DCYC:CH2 50 
 
12. PULSe:DCYCle:CH2? 


<!-- page 46 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-34 
Command 
Format 
PULSe:DCYCle:CH2? [MINimum|MAXimum] 
Function 
Query the duty cycle of pulse from CH2. 
Return Value 
The qurey returns the percent of duty cycle in the form of scientific 
notationn, such as: 5.000000e+01. 
 


### AM  *(p.47)*


<!-- page 47 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-35
AM 
In AM, the amplitude of carrier is varies with the instantaneous voltage of the 
modulation waveform. Among CH1, the generator can generate AM modulation waves. 
In addition, AM commands could be used for these settings: modulation source, 
modulation waveform, modulation frequency, modulation depth and AM modulation 
state.  
DG1022 supports following AM commands: 
1. 
AM:SOURce 
2. 
AM:SOURce? 
3. 
AM:INTernal:FUNCtion 
4. 
AM:INTernal:FUNCtion? 
5. 
AM:INTernal:FREQuency 
6. 
AM:INTernal:FREQuency? 
7. 
AM:DEPTh 
8. 
AM:DEPTh? 
9. 
AM:STATe 
10. AM:STATe? 
 


<!-- page 48 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-36 
The detailed information of each command are: 
 
1. AM:SOURce 
Command 
Format 
AM:SOURce {INTernal|EXTernal} 
Function 
Select internal or external modulation source, the default is INT.  
Example 
AM:SOUR EXT 
 
2. AM:SOURce? 
Command 
Format 
AM:SOURce? 
Function 
Query the modulation source of AM.  
Return Value 
The query returns INT or EXT.  
 
3. AM:INTernal:FUNCtion 
Command 
Format 
AM:INTernal:FUNCtion 
{SINusoid|SQUare|RAMP|NRAMp|TRIangle|NOISe|USER} 
Function 
Select the internal modulation wave of AM. 
Explanations 
In internal modulation source mode, the modulation wave could be 
sine, square, ramp, negative ramp, triangle, noise or arbitrary 
wave, the default is sine. 
Example 
AM:INT:FUNC SQU 
 
4. AM:INTernal:FUNCtion? 
Command 
Format 
AM:INTernal:FUNCtion? 
Function 
Query the internal modulation wave of AM that has been selected. 
Return Value 
The query returns SIN, SQU, RAMP, NRAM, TRI, NOIS or USER. 
 
5. AM:INTernal:FREQuency 
Command 
Format 
AM:INTernal:FREQuency {<frequency>|MINimum|MAXimum} 
Function 
Set the frequency of internal modulation of AM in Hz. 
Explanations 
Frequency range: 2mHz～20kHz 
Example 
AM:INT:FREQ 200 
 
6. AM:INTernal:FREQuency? 


<!-- page 49 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-37
Command 
Format 
AM:INTernal:FREQuency? 
Function 
Query the frequency of internal modulation of AM. 
Return Value 
The query returns the percent of the frequency of AM internal 
modulation in the form of scientific notation, such as: 
2.000000e+02. 
 
7. AM:DEPTh 
Command 
Format 
AM:DEPTh {<depth percent>|MINimum|MAXimum} 
Function 
Set the depth of internal modulation of AM in percent.  
Explanations 
Depth range: 0%～120% 
Example 
AM:DEPT 70 
 
8. AM:DEPTh? 
Command 
Format 
AM:DEPTh? [MINimum|MAXimum] 
Function 
Query the depth of internal modulation of AM.  
Return Value 
The qurey returns the percent of the depth of AM internal 
modulation in the form of scientific notation, such as: 
7.000000e+01. 
 
9. AM:STATe 
Command 
Format 
AM:STATe {OFF|ON} 
Function 
Disable or enable AM function.  
Example 
AM:STAT OFF 
 
10.  AM:STATe? 
Command 
Format 
AM:STATe? 
Function 
Query the modulation state of AM. 
Return Value 
The query returns OFF or ON. 


### FM  *(p.50)*


<!-- page 50 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-38 
FM 
In FM, the frequency of carrier is varies with the instantaneous voltage of the 
modulation waveform. Among CH1, the generator can generate FM modulated waves. 
In addition, FM commands could be used for these settings: modulation source, 
modulation waveform, modulation frequency, frequency deviation of peak value and 
FM modulation state.  
DG1022 supports following FM commands: 
1. 
FM:SOURce 
2. 
FM:SOURce? 
3. 
FM:INTernal:FUNCtion 
4. 
FM:INTernal:FUNCtion? 
5. 
FM:INTernal:FREQuency 
6. 
FM:INTernal:FREQuency? 
7. 
FM:DEViation 
8. 
FM:DEViation? 
9. 
FM:STATe 
10. FM:STATe? 
 


<!-- page 51 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-39
The detailed information of each command are: 
 
1. FM:SOURce 
Command 
Format 
FM:SOURce {INTernal|EXTernal} 
Function 
Select internal or external modulation source, the default is INT. 
Example 
FM:SOUR EXT 
 
2. FM:SOURce? 
Command 
Format 
FM:SOURce? 
Function 
Query the modulation source of FM.  
Return Value 
The query returns INT or EXT. 
 
3. FM:INTernal:FUNCtion 
Command 
Format 
FM:INTernal:FUNCtion 
{SINusoid|SQUare|RAMP|NRAMp|TRIangle|NOISe|USER} 
Function 
Select the internal modulation wave of FM. 
Explanations 
In internal modulation source mode, the modulation wave could be 
sine, square, ramp, negative ramp, triangle, noise or arbitrary 
wave, the default is sine. 
Example 
FM:INT:FUNC SQU 
 
4. FM:INTernal:FUNCtion? 
Command 
Format 
FM:INTernal:FUNCtion? 
Function 
Query the internal modulation wave of FM that has been selected. 
Return Value 
The query returns SIN, SQU, RAMP, NRAM, TRI, NOIS or USER. 
 
5. FM:INTernal:FREQuency 
Command 
Format 
FM:INTernal:FREQuency {<frequency>|MINimum|MAXimum} 
Function 
Set the frequency of internal modulation of FM in Hz. 
Explanations 
Frequency range: 2mHz～20kHz 
Example 
FM:INT:FREQ 200 
 
6. FM:INTernal:FREQuency? 


<!-- page 52 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-40 
Command 
Format 
FM:INTernal:FREQuency? 
Function 
Query the frequency of internal modulation of FM. 
Return Value 
The query returns the percent of the frequency of FM internal 
modulation in the form of scientific notation, such as: 
2.000000e+02 
 
7. FM:DEViation 
Command 
Format 
FM:DEViation{<frequency deviation of peak value> 
|MINimum|MAXimum} 
Function 
Set the frequency deviation of peak value of FM in Hz.  
Example 
FM:DEV 100 
 
8. FM:DEViation? 
Command 
Format 
FM:DEViation? [MINimum|MAXimum] 
Function 
Query the frequency deviation of peak value of FM. 
Return Value 
The query returns the frequency deviation of peak value of FM in 
the form of scientific notation and in Hz, such as: 1.000000e+02 
 
9. FM:STATe 
Command 
Format 
FM:STATe {OFF|ON} 
Function 
Disable or enable FM function.  
Example 
FM:STAT OFF 
 
10.  FM:STATe? 
Command 
Format 
FM:STATe? 
Function 
Query the modulation state of FM. 
Return Value 
The query returns OFF or ON. 
 


### PM  *(p.53)*


<!-- page 53 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-41
PM 
In PM, the phase of carrier is varies with the instantaneous voltage of the modulation 
waveform. Among CH1, the generator can generate PM modulation waves. In addition, 
PM commands could be used for these settings: modulation source, modulation 
waveform, modulation frequency, phase deviation and PM modulation state.  
DG1022 supports following PM commands: 
1. 
PM:SOURce 
2. 
PM:SOURce? 
3. 
PM:INTernal:FUNCtion 
4. 
PM:INTernal:FUNCtion? 
5. 
PM:INTernal:FREQuency 
6. 
PM:INTernal:FREQuency? 
7. 
PM:DEViation 
8. 
PM:DEViation? 
9. 
PM:STATe 
10. PM:STATe? 
 


<!-- page 54 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-42 
The detailed information of each command are: 
 
1. PM:SOURce 
Command 
Format 
PM:SOURce {INTernal|EXTernal} 
Function 
Select internal or external modulation source, the default is INT. 
Example 
PM:SOUR EXT 
 
2. PM:SOURce? 
Command 
Format 
PM:SOURce? 
Function 
Query the modulation source of PM. 
Return Value 
The query returns INT or EXT. 
 
3. PM:INTernal:FUNCtion 
Command 
Format 
PM:INTernal:FUNCtion 
{SINusoid|SQUare|RAMP|NRAMp|TRIangle|NOISe|USER} 
Function 
Select the internal modulation wave of PM. 
Explanations 
In internal modulation source mode, the modulation wave could be 
sine, square, ramp, negative ramp, triangle, noise or arbitrary 
wave, the default is sine. 
Example 
PM:INT:FUNC SQU 
 
4. PM:INTernal:FUNCtion? 
Command 
Format 
PM:INTernal:FUNCtion? 
Function 
Query the internal modulation wave of PM that has been selected. 
Return Value 
The query returns SIN, SQU, RAMP, NRAM, TRI, NOIS or USER. 
 
5. PM:INTernal:FREQuency 
Command 
Format 
PM:INTernal:FREQuency {<frequency>|MINimum|MAXimum} 
Function 
Set the frequency of internal modulation of PM and in Hz.  
Explanations 
Frequency range: 2mHz～20kHz 
Example 
PM:INT:FREQ 200 
 
6. PM:INTernal:FREQuency? 


<!-- page 55 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-43
Command 
Format 
PM:INTernal:FREQuency? 
Function 
Query the frequency of internal modulation of PM. 
Return Value 
The query returns the internal modulation frequency of PM in the 
form of scientific notation, such as: 2.000000e+02. 
 
7. PM:DEViation 
Command 
Format 
PM:DEViation {<phase deviation>|MINimum|MAXimum} 
Function 
Set the phase deviation of PM and in degree.  
Explanations 
Phase deviation range: 0°～360° 
Example 
PM:DEV 180 
 
8. PM:DEViation? 
Command 
Format 
PM:DEViation? [MINimum|MAXimum] 
Function 
Query the phase deviation of PM.  
Return Value 
The query returns the phase deviation of PM in the form of 
scientific notation in degree, such as: 1.800000e+02. 
 
9. PM:STATe 
Command 
Format 
PM:STATe {OFF|ON} 
Function 
Disable or enable PM function. 
Example 
PM:STAT OFF 
 
10.  PM:STATe? 
Command 
Format 
PM:STATe? 
Function 
Query the modulation state of PM. 
Return Value 
The query returns OFF or ON. 
 


### FSKey  *(p.56)*


<!-- page 56 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-44 
FSKey 
In FSK modulation, you can configure the generator to “shift” its output frequency 
between two preset frequencies (called the “carrier frequency” and the “hop 
frequency”) from CH1. The output frequency that shifts from the carrier frequency to 
the hop frequency is called “FSK rate”. FSK rate is determined by internal frequency 
generator or signal level which is inputted from the [Ext Trig/FSK/Burst] connector on 
the rear panel. 
 
To generate a FSK waveform, you have to configure the carrier wave, choose the 
modulation source, select the “hop frequency” and the FSK rate, and then enable the 
FSK modulation. 
DG1022 supports following FSK commands: 
1. 
FSK:SOURce 
2. 
FSK:SOURce? 
3. 
FSK:FREQuency 
4. 
FSK:FREQuency? 
5. 
FSK:INTernal:RATE 
6. 
FSK:INTernal:RATE? 
7. 
FSK:STATe 
8. 
FSK:STATe? 
 


<!-- page 57 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-45
The detailed information of each command are: 
 
1. FSK:SOURce 
Command 
Format 
FSK:SOURce {INTernal|EXTernal} 
Function 
Select internal or external modulation source, the default is INT. 
Example 
FSK:SOUR EXT 
 
2. FSK:SOURce? 
Command 
Format 
FSK:SOURce? 
Function 
Query the modulation source of FSK. 
Return Value 
The query returns INT or EXT. 
 
3. FSK:FREQuency 
Command 
Format 
FSK:FREQuency {<frequency>|MINimum|MAXimum} 
Function 
Set the hop frequency of FSK in Hz.  
Example 
FSK:FREQ 10 
 
4. FSK:FREQuency? 
Command 
Format 
FSK:FREQuency? 
Function 
Query the hop frequency of FSK.  
Return Value 
The query returns the hop frequency of FSK in the form of 
scientific notation, such as: 1.000000e+01. 
 
5. FSK:INTernal:RATE 
Command 
Format 
FSK:INTernal:RATE {<rate>|MINimum|MAXimum} 
Function 
Set the rate at which the output frequency “shifts” between the 
carrier and hop frequency, the unit is Hz. 
Explanations 
Rate range: 2mHz～50kHz 
Example 
FSK:INT:RATE 100 
 
6. FSK:INTernal:RATE? 
Command 
FSK:INTernal:RATE? 


<!-- page 58 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-46 
Format 
Function 
Query the rate of FSK.  
Return Value 
The query returns the rate of FSK in the form of scientific notation, 
such as: 1.000000e+02. 
 
7. FSK:STATe 
Command 
Format 
FSK:STATe {OFF|ON} 
Function 
Disable or enable FSK function. 
Example 
FSK:STAT OFF 
 
8. FSK:STATe? 
Command 
Format 
FSK:STATe? 
Function 
Query the modulation state of FSK. 
Return Value 
The query returns OFF or ON. 


### SWEep  *(p.59)*


<!-- page 59 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-47
SWEep 
In frequency sweep mode, the generator “steps” from the start frequency to the stop 
frequency at a sweep rate that you specified. You can sweep up or down in frequency, 
and with either linear or logarithmic spacing.  
In addition, you can configure the generator to output a single sweep (one pass from 
start frequency to stop frequency) by applying an external or manual trigger. The 
generator can produce a frequency sweep for sine, square, ramp or arbitrary 
waveforms (pulse, noise, and DC are not allowed) from CH1. 
DG1022 supports following SWEep commands: 
1. 
SWEep:SPACing 
2. 
SWEep:SPACing? 
3. 
SWEep:TIME 
4. 
SWEep:TIME? 
5. 
SWEep:STATe 
6. 
SWEep:STATe? 
 


<!-- page 60 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-48 
The detailed information of each command are: 
 
1. SWEep:SPACing 
Command 
Format 
SWEep:SPACing {LINear|LOGarithmic} 
Function 
Select linear or logarithmic spacing for the sweep, the default is 
Linear. 
Example 
SWE:SPAC LIN 
 
2. SWEep:SPACing? 
Command 
Format 
SWEep:SPACing? 
Function 
Query current sweep mode. 
Return Value 
The query returns LINEAR or LOG. 
 
3. SWEep:TIME 
Command 
Format 
SWEep:TIME {<seconds>|MINimum|MAXimum} 
Function 
Set the sweep time expected from the start frequency to the stop 
frequency, the default time is 1 s.  
Explanations 
<seconds> is the sweep time, the unit is s. 
MIN=1ms, MAX＝500s。 
Example 
SWE:TIME 10 
 
4. SWEep:TIME? 
Command 
Format 
SWEep:TIME? 
Function 
Query the sweep time expected from the start frequency to the 
stop frequency. 
Return Value 
The query returns the sweep time in the form of scientific notation 
in seconds such as: 1.000000e+01. 
 
5. SWEep:STATe 
Command 
Format 
SWEep:STATe {OFF|ON} 
Function 
Disable or enable the sweep mode.  
Example 
SWE:STAT OFF 


<!-- page 61 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-49
 
6. SWEep:STATe? 
Command 
Format 
SWEep:STATe? 
Function 
Query the sweep state.  
Return Value 
The query returns OFF or ON. 
 


### TRIGger  *(p.62)*


<!-- page 62 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-50 
TRIGger 
TRIGger commands are available in Sweep and Burst mode for CH1 only. 
DG1022 supports following TRIGger commands: 
1. 
TRIGger:SOURce 
2. 
TRIGger:SOURce? 
3. 
TRIGger:SLOPe 
4. 
TRIGger:SLOPe? 
5. 
TRIGger:DELay 
6. 
TRIGger:DELay? 
 


<!-- page 63 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-51
The detailed information of each command are: 
 
1. TRIGger:SOURce 
Command 
Format 
TRIGger:SOURce {IMMediate|EXTernal|BUS} 
Function 
Select the trigger source for generator, such as: internal trigger 
(IMM), external trigger (EXT) from the [Ext Trig/FSK/Burst] 
connector on the rear panel, or manual trigger (BUS). The default 
is IMM.  
Example 
TRIG:SOUR EXT 
 
2. TRIGger:SOURce? 
Command 
Format 
TRIGger:SOURce? 
Function 
Query the trigger source of generator. 
Return Value 
The query returns IMM, EXT or BUS. 
 
3. TRIGger:SLOPe 
Command 
Format 
TRIGger:SLOPe {POSitive|NEGative} 
Function 
Select whether the generator uses rising edge(POS) or falling 
edge(NEG) of the trigger signal inputted from the [Ext 
Trig/FSK/Burst] connector on the rear panel. The default is POS 
(rising edge).  
Explanations 
This command could be used only when OUTPut:TRIGger is 
enabled.  
Example 
TRIG:SLOP POS 
 
4. TRIGger:SLOPe? 
Command 
Format 
TRIGger:SLOPe? 
Function 
Query the edge of trigger signal that has been selected.  
Return Value 
The query returns POSITIVE or NEGATIVE. 
 
5. TRIGger:DELay 
Command 
Format 
TRIGger:DELay {<second>|MINimum|MAXimum} 


<!-- page 64 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-52 
Function 
Set the trigger delay in seconds. Note: this command is only 
applied to Burst mode.  
Example 
TRIG:DEL 0.000005 
 
6. TRIGger:DELay? 
Command 
Format 
TRIGger:DELay? 
Function 
Query the trigger delay.  
Return Value 
The query returns the selected delay time in the form of scientific 
notation in seconds, such as: 5.000000e-06. 


### BURSt  *(p.65)*


<!-- page 65 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-53
BURSt 
BURSt commands are used for setting the generator to output pulse sequence(called 
burst) with specified cycles. Among CH1, burst could be generated based on sine, 
square, ramp, pulse or arbitrary waves.  
DG1022 supports following BURSt commands: 
1. 
BURSt:MODE 
2. 
BURSt:MODE? 
3. 
BURSt:NCYCles 
4. 
BURSt:NCYCles? 
5. 
BURSt:INTernal:PERiod 
6. 
BURSt:INTernal:PERiod? 
7. 
BURSt:PHASe 
8. 
BURSt:PHASe? 
9. 
BURSt:STATe 
10. BURSt:STATe? 
11. BURSt:GATE:POLarity 
12. BURSt:GATE:POLarity? 
 


<!-- page 66 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-54 
The detailed information of each command are: 
 
1. BURSt:MODE 
Command 
Format 
BURSt:MODE {TRIGgered|GATed} 
Function 
Select the burst mode. 
Explanations 
 
In TRIG mode, the generator outputs a wave with specified 
cycle number once receive an assigned trigger via sending 
TRIGger:SOURce. 
 
In GAT mode, the output state of waves (“ON” or “OFF”) 
depends on the external level used by [Ext Trig/FSK/Burst] 
connector on the rear panel.  
 
The default burst mode is TRIG.  
Example 
BURS:MODE GAT 
 
2. BURSt:MODE? 
Command 
Format 
BURSt:MODE? 
Function 
Query the burst mode.  
Return Value 
The query returns TRIG or GAT. 
 
3. BURSt:NCYCles 
Command 
Format 
BURSt:NCYCles {<cycle>|INFinity|MINimum|MAXimum} 
Function 
Set the cycle number of burst (only used in TRIG mode).  
Explanations 
 
<cycle> is the cycle number for user to set.  
 
MIN=1 cycle, MAX=50,000 cycles, INF is infinite number of 
cycles.  
Example 
BURS:NCYC 100 
 
4. BURSt:NCYCles? 
Command 
Format 
BURSt:NCYCles? 
Function 
Query the cycle number of burst.  
Return Value 
The query returns the burst counting in the form of scientific 
notation such as 1.000000e+02 or returns “Infinite”. 
 


<!-- page 67 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-55
5. BURSt:INTernal:PERiod 
Command 
Format 
BURSt:INTernal:PERiod {<秒>|MINimum|MAXimum} 
Function 
Set the period of burst in internal trigger mode. 
Explanations 
 
<second> is the burst period for user to set, the unit is s.  
 
MIN=1μs, MAX=500s. 
Example 
BURS:INT:PER 10 
 
6. BURSt:INTernal:PERiod? 
Command 
Format 
BURSt:INTernal:PERiod? [MINimum|MAXimum] 
Function 
Query the period of burst in internal trigger mode.  
Return Value 
The query returns the burst period in the form of scientific notation 
such as: 1.000000e+01. 
 
7. BURSt:PHASe 
Command 
Format 
BURSt:PHASe {<angle>|MINimum|MAXimum} 
Function 
Set the initial phase of burst.  
Explanations 
 
<angle> is the phase for user to set, the unit is degree. 
 
MIN=-180°, MAX=180°. 
Example 
BURS:PHAS 150 
 
8. BURSt:PHASe? 
Command 
Format 
BURSt:PHASe? [MINimum|MAXimum] 
Function 
Query the initial phase of burst.  
Return Value 
The query returns the initial phase of burst in the form of scientific 
notation in degree such as: 1.500000e+02. 
 
9. BURSt:STATe 
Command 
Format 
BURSt:STATe {OFF|ON} 
Function 
Enable or disable burst mode.  
Example 
BURS:STAT OFF 
 
10. BURSt:STATe? 


<!-- page 68 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-56 
Command 
Format 
BURSt:STATe? 
Function 
Query the state of burst mode.  
Return Value 
The query returns OFF or ON. 
 
11. BURSt:GATE:POLarity 
Command 
Format 
BURSt:GATE:POLarity {NORMal|INVerted} 
Function 
Set the polarity of external gating signal from [Ext Trig/FSK/Burst] 
conncetor on the rear panel, the default is NORMal. 
Example 
BURS:GATE:POL INV 
 
12. BURSt:GATE:POLarity? 
Command 
Format 
BURSt:GATE:POLarity? 
Function 
Query the polarity of external gating signal from the rear panel. 
Return Value 
The query returns NORM or INV. 


### DATA  *(p.69)*


<!-- page 69 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-57
DATA 
DATA commands are usd for editing or saving arbitrary waves and outputing those 
waves via CH1. You can store ten user-defined waveforms at most in non-volatile 
memory in addition to one in volatile memory. Each waveform can contain data points 
within 1 and 524,288 (512k).  
DG1022 supports following DATA commands: 
1. 
DATA 
2. 
DATA:DAC 
3. 
DATA:COPY 
4. 
DATA:DELete 
5. 
DATA:CATalog? 
6. 
DATA:RENAME 
7. 
DATA:NVOLatile:CATalog? 
8. 
DATA:NVOLatile:FREE? 
9. 
DATA:ATTRibute:POINts? 
10. DATA:LOAD 
 


<!-- page 70 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-58 
The detailed information of each command are: 
 
1. DATA 
Command 
Format 
DATA VOLATILE,<value>, <value>, . . . 
Function 
Load the floating point numbers between -1 and 1 into volatile 
memory.  
Explanations 
 DATA command may cover a previous waveform in volatile 
memory (does not generate error). 
 Use DATA:COPY command to copy the waveform to 
non-volatile memory. 
 Use DATA:DELete command to delete the waveform in 
volatile memory or any of the ten user-defined waveforms in 
nonvolatile memory. 
 Use DATA:CATalog? command to list all waveforms currently 
stored in volatile and non-volatile memory. 
 Use FUNCtion:USER command to output the waves that has 
been edited and stored after downloading the waveform data 
to memory. 
Example 
DATA VOLATILE,1,0.67,0.33,0,-0.33,-0.67,-1 
 
2. DATA:DAC 
Command 
Format 
DATA:DAC VOLATILE,<value>, <value>, . . . 
Function 
Download decimal integer values from 0 to 16383 into volatile 
memory.  
Explanations 
 DATA:DAC command may cover a previous waveform in 
volatile memory ( does not generate error). 
 Use DATA:COPY command to copy the waveform to 
non-volatile memory. 
 Use DATA:DELete command to delete the waveform in 
volatile memory or any of the ten user-defined waveforms in 
nonvolatile memory. 
 Use DATA:CATalog? command to list all waveforms currently 
stored in volatile and non-volatile memory. 
 Use FUNCtion:USER command to output the waves that has 
been edited and stored after downloading the waveform data 


<!-- page 71 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-59
to memory. 
Example 
DATA:DAC VOLATILE,8192,16383,8192,0 
 
3. DATA:COPY  
Command 
Format 
DATA:COPY < destination arb name >[,VOLATILE] 
Function 
Copy the waveform from volatile memory to the specified 
non-volatile memory. 
Explanations 
 The arb name may contain up to 12 characters. The first 
character must be a letter (A-Z or a-z), the remaining 
characters can be numbers (0-9) or the underscore character 
(“_”). Blank space is invalid. 
 The VOLATILE parameter is optional and can be omitted. Note 
that the keyword “VOLATILE” does not have a short form. 
 Use DATA:DELete command to delete the waveform in 
volatile memory or any of the ten user-defined waveforms in 
non-volatile memory.  
 Use DATA:CATalog? command to list all waveforms currently 
stored in volatile and non-volatile memory.  
Example 
DATA:COPY a1,VOLATILE 
 
4. DATA:DELete 
Command 
Format 
DATA:DELete <arb name> 
Function 
Delete the specified arbitrary waveform from either volatile 
memory or non-volatile memory.  
Example 
DATA:DEL a1 
 
5. DATA:CATalog? 
Command 
Format 
DATA:CATalog? 
Function 
Query the names of all waveforms currently available for selection. 
Return Value 
The query returns the names of the five built-in waveforms 
(non-volatile memory), “VOLATILE” (if a waveform is currently 
downloaded to volatile memory), and all user-defined waveforms 
downloaded to non-volatile memory, such as: 
"VOLATILE","EXP_RISE","EXP_FALL","NEG_RAMP", "SINC", 


<!-- page 72 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-60 
"CARDIAC","A","B","C","D","E","F","G","H","I","J". 
 
6. DATA:RENAME 
Command 
Format 
DATA:RENAME <destination arb name>,<new arb name> 
Function 
Rename an arbitrary wave. 
Example 
DATA:RENAME old, new 
 
7. DATA:NVOLatile:CATalog? 
Command 
Format 
DATA:NVOLatile:CATalog? 
Function 
Query the names of all user-defined arbitrary waveforms 
downloaded to non-volatile memory.  
Return Value 
The query returns the quoted names of up to 10 waveforms such 
as: "A","B","C","D","E","F","G","H","I","J". 
 
8. DATA:NVOLatile:FREE? 
Command 
Format 
DATA:NVOLatile:FREE? 
Function 
Query the number of non-volatile memory that is available for 
saving user-defined waveforms.  
Return Value 
The query returns 0 (denotes full memory), 1, 2, 3, 4, 5, 6, 7, 8, 9, 
10. 
 
9. DATA:ATTRibute:POINts? 
Command 
Format 
DATA:ATTRibute:POINts? <destination arb name> 
Function 
Query the number of points in the specified arbitrary waveform.  
Return Value 
The query return a value within 0~524,288, such as 4096. 
 
10. DATA:LOAD 
Command 
Format 
DATA:LOAD [<destination arb name>] 
Function 
Upload the specified arbitrary wave to the application software. 


### MEMory  *(p.73)*


<!-- page 73 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-61
MEMory 
The generator has 10 storage locations in non-volatile memory (STATE1~ STATE10) to 
store instrument states. The locations are numbered from 1 to 10. The generator 
automatically uses location “0” to hold the state of the instrument when power down. 
You can also assign a user-defined name to each of the locations (1 through 10) from 
the front panel. 
DG1022 supports following MEMory commands: 
1. 
MEMory:STATe:NAME 
2. 
MEMory:STATe:NAME? 
3. 
MEMory:STATe:DELete 
4. 
MEMory:STATe:RECall:AUTO 
5. 
MEMory:STATe:RECall:AUTO? 
6. 
MEMory:STATe:VALid? 
7. 
MEMory:NSTates? 
 


<!-- page 74 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-62 
The detailed information of each command are: 
 
1. MEMory:STATe:NAME 
Command 
Format 
MEMory:STATe:NAME {0|1|2|3|4|5|6|7|8|9|10} [,<name>] 
Function 
Assign an user-defined name for specified memory location.  
Example 
MEM:STAT:NAME 1,A1 
 
2. MEMory:STATe:NAME? 
Command 
Format 
MEMory:STATe:NAME? {0|1|2|3|4|5|6|7|8|9|10} 
Function 
Query the name of specified memory location.  
Return Value 
The query returns the name of specified memory location such as 
A1. If no name was assigned, the return is empty.  
 
3. MEMory:STATe:DELete 
Command 
Format 
MEMory:STATe:DELete {0|1|2|3|4|5|6|7|8|9|10} 
Function 
Delete the contents in specified memory location.  
Example 
MEM:STAT:DEL 1 
 
4. MEMory:STATe:RECall:AUTO 
Command 
Format 
MEMory:STATe:RECall:AUTO {OFF| ON} 
Function 
Disable or enable the automatic recall of the power-down state 
from storage location “0” when power on. Select “ON” to 
automatically recall power-down state when power on and select 
“OFF” (default) to issue a reset.  
Example 
MEM:STAT:REC:AUTO OFF 
 
5. MEMory:STATe:RECall:AUTO? 
Command 
Format 
MEMory:STATe:RECall:AUTO? 
Function 
Query the recall state when power off. 
Return Value 
The query returns OFF or ON. 
 
6. MEMory:STATe:VALid? 


<!-- page 75 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-63
Command 
Format 
MEMory:STATe:VALid? {0|1|2|3|4|5|6|7|8|9|10} 
Function 
Query the specified storage location to determine if a valid state 
has already been stored in that location.  
Return Value 
Return “0” if no state has been stored or if it has been deleted. or 
else return “1”. 
 
7. MEMory:NSTates? 
Command 
Format 
MEMory:NSTates? 
Function 
Query the total number of memory locations available for state 
storage. 
Return Value 
Always returns “11” (including memory location “0”). 


### SYSTem  *(p.76)*


<!-- page 76 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-64 
SYSTem 
SYSTem commands provide information about state storage, power-down recall, 
error state and screen control of the front panel and other information about the 
instrument. 
DG1022 supports following SYSTem commands: 
1. 
SYSTem:ERRor? 
2. 
SYSTem:VERSion? 
3. 
SYSTem:BEEPer:STATe 
4. 
SYSTem:BEEPer:STATe? 
5. 
SYSTem:LOCal 
6. 
SYSTem:RWLock 
7. 
SYSTem:REMote 
8. 
SYSTem:CLKSRC 
9. 
SYSTem:LANGuage 
 


<!-- page 77 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-65
The detailed information of each command are: 
 
1. SYSTem:ERRor? 
Command 
Format 
SYSTem:ERRor? 
Function 
Read and clear an error from error queues.  
Return Value 
The query returns an error information with following format:  
-118,"Invalid parameter" 
 
2. SYSTem:VERSion? 
Command 
Format 
SYSTem:VERSion? 
Function 
Query current edition of the instrument.  
Return Value 
The query returns the character string with following format:  
00.01.00.04.00.02.03 
 
3. SYSTem:BEEPer:STATe 
Command 
Format 
SYSTem:BEEPer:STATe {OFF|ON} 
Function 
Enable or disable the beep when error occurs on front panel or 
remote interface.  
Example 
SYST:BEEP:STAT OFF 
 
4. SYSTem:BEEPer:STATe? 
Command 
Format 
SYSTem:BEEPer:STATe? 
Function 
Query the state of beeper.  
Return Value 
The query returns 0 (OFF) or 1 (ON). 
 
5. SYSTem:LOCal 
Command 
Format 
SYSTem:LOCal 
Function 
Activate local state and delete RMT indicator and unlock the front 
panel.  
 
6. SYSTem:RWLock 
Command 
SYSTem:RWLock 


<!-- page 78 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-66 
Format 
Function 
Activate remote state with locking function and display R-LOCK 
indicator and lock the keyboard. (including Local button)  
 
7. SYSTem:REMote 
Command 
Format 
SYSTem:REMote 
Function 
Activate remote state and display RMT indicator and lock the  
keyboard. (except for Local button)  
 
8. SYSTem:CLKSRC 
Command 
Format 
SYSTem:CLKSRC {EXT|INT} 
Function 
Select the system clock source as internal or external, the default 
is INT.  
Explanations 
When external clock source is actived, the system accepts the 
clock source from [10 MHz In] connector on the rear panel. 
Example 
SYST:CLKSRC EXT 
 
9. SYSTem:LANGuage 
Command 
Format 
SYSTem:LANGuage {CHINESE|ENGLISH} 
Function 
Select the system language as Chinese or English. 
Example 
SYST:LANG CHINESE 


### PHASe  *(p.79)*


<!-- page 79 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-67
PHASe 
PHASe commands are used for setting the initial phase of signals from each channel 
and controlling the dual channels phase output synchronously. 
DG1022 supports following PHASe commands: 
1. 
PHASe 
2. 
PHASe? 
3. 
PHASe:CH2 
4. 
PHASe:CH2? 
5. 
PHASe:ALIGN 
 
 
 
 


<!-- page 80 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-68 
The detailed information of each command are: 
 
1. PHASe 
Command 
Format 
PHASe {<angle>|MINimum|MAXimum} 
Function 
Set the initial phase of signals from CH1.  
Explanations 
<angle> is the phase for user to set, the unit is degree.  
MIN=-180°, MAX=180°。 
Return Value 
PHAS 90 
 
2. PHASe? 
Command 
Format 
PHASe? [MINimum|MAXimum] 
Function 
Query the initial phase of signals from CH1.  
Return Value 
The query returns any numerical value between -180 and 180, 
such as: 90.000. 
 
3. PHASe:CH2 
Command 
Format 
PHASe:CH2 {<angle>|MINimum|MAXimum} 
Function 
Set the initial phase of signals from CH2. 
Explanations 
<angle> is the phase for user to set, the unit is degree. 
MIN=-180°, MAX=180°。 
Return Value 
PHAS:CH2 90 
 
4. PHASe:CH2? 
Command 
Format 
PHASe:CH2? [MINimum|MAXimum] 
Function 
Query the initial phase of signals from CH2.  
Return Value 
The query returns any numerical value between -180 and 180, 
such as: 90.000. 
 
5. PHASe:ALIGN 
Command 
Format 
PHASe:ALIGN 
Function 
Enable the dual channels output phase synchronously.  


### DISPlay  *(p.81)*


<!-- page 81 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-69
DISPlay 
DISPlay commands are used for controlling the display of front panel.  
DG1022 supports following DISPlay commands: 
1. 
DISPlay 
2. 
DISPlay? 
3. 
DISPlay:CONTRAST 
4. 
DISPlay:LUMInance 
 
The detailed information of each command are: 
 
1. DISPlay 
Command 
Format 
DISPlay {OFF|ON} 
Function 
Enable or disable the display function of front panel.  
Example 
DISP OFF 
 
2. DISPlay? 
Command 
Format 
DISPlay? 
Function 
Query the state of screen.  
Return Value 
The query returns ON or OFF.  
 
3. DISPlay:CONTRAST 
Command 
Format 
DISPlay:CONTRAST <value> 
Function 
Set the contrast of display within 0~31. 
Example 
DISP:CONTRAST 25 
 
4. DISPlay:LUMInance 
Command 
Format 
DISPlay:LUMInance <value> 
Function 
Set the luminance of display within 0~31. 
Example 
DISP:LUMI 25 


### COUPling  *(p.82)*


<!-- page 82 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-70 
COUPling 
COUPling commands are used for channel coupling or copying.  
DG1022 supports following COUPling commands: 
1. 
COUPling 
2. 
COUPling? 
3. 
COUPling:BASEdchannel 
4. 
COUPling:BASEdchannel? 
5. 
COUPling:PHASEDEViation 
6. 
COUPling:PHASEDEViation? 
7. 
COUPling:FREQDEViation 
8. 
COUPling:FREQDEViation? 
9. 
COUPling:CHANNCopy  
 
 
 
 


<!-- page 83 -->

DG1022 Commands System                                                        RIGOL 
Programming Guide for DG1022 
2-71
The detailed information of each command are: 
 
1. COUPling 
Command 
Format 
COUPling {OFF|ON} 
Function 
Enable or disable coupling function.  
Example 
COUP OFF 
 
2. COUPling? 
Command 
Format 
COUPling? 
Function 
Query the coupling state.  
Return Value 
The query returns OFF or ON. 
 
3. COUPling:BASEdchannel 
Command 
Format 
COUPling:BASEdchannel{:CH1|:CH2} 
 
Function 
Select the base channel while coupling channels.  
Example 
COUP:BASE:CH1 
 
4. COUPling:BASEdchannel? 
Command 
Format 
COUPling:BASEdchannel? 
Function 
Query the base channe that has been selected.  
Return Value 
The query returns CH1 or CH2. 
 
5. COUPling:PHASEDEViation 
Command 
Format 
COUPling:PHASEDEViation <value> 
Function 
Set the phase deviation, the unit is degree.  
Explanations 
<value>: -180°~180° 
Example 
COUP:PHASEDEV 10 
 
6. COUPling:PHASEDEViation? 
Command 
Format 
COUPling:PHASEDEViation? 
Function 
Query the phase deviation.  


<!-- page 84 -->

RIGOL                                                       DG1022 Commands System                   
                                                                                
 Programming Guide for DG1022 
2-72 
Return Value 
The query returns the phase deviation in the form of scientific 
notation, such as: 1.000000e+01. 
 
7. COUPling:FREQDEViation 
Command 
Format 
COUPling:FREQDEViation <value>  
Function 
Set the frequency deviation in Hz.  
Explanations 
<value>: 0Hz~20MHz 
Example 
COUP:FREQDEV 100 
 
8. COUPling:FREQDEViation? 
Command 
Format 
COUPling:FREQDEViation?  
Function 
Query the frequency deviation.  
Return Value 
The query returns the frequency deviation in the form of scientific 
notation, such as: 1.000000e+02. 
 
9. COUPling:CHANNCopy 
Command 
Format 
COUPling:CHANNCopy {1>2|2>1} 
Function 
Copy CH1 to CH2 or copy CH2 to CH1.  
Example 
COUP:CHANNC 1>2 
 


## Application Examples  *(p.85)*


<!-- page 85 -->

Application Examples                                                              RIGOL 
Programming Guide for DG1022 
3-1 
Chapter 3 Application Examples 
 
This chapter shows you how to realize the examples in《DG1022 User’s Guide》via 
command lines, you can compare with the user’s Guide and get deeper understand for 
the usage of commands.  
 
The numbers before every command line in these examples are not the contents of 
command, also for the contents enclosed in “ / * ” and “ * / ” behind every command 
line, which are used to assist user to understand the command well. 
 
Before execute every example, please make sure that all the corresponding devices 
have been connected correctly. 
 


### Example 1: To Generate a Sine Wave  *(p.86)*


<!-- page 86 -->

RIGOL                                                              Application Examples                   
                                                                                
 Programming Guide for DG1022 
3-2 
Example 1: To Generate a Sine Wave  
 
Target: Generate a sine wave with 20 kHz of frequency, 2.5 Vpp of amplitude, 
500mVDC  offset and 10°of phase via CH1. 
 
How to realize via commands? 
 
Method1: 
0 
*IDN? 
 
 
 
 
 
/* Query ID to check the operating state */ 
1 
VOLT:UNIT VPP 
 
 
 
/* Set the unit of amplitude */ 
2 
APPL:SIN 20000,2.5,0.5 
 
/*Set the frequency, amplitude and offset of the 
sine wave*/ 
3 
PHAS 10  
 
 
 
 
/* Set the initial phase */ 
4 
OUTP ON 
 
 
 
 
/*Enable the [Output] connector of CH1 at front 
panel */ 
    
Method2: 
 
0 
*IDN? 
 
 
 
 
 
/* Query ID to check the operating state */ 
1 
FUNC SIN 
 
 
 
 
/*Select sine function*/ 
2 
FREQ 20000  
 
 
 
/* Set the output frequency*/ 
3 
VOLT:UNIT VPP 
 
 
 
/* Set the unit of amplitude*/ 
4 
VOLT 2.5 
 
 
 
 
/* Set the output amplitude */ 
5 
VOLT:OFFS 0.5 
 
 
 
/* Set the offset*/ 
6 
PHAS 10  
 
 
 
 
/* Set the initial phase */ 
7 
OUTP ON 
 
 
 
 
/*Enable the [Output] connector of CH1 at front 
panel */ 
 
Note: 
Command “VOLT:UNIT VPP” and “APPL:SIN 20000,2.5,0.5” are equivalent to these 
five commands together: “FUNC SIN, FREQ 20000”, “VOLT:UNIT VPP”, “VOLT 2.5” and 
“VOLT:OFFS 0.5”. 


### Example 2: To Generate a Built-in Arbitrary Wave  *(p.87)*


<!-- page 87 -->

Application Examples                                                              RIGOL 
Programming Guide for DG1022 
3-3 
Example 2: To Generate a Built-in Arbitrary Wave  
 
Target: Generate an ExpRise wave with 2MHz of frequency, 5VRMS of amplitude, 
10mVDC offset and 60° of phase via CH1. 
 
How to realize via commands? 
 
 
0 
*IDN? 
 
 
 
 
 
/*Query ID to check the operating state */ 
1 
FUNC:USER EXP_RISE  
 
/* Select built-in wave function */ 
2 
FREQ 2000000 
 
 
 
/* Set the output frequency */ 
3 
VOLT:UNIT VRMS  
 
 
/* Set the unit of amplitude */ 
4 
VOLT 5  
 
 
 
 
/*Set the output amplitude */ 
5 
VOLT:OFFS 0.01  
 
 
/* Set the offset */ 
6 
PHAS 60  
 
 
 
 
/*Set the initial phase */ 
7 
OUTP ON 
 
 
 
 
/*Enable the [Output] connector of CH1 at front 
panel */ 
 
 
 
 


### Example 3: To Generate an User-defined Arbitrary Wave  *(p.88)*


<!-- page 88 -->

RIGOL                                                              Application Examples                   
                                                                                
 Programming Guide for DG1022 
3-4 
Example 3: To Generate an User-defined Arbitrary 
Wave  
 
Target: Generate a ramp wave with 10μs of period, 4V of high level and -4V of low 
level. 
 
4
-4
0
2.5
5
7.5
10 μs
Vpp
2
-2
 
 
The vertical resolution of user-defined arbitrary wave is 14 bits, the value from 0 to 
16383 separately corresponds to the minmum and maximum amplitude, that is: -4 V 
corresponds to 0, 0 V corresponds to 8192 and 4 V corresponds to 16383. So, edit the 
points in following table is enough.   
 
Point Time Value 
(voltage) Value 
1 
0s 
(0V) 8192 
2 
2.5μs 
(4V) 16383 
3 
5μs 
(0V) 8192 
4 
7.5μs 
(-4V) 0 
 
How to realize via commands? 
 
0 
*IDN? 
 
 
 
 
 
/*Query ID to check the operating state */ 
1 
FUNC USER  
 
 
 
/*select user-defined arbitrary wave*/ 
2 
FREQ 100000 
 
 
 
/* Set the frequency as 100kHz (period: 10μs)*/  
3 
VOLT:UNIT VPP 
 
 
 
/* Set the unit of amplitude*/ 
4 
VOLT:HIGH 4  
 
 
 
/* Set the high level*/ 
5 
VOLTage:LOW -4  
 
 
/*Set the low level*/ 
6 
DATA:DAC VOLATILE,8192,16383,8192,0 
① 
② 
① 
③ 
④ 


<!-- page 89 -->

Application Examples                                                              RIGOL 
Programming Guide for DG1022 
3-5 
/*Load the 4 decimal numbers to volatile  
    memory */  
7 
FUNC:USER VOLATILE  
 
/*Output the waves in volatile memory */  
8 
OUTP ON 
 
 
 
 
/* Enable the [Output] connector of CH1 at front 
panel */   
 
 


### Example 4: To Generate a FSK Wave  *(p.90)*


<!-- page 90 -->

RIGOL                                                              Application Examples                   
                                                                                
 Programming Guide for DG1022 
3-6 
Example 4: To Generate a FSK Wave 
 
Target: Generate a FSK wave with: 10 kHz, 5 Vpp, 0 VDC of carrier wave, internal 
modulation source, 800 Hz of hop frequency and 200 Hz of FSK rate. 
 
How to realize via commands? 
 
0 
*IDN? 
 
 
 
 
 
/* Query ID to check the operating state */ 
1 
FUNC SIN 
 
 
 
 
/*Select carrier function*/ 
2 
FREQ 10000  
 
 
 
/* Set the frequency of carrier*/ 
3 
VOLT:UNIT VPP 
 
 
 
/* Set the amplitude unit of carrier */ 
4 
VOLT 5  
 
 
 
 
/*Set the amplitude of carrier */ 
5 
VOLT:OFFS 0  
 
 
 
/* Set the offset of carrier */ 
6 
FSK:STAT ON 
 
 
 
/* Enable FSK function*/ 
7 
FSK:SOUR INT 
 
 
 
/* Select internal modulation source */ 
8 
FSK:FREQ 800 
 
 
 
/* Set the hop frequency */ 
9 
FSK:INT:RATE 200 
 
 
/* Set the FSK rate*/ 
10 OUTP ON 
 
 
 
 
/* Enable the [Output] connector of CH1 at front 
panel */ 
 
 
 


### Example 5: To Generate a Linear Sweep Wave  *(p.91)*


<!-- page 91 -->

Application Examples                                                              RIGOL 
Programming Guide for DG1022 
3-7 
Example 5: To Generate a Linear Sweep Wave  
 
Target: Generate a sweep sine wave with: 100 Hz ~ 10 kHz of frequency range, 
internal trigger, linear mode and 1 s of sweep time. 
 
How to realize via commands? 
 
0 
*IDN? 
 
 
 
 
 
/* Query ID to check the operating state */  
1 
FUNC SIN 
 
 
 
 
/* Select the sweep function */ 
2 
SWE:STAT ON 
 
 
 
/* Enable sweep state*/ 
3 
SWE:SPAC LIN 
 
 
 
/* Select linear sweep mode */ 
4 
FREQ:STAR 100  
 
 
/* Set the start frequency */ 
5 
FREQ:STOP 10000 
 
 
/* Set the stop frequency */ 
6 
SWE:TIME 1  
 
 
 
/* Set the sweep time */  
7 
TRIG:SOUR IMM  
 
 
/* Select internal trigger source */ 
8 
OUTP ON 
 
 
 
 
/* Enable the [Output] connector of CH1 at front 
panel */  
 
 
 


### Example 6: To Generate a Burst Wave  *(p.92)*


<!-- page 92 -->

RIGOL                                                              Application Examples                   
                                                                                
 Programming Guide for DG1022 
3-8 
Example 6: To Generate a Burst Wave 
 
Target: Generate a burst with: 3-cycle of square, 0° of initial phase, 10 ms of burst 
period and adopt internal trigger. 
 
How to realize via commands? 
 
0 
*IDN? 
 
 
 
 
 
/* Query ID to check the operating state */ 
1 
FUNC SQU 
 
 
 
 
/* Select burst function */ 
2 
BURS:STAT ON 
 
 
 
/* Enable burst state */ 
3 
BURS:MODE TRIG 
 
 
/* Select the burst mode */ 
4 
BURS:NCYC 3 
 
 
 
/* Set the cycle number */ 
5 
BURS:PHAS 0 
 
 
 
/* Set the initial phase*/ 
6 
BURS:INT:PER 0.01 
 
 
/* Set the period */ 
7 
TRIG:SOUR IMM  
 
 
/* Select internal trigger source */ 
8 
OUTP ON 
 
 
 
 
/* Enable the [Output] connector of CH1 at front 
panel */ 
    
 
 


### Example 7: To Output Waves via Dual Channels  *(p.93)*


<!-- page 93 -->

Application Examples                                                              RIGOL 
Programming Guide for DG1022 
3-9 
Example 7: To Output Waves via Dual Channels  
 
Target: Output a sine wave with 1kHz, 2.5Vpp, 500mVDC, 10° via CH1 and a ramp 
wave with 1.5kHz, 5Vpp, 1 VDC, 20° via CH2. 
 
 
How to realize via commands? 
 
0 
*IDN? 
 
 
 
 
 
/* Query ID to check the operating state */  
1 
VOLT:UNIT VPP 
 
 
 
/* Set the amplitude unit of CH1 */ 
2 
APPL:SIN 1000,2.5,0.5 
 
/* Set the frequency, amplitude and offset of sine 
wave from CH1 */ 
3 
PHAS 10  
 
 
 
 
/* Set the initial phase of wave from CH1 */ 
4 
OUTP ON 
 
 
 
 
/* Enable the [Output] connector of CH1 at front 
panel */ 
5 
VOLT:UNIT:CH2 VPP  
 
/* Set the amplitude unit of CH2*/ 
6 
APPL:RAMP:CH2 1500,5,1  
/*Set the frequency, amplitude and offset of 
ramp wave from CH2*/ 
7 
PHAS:CH2 20 
 
 
 
/* Set the initial phase of wave from CH2*/ 
8 
OUTP:CH2 ON 
 
 
 
/* Enable the [Output] connector of CH2 at front 
panel */ 
9 
PHAS:ALIGN  
 
 
 
/*Control the dual channels phase output 
synchronously */ 
 
 
 
 


### Example 8: Channel Coupling  *(p.94)*


<!-- page 94 -->

RIGOL                                                              Application Examples                   
                                                                                
 Programming Guide for DG1022 
3-10 
Example 8: Channel Coupling  
 
Target: Output a sine wave with 1kHz, 5Vpp, 0VDC, 0° via CH1 and a ramp wave with 
1.5kHz, 5Vpp, 0 VDC, 0° via CH2, and then, take CH1 as the base channel and Set the 
phase deviation as 10°, finally, observe the phase of wave from CH2 after coupling. 
 
How to realize via commands? 
 
0 
*IDN? 
 
 
 
 
 
/* Query ID to check the operating state */ 
1 
VOLT:UNIT VPP 
 
 
 
/* Set the amplitude unit of CH1 */ 
2 
APPL:SIN 1000,5,0 
 
 
/* Set the frequency, amplitude and offset of sine 
wave from CH1 */ 
3 
PHAS 0  
 
 
 
 
/* Set the initial phase of wave from CH1*/ 
4 
VOLT:UNIT:CH2 VPP  
 
/* Set the amplitude unit of CH2*/ 
5 
APPL:RAMP:CH2 1500,5,0  
/* Set the frequency, amplitude and offset of 
ramp wave from CH2*/ 
6 
PHAS:CH2 0  
 
 
 
/* Set the initial phase of wave from CH2*/ 
7 
COUP ON 
 
 
 
 
/* Enable channel coupling function */ 
8 
COUP:BASE:CH1  
 
 
/* Select CH1 as the base channel */ 
9 
COUP:PHASEDEV 10  
 
/* Set up the phase deviation */ 
10 PHAS 2  
 
 
 
 
/*Change the phase of waves output from CH1*/ 
11 PHAS:CH2?  
 
 
 
/*Query the phase of waves output from CH2 */ 
   
Notes: 
1 
The return value of “PHAS:CH2?” is 12, which indicates that the phase of CH2 is 
vary with the phase of CH1 and keeps 10° of phase deviation. 
2 
The way to set frequency coupling is the same as phase coupling.  
 


### Example 9: Channel Copy  *(p.95)*


<!-- page 95 -->

Application Examples                                                              RIGOL 
Programming Guide for DG1022 
3-11
Example 9: Channel Copy  
 
Target: Output a sine wave with 1kHz, 5Vpp, 500mVDC, 10° via CH1 and a ramp wave 
with 1.5kHz, 2Vpp, 0 VDC, 0° via CH2, and then observe the parameters of wave from 
CH2 after copying CH1 to CH2. 
 
How to realize via commands? 
 
0 
*IDN? 
 
 
 
 
 
/* Query ID to check the operating state */ 
1 
VOLT:UNIT VPP 
 
 
 
/* Set the amplitude unit of CH1*/ 
2 
APPL:SIN 1000,5,0.5  
 
/* Set the frequency, amplitude and offset of sine 
wave from CH1*/ 
3 
PHAS 10  
 
 
 
 
/* Set the initial phase of wave from CH1*/ 
4 
VOLT:UNIT:CH2 VPP  
 
/* Set the amplitude unit of CH2*/ 
5 
APPL:RAMP:CH2 1500,2,0  
/* Set the frequency, amplitude and offset of 
ramp wave from CH2*/ 
6 
PHAS:CH2 0  
 
 
 
/* Set the initial phase of wave from CH2*/ 
7 
COUP OFF 
 
 
 
 
/* Disable channel coupling to enable channel 
copy */ 
8 
COUP:CHANNC 1>2 
/* Copy the wave parameters from CH1 to CH2 */ 
/* Query the wave parameters of CH2 after copying */ 
9 
FREQuency:CH2?  
 
 
/* Return 1.000000e+03 (1kHz)*/ 
10 VOLTage:CH2? 
 
 
 
/* Return 5.000000e+00 (5Vpp)*/ 
11 VOLTage:OFFSet:CH2?  
 
/* Return 5.000000e-01 (500mVDC )*/ 
12 PHAS:CH2?   
 
 
 
/* Return 10.000 (10°)*/ 
 
Notes: 
1 
Channel Copy function is only valid for wave parameters but not for wave shapes.  
2 
Channel Copy function is enabled automatically after Channel Coupling is 
disabled. 
3 
Channel Copy function is limited by parameter verification, for the details please 
refer to <<DG1022 User’s Guide>>. 
 


<!-- page 96 -->



## Appendix: Commands Reference A-Z  *(p.97)*


<!-- page 97 -->

Appendix: Commands Reference A-Z                                                RIGOL 
 Programming Guide for DG1022 
1
Appendix: Commands Reference A-Z 
 
*IDN?  2-2 
 
A 
AM:SOURce  2-36 
AM:SOURce?  2-36 
AM:INTernal:FUNCtion  2-36 
AM:INTernal:FUNCtion?  2-36 
AM:INTernal:FREQuency  2-36 
AM:INTernal:FREQuency?  2-36 
AM:DEPTh  2-37 
AM:DEPTh?  2-37 
AM:STATe  2-37 
AM:STATe?  2-37 
APPLy:SINusoid  2-4 
APPLy:SQUare  2-4 
APPLy:RAMP  2-4 
APPLy:PULSe  2-5 
APPLy:NOISe  2-5 
APPLy:DC  2-5 
APPLy:USER  2-6 
APPLy?  2-6 
APPLy:SINusoid:CH2  2-6 
APPLy:SQUare:CH2  2-6 
APPLy:RAMP:CH2  2-7 
APPLy:PULSe:CH2  2-7 
APPLy:NOISe:CH2  2-7 
APPLy:DC:CH2  2-7 
APPLy:USER:CH2  2-8 
APPLy:CH2?  2-8 
 
B 
BURSt:MODE  2-54 
BURSt:MODE?  2-54 
BURSt:NCYCles  2-54 
BURSt:NCYCles?  2-54 
BURSt:INTernal:PERiod  2-55 
BURSt:INTernal:PERiod?  2-55 
BURSt:PHASe  2-55 
BURSt:PHASe?  2-55 
BURSt:STATe  2-55 
BURSt:STATe?  2-55 
BURSt:GATE:POLarity  2-56 
BURSt:GATE:POLarity?  2-56 
 
C 
COUPling  2-71 
COUPling?  2-71 
COUPling:BASEdchannel  2-71 
COUPling:BASEdchannel?  2-71 
COUPling:PHASEDEViation  2-71 
COUPling:PHASEDEViation?  2-71 
COUPling:FREQDEViation  2-72 
COUPling:FREQDEViation?  2-72 
COUPling:CHANNCopy  2-72 
 
D 
DATA  2-58 
DATA:DAC  2-58 
DATA:COPY  2-59 
DATA:DELete  2-59 
DATA:CATalog?  2-59 
DATA:RENAME  2-60 
DATA:NVOLatile:CATalog?  2-60 
DATA:NVOLatile:FREE?  2-60 
DATA:ATTRibute:POINts?  2-60 
DATA:LOAD  2-60 
DISPlay  2-69 
DISPlay?  2-69 


<!-- page 98 -->

RIGOL                                                Appendix: Commands Reference A-Z 
                                                                                
 Programming Guide for DG1022 
2
DISPlay:CONTRAST  2-69 
DISPlay:LUMInance  2-69 
 
F 
FM:SOURce  2-39 
FM:SOURce?  2-39 
FM:INTernal:FUNCtion  2-39 
FM:INTernal:FUNCtion?  2-39 
FM:INTernal:FREQuency  2-39 
FM:INTernal:FREQuency?  2-39 
FM:DEViation  2-40 
FM:DEViation?  2-40 
FM:STATe  2-40 
FM:STATe?  2-40 
FREQuency  2-17 
FREQuency?  2-17 
FREQuency:CH2  2-17 
FREQuency:CH2?  2-17 
FREQuency:STARt  2-17 
FREQuency:STARt?  2-18 
FREQuency:STOP  2-18 
FREQuency:STOP?  2-18 
FREQuency:CENTer  2-18 
FREQuency:CENTer?  2-18 
FREQuency:SPAN  2-19 
FREQuency:SPAN?  2-19 
FSK:SOURce  2-45 
FSK:SOURce?  2-45 
FSK:FREQuency  2-45 
FSK:FREQuency?  2-45 
FSK:INTernal:RATE  2-45 
FSK:INTernal:RATE?  2-45 
FSK:STATe  2-46 
FSK:STATe?  2-46 
FUNCtion  2-11 
FUNCtion?  2-11 
FUNCtion:USER  2-11 
FUNCtion:USER?  2-12 
FUNCtion:SQUare:DCYCle  2-12 
FUNCtion:SQUare:DCYCle?  2-12 
FUNCtion:RAMP:SYMMetry  2-12 
FUNCtion:RAMP:SYMMetry?  2-13 
FUNCtion:CH2  2-13 
FUNCtion:CH2?  2-13 
FUNCtion:USER:CH2  2-13 
FUNCtion:USER:CH2?  2-14 
FUNCtion:SQUare:DCYCle:CH2  2-14 
FUNCtion:SQUare:DCYCle:CH2?  2-14 
FUNCtion:RAMP:SYMMetry:CH2  2-14 
FUNCtion:RAMP:SYMMetry:CH2?  2-15 
 
M 
MEMory:STATe:NAME  2-62 
MEMory:STATe:NAME?  2-62 
MEMory:STATe:DELete  2-62 
MEMory:STATe:RECall:AUTO  2-62 
MEMory:STATe:RECall:AUTO?  2-62 
MEMory:STATe:VALid?  2-62 
MEMory:NSTates?  2-63 
 
O 
OUTPut  2-27 
OUTPut?  2-27 
OUTPut:LOAD  2-27 
OUTPut:LOAD?  2-27 
OUTPut:POLarity  2-27 
OUTPut:POLarity?  2-28 
OUTPut:SYNC  2-28 
OUTPut:SYNC?  2-28 
OUTPut:TRIGger:SLOPe  2-28 
OUTPut:TRIGger:SLOPe?  2-28 
OUTPut:TRIGger  2-29 
OUTPut:TRIGger?  2-29 
OUTPut:CH2  2-29 
OUTPut:CH2?  2-29 
OUTPut:LOAD:CH2  2-29 


<!-- page 99 -->

Appendix: Commands Reference A-Z                                                RIGOL 
Programming Guide for DG1022 
3
OUTPut:LOAD:CH2?  2-29 
OUTPut:POLarity:CH2  2-30 
OUTPut:POLarity:CH2?  2-30 
 
P 
PHASe  2-68 
PHASe?  2-68 
PHASe:CH2  2-68 
PHASe:CH2?  2-68 
PHASe:ALIGN  2-68 
PM:SOURce  2-42 
PM:SOURce?  2-42 
PM:INTernal:FUNCtion  2-42 
PM:INTernal:FUNCtion?  2-42 
PM:INTernal:FREQuency  2-42 
PM:INTernal:FREQuency?  2-42 
PM:DEViation  2-43 
PM:DEViation?  2-43 
PM:STATe  2-43 
PM:STATe?  2-43 
PULSe:PERiod  2-32 
PULSe:PERiod?  2-32 
PULSe:WIDTh  2-32 
PULSe:WIDTh?  2-32 
PULSe:DCYCle  2-32 
PULSe:DCYCle?  2-32 
PULSe:PERiod:CH2  2-33 
PULSe:PERiod:CH2?  2-33 
PULSe:WIDTh:CH2  2-33 
PULSe:WIDTh:CH2?  2-33 
PULSe:DCYCle:CH2  2-33 
PULSe:DCYCle:CH2?  2-33 
 
S 
SWEep:SPACing  2-48 
SWEep:SPACing?  2-48 
SWEep:TIME  2-48 
SWEep:TIME?  2-48 
SWEep:STATe  2-48 
SWEep:STATe?  2-49 
SYSTem:ERRor?  2-65 
SYSTem:VERSion?  2-65 
SYSTem:BEEPer:STATe  2-65 
SYSTem:BEEPer:STATe?  2-65 
SYSTem:LOCal   2-65 
SYSTem:RWLock  2-65 
SYSTem:REMote  2-66 
SYSTem:CLKSRC  2-66 
SYSTem:LANGuage  2-66 
 
T 
TRIGger:SOURce  2-51 
TRIGger:SOURce?  2-51 
TRIGger:SLOPe  2-51 
TRIGger:SLOPe?  2-51 
TRIGger:DELay  2-51 
TRIGger:DELay?  2-52 
 
V 
VOLTage  2-21 
VOLTage?  2-21 
VOLTage:HIGH  2-21 
VOLTage:HIGH?  2-21 
VOLTage:LOW  2-21 
VOLTage:LOW?  2-22 
VOLTage:OFFSet  2-22 
VOLTage:OFFSet?  2-22 
VOLTage:UNIT  2-22 
VOLTage:UNIT?  2-22 
VOLTage:CH2  2-22 
VOLTage:CH2?  2-22 
VOLTage:HIGH:CH2  2-23 
VOLTage:HIGH:CH2?  2-23 
VOLTage:LOW:CH2  2-24 
VOLTage:LOW:CH2?  2-24 
VOLTage:OFFSet:CH2  2-24 


<!-- page 100 -->

RIGOL                                                Appendix: Commands Reference A-Z 
                                                                                
 Programming Guide for DG1022 
4
VOLTage:OFFSet:CH2?  2-24 
VOLTage:UNIT:CH2  2-24 
VOLTage:UNIT:CH2?  2-25
 
