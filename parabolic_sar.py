import pandas as pd # optional

def parabolic_sar( bar , step_size = None ,  start_value = None, max_value = None  ):
      import numpy as np
      import math

      if not step_size or max_value or start_value:
          step_size= 0.02
          start_value = 0.02 
          max_value = 0.2

      low = np.array( bar.Low , dtype=np.float32)
      high = np.array( bar.High , dtype=np.float32)
      close = np.array( bar.Close , dtype=np.float32)
      
      period = 5
      sar_array = np.empty_like( high , dtype=np.float16 )
      extreme_point = np.empty_like( high , dtype=np.float16 )
      a_factor = np.empty_like( high , dtype=np.float16 )

      trend = 0
      a_factor = np.full(  high.shape , np.nan )
      extreme_point = np.full( high.shape , np.nan )
      sar_array = np.full( high.shape , np.nan )

      def trend_direction(high, low, sar_array, n):
        if  high[n] > sar_array[n-1] : return 1 
        elif low[n] < sar_array[n-1] : return -1 
        
      def trend_now(high ,  low):
        mean =  np.mean(( high[:5] , low[:5]  ))
        if close[5] > mean  : return 1 # previous parabolic sar value 
        else : return -1 

      if trend_now(high , low) == 1 : 
        extreme_point[4] = np.max( ( high[:4] ))
        sar_array[4] = extreme_point[4]
      else:   
        extreme_point[4] = np.min( ( low[:4] ))
        sar_array[4] = extreme_point[4]
      a_factor[4] = start_value 

      def afactor_multiplier_downtrend(n ,period,  low,  start_value , max_value, trend ) :
          if trend >= 0 : trend = -1
          pre_low = np.min( ( low[n-period:n-1]  ) ) 
          if low[n] < pre_low: 
              trend += -1 
          multiplier = abs(trend) - 1
          if multiplier >  max_value /  start_value :     
              multiplier = round(max_value /  start_value)
          return  multiplier

      def afactor_multiplier_uptrend(n ,period,  high,  start_value , max_value, trend ) :
          if trend <= 0 : trend = 1
          pre_high = np.max( ( high[n-period:n-1]  ) ) 
          if high[n] > pre_high: 
              trend += 1 
          multiplier = trend - 1
          if multiplier >  max_value /  start_value :     
              multiplier = round(max_value /  start_value)
          return  multiplier

      for n in range( period , len(sar_array) ):
          direction =  trend_direction(high, low, sar_array, n)
          if direction == 1  :                              # Upward trend validity 
              # high[n-1:n] --> current bar high        # high[n-period] --> n-4 bar high
              multiplier = afactor_multiplier_uptrend(n ,period,  high,  start_value , max_value, trend )
        
              extreme_point[n] =  np.max( ( high[n-period:n] ))
              a_factor[n] = start_value + multiplier * step_size 
              prior_sar = sar_array[n-1]
              sar_array[n] =  sar_array[n-1]   + a_factor[n-1] * (extreme_point[n-1] - sar_array[n-1]   )
                                                                                      
          elif direction ==  -1  : # Downward trend validity  
              
              multiplier =  afactor_multiplier_downtrend(n, period,  high,  start_value , max_value, trend )

              extreme_point[n] = np.min(( low[n-period:n] ))                  
              a_factor[n] = start_value + multiplier * step_size
                          
              sar_array[n]  =  sar_array[n-1]    - a_factor[n-1] * (extreme_point[n-1] - sar_array[n-1]  )                                
      
      return sar_array 
