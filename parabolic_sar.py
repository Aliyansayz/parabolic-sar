## EXAMPLE ##
# bars["sar_value"] = parabolic_sar(bars)
import numpy as np
import pandas as pd

## PARABOLIC SAR ## 
def fall_sar(sar , a_factor , ep ):
  
  return sar - a_factor * (ep - sar) 

def rise_sar(sar , a_factor , ep ):

  return sar + a_factor * (ep - sar) 

def parabolic_sar(bars , step_size =None , max_value=None , start_value=None):
  
  if not step_size or max_value or start_value:
    step_size= 0.02
    start_value = 0.02 
    max_value = 0.2
  
  bar_low = bars.Low 
  bar_high = bars.High
  sar_array = np.empty_like(bar_high , dtype=np.float16)
  sar_array = np.full( bar_high.shape , np.nan)

  trend_count = 0
  added = bar_low[0] + bar_high[0]
  sar =  added/2
  sar_array[0] = sar
  
  if bar_high[1] > bar_high[0]:
    trend_count += 1  
    sar = min(bar_low[1] , bar_low[0])
    ep = max(bar_high[1] , bar_high[0])
    a_factor = start_value + abs(trend_count-1) * step_size

  elif  bar_high[1] < bar_high[0]:
    trend_count += -1  
    sar = max(bar_high[1] , bar_high[0])
    ep = min(bar_low[1] , bar_low[0])
    a_factor = start_value + abs(trend_count-1) * step_size
  
  
  sar_array[1] = sar

  
  for n in range(2, len(bars)):
      
      if  bar_low[n] <  sar_array[n-1]  and trend_count > 0 :  # reversal towards downtrend
        trend_count = 0
        trend_count += -1 
        # fsar = fall_sar( sar_array[n-1]  , a_factor , ep )
        # sar = max( bar_high[n] , bar_high[n-1] )
        ep = min(bar_low[n] , bar_low[n-1])
        a_factor = start_value + abs(trend_count-1) * step_size

        reversed_sar = fall_sar(sar_array[n-1] , a_factor , ep )
        sar_array[n] = reversed_sar
        continue

      elif   bar_high[n] >  sar_array[n-1]  and trend_count < 0 :  # reversal towards uptrend
        trend_count = 0 
        trend_count += 1 
        # sar = min( bar_low[n] , bar_low[n-1] ) 
        ep = max(bar_high[n] , bar_high[n-1]) 
        a_factor = start_value + abs(trend_count-1) * step_size

        reversed_sar = rise_sar(sar_array[n-1] , a_factor , ep )
        sar_array[n] = reversed_sar
        continue

      if trend_count > 0 :

        # new_SAR = sar + a_factor (ep - sar)
        rsar = rise_sar(sar , a_factor , ep )
        sar = min(rsar , bar_low[n-1] , bar_low[n-2] )
        trend_count += 1
        ep = max(bar_high[n] , bar_high[n-1])

      else:
        # new_SAR = sar - a_factor (ep - sar)
        fsar = fall_sar(sar , a_factor , ep )
        sar = max(fsar , bar_high[n-1] , bar_high[n-2] )
        trend_count += -1
        ep = min(bar_low[n] , bar_low[n-1])

      a_factor = start_value + abs(trend_count-1) * step_size
      sar_array[n] = sar
      if a_factor > max_value : # max accelerator 0.2
        a_factor = max_value 

  return sar_array      
