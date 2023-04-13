import pandas as pd # optional
import numpy as np

def upward_trend( trend , start_value , max_value  ) :

    if trend < 0 : 
      trend = 0 
      trend += 1
    else:
      trend += 1
    if abs(trend) >  max_value /  start_value :     
        trend = round(max_value /  start_value)
    multiplier = abs(trend - 1)
    return trend , multiplier

def downward_trend(trend , start_value , max_value ) :

    if trend > 0 :
      trend = 0 
      trend += -1
    else:
      trend += -1
    if abs(trend) >  max_value /  start_value :     
        trend = round(max_value /  start_value)    
    multiplier = abs(trend - 1)
    return trend , multiplier

  
def parabolic_sar(bar , step_size =None , max_value=None , start_value=None):

    if not step_size or max_value or start_value:
        step_size= 0.02
        start_value = 0.02 
        max_value = 0.2
    low = np.array( bar["Low"] , dtype=np.float16)
    high = np.array( bar["High"] , dtype=np.float16)

    period = 5
    sar_array = np.empty_like( high , dtype=np.float16)
    sar_array = np.full( high.shape , np.nan)
    trend = 0
    for n in range(period , len(sar_array)+1 ):
        
        if high[n-1:n] > high[n-period] : # Upward trend validity 
            # high[n-1:n] --> current bar high        # high[n-period] --> n-4 bar high
            trend , multiplier = upward_trend( trend , start_value , max_value )
            old_sar = min( low[n-period:n] , sar_array[n-1]  )
            extreme_point = max( high[n-period:n] )                       

            a_factor = start_value + multiplier * step_size
            sar_array[n-1] =  old_sar + a_factor * (extreme_point - old_sar) 
                                                                                    

        elif high[n-period] > high[n-1:n] : # Downward trend validity 

            trend , multiplier =  downward_trend(trend , start_value , max_value )
            old_sar = max( high[n-period:n] , sar_array[n-1]  )  
            extreme_point = min( high[n-period:n] )                       

            a_factor = start_value + multiplier * step_size
                                                                                        
            sar_array[n-1] =  old_sar - a_factor * (extreme_point - old_sar)                                

    return sar_array   
