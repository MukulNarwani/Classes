/**************************************************************************/
/* LabWindows/CVI User Interface Resource (UIR) Include File              */
/*                                                                        */
/* WARNING: Do not add to, delete from, or otherwise modify the contents  */
/*          of this include file.                                         */
/**************************************************************************/

#include <userint.h>

#ifdef __cplusplus
    extern "C" {
#endif

     /* Panels and Controls: */

#define  PANEL                            1
#define  PANEL_quit                       2       /* control type: command, callback function: Bye */
#define  PANEL_acquireData                3       /* control type: command, callback function: acquireData */
#define  PANEL_frequency                  4       /* control type: numeric, callback function: (none) */
#define  PANEL_timeRange                  5       /* control type: numeric, callback function: (none) */
#define  PANEL_graph_Frequency            6       /* control type: graph, callback function: (none) */
#define  PANEL_fourier                    7       /* control type: graph, callback function: (none) */
#define  PANEL_saveTime                   8       /* control type: command, callback function: saveTime */
#define  PANEL_saveFrequency              9       /* control type: command, callback function: saveFrequency */
#define  PANEL_TRANSFORM                  10      /* control type: command, callback function: transform */


     /* Control Arrays: */

          /* (no control arrays in the resource file) */


     /* Menu Bars, Menus, and Menu Items: */

          /* (no menu bars in the resource file) */


     /* Callback Prototypes: */

int  CVICALLBACK acquireData(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK Bye(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK saveFrequency(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK saveTime(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);
int  CVICALLBACK transform(int panel, int control, int event, void *callbackData, int eventData1, int eventData2);


#ifdef __cplusplus
    }
#endif