#include <formatio.h>
#include <ansi_c.h>
#include <advanlys.h>
#include <cvirte.h>		
#include <userint.h>
#include "Kyle_MukulEx2.h"
#include <NIDAQmx.h>
static char savedfile[300];


static int initTime;
static int32 actualSamples;
static uInt32 arraySizeSample;
double *voltageArray;
double *xArray;
static char input[1];
static char taskName[1];
static TaskHandle firstTask;
static int finalTime;
static double frequency;
static double timeRange;
double *frequencyarray;
double *spectrumArray;

static int panelHandle;

int main (int argc, char *argv[])
{
	if (InitCVIRTE (0, argv, 0) == 0)
		return -1;	/* out of memory */
	if ((panelHandle = LoadPanel (0, "Kyle_MukulEx2.uir", PANEL)) < 0)
		return -1;
	DisplayPanel (panelHandle);
	RunUserInterface ();
	DiscardPanel (panelHandle);
	return 0;
}

int CVICALLBACK Bye (int panel, int control, int event,
					 void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			QuitUserInterface (0);

			break;
	}
	return 0;
}

int CVICALLBACK acquireData (int panel, int control, int event,
							 void *callbackData, int eventData1, int eventData2)
{
	int inputGraphHandle;
	switch (event)
	{
		case EVENT_COMMIT:
			GetCtrlVal (panelHandle, PANEL_timeRange, &timeRange);
			GetCtrlVal (panelHandle, PANEL_frequency, &frequency);
			arraySizeSample=timeRange*frequency;
			voltageArray=(double*)malloc((arraySizeSample)*sizeof(double));
			
			DAQmxCreateTask (taskName, &firstTask);
			DAQmxCreateAIVoltageChan (firstTask, "Dev1/ai0", "", DAQmx_Val_Diff, -10.0, 10.0, DAQmx_Val_Volts, "");
			DAQmxCfgSampClkTiming (firstTask, "OnboardClock", frequency, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, arraySizeSample);
			DAQmxStartTask (firstTask);
			DAQmxReadAnalogF64 (firstTask, arraySizeSample, timeRange, DAQmx_Val_GroupByChannel, voltageArray, arraySizeSample, &actualSamples, 0);
			DAQmxStopTask (firstTask);
				 (firstTask);
			
			xArray=(double*)malloc((arraySizeSample)*sizeof(double));

			for(int i=0;i<arraySizeSample;i++){
				xArray[i]=i/frequency;
			}
			//----Plotting-----
			PlotXY (panelHandle, PANEL_graph_Frequency, xArray, voltageArray, arraySizeSample, VAL_DOUBLE, VAL_DOUBLE, VAL_THIN_LINE, VAL_EMPTY_SQUARE, VAL_SOLID, 1, VAL_RED);
			break;
	}
	return 0;
}


int CVICALLBACK saveFrequency (int panel, int control, int event,
							   void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			double savedFrequencyArray[arraySizeSample*2];

			for(int i=0;i<arraySizeSample*2;i++){
			if(i<arraySizeSample){
				savedFrequencyArray[i]=frequencyarray[i];
			}
			if(i>arraySizeSample){
				savedFrequencyArray[i]=spectrumArray[i-arraySizeSample];
			}
			}
			FileSelectPopup ("", "*.*", "", "", VAL_SAVE_BUTTON, 0, 0, 1, 0, savedfile);
			ArrayToFile (savedfile, savedFrequencyArray, VAL_DOUBLE, arraySizeSample*2, 2, VAL_GROUPS_TOGETHER, VAL_GROUPS_AS_COLUMNS, VAL_CONST_WIDTH, 10, VAL_ASCII, VAL_TRUNCATE);
			break;
	}
	return 0;
}

int CVICALLBACK saveTime (int panel, int control, int event,
						  void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			double savedTimeArray[arraySizeSample*2];
			for(int i=0;i<arraySizeSample*2;i++){
			if(i<arraySizeSample){
				savedTimeArray[i]=xArray[i];
			}
			if(i>=arraySizeSample){
				savedTimeArray[i]=voltageArray[i-arraySizeSample];
			}
			}
			FileSelectPopup ("", "*.*", "", "", VAL_SAVE_BUTTON, 0, 0, 1, 0, savedfile);
			ArrayToFile (savedfile, savedTimeArray, VAL_DOUBLE, arraySizeSample*2, 2, VAL_GROUPS_TOGETHER, VAL_GROUPS_AS_COLUMNS, VAL_CONST_WIDTH, 10, VAL_ASCII, VAL_TRUNCATE);
			
			break;
	}
	return 0;
}

int CVICALLBACK transform (int panel, int control, int event,
						   void *callbackData, int eventData1, int eventData2)
{
	switch (event)
	{
		case EVENT_COMMIT:
			frequencyarray=(double*)malloc((arraySizeSample)*sizeof(double));
			for(int i =0;i<arraySizeSample;i++){
				frequencyarray[i]=i/timeRange;
			}
			spectrumArray=(double*)malloc((arraySizeSample)*sizeof(double));
			for(int i =0; i<arraySizeSample;i++){
				spectrumArray[i]=voltageArray[i];
			}
			Spectrum (spectrumArray, arraySizeSample);
			PlotXY (panelHandle, PANEL_fourier,frequencyarray, spectrumArray, arraySizeSample, VAL_DOUBLE, VAL_DOUBLE, VAL_THIN_LINE, VAL_EMPTY_SQUARE, VAL_SOLID, 1, VAL_RED);
			
			break;
	}
	return 0;
}
