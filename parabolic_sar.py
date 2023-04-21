import pandas as pd # optional
import numpy as np

def parabolic_sar( bar , step_size = None , max_value = None , start_value = None):
      import numpy as np

      if not step_size or max_value or start_value:
          step_size= 0.02
          start_value = 0.02 
          max_value = 0.2

      low = np.array( bar.Low , dtype=np.float32)
      high = np.array( bar.High , dtype=np.float32)
      
      
      period = 5
      sar_array = np.empty_like( high , dtype=np.float16 )
      extreme_point = np.empty_like( high , dtype=np.float16 )
      extreme_point = np.full( high.shape , np.nan)
      sar_array = np.full( high.shape , np.nan)

      def trend(high ,  low, period, n):
        mean =  np.mean( ( high[ n-period:n ] , low[ n-period:n ]  ) )
        if high[n] > mean : return 1 
        else : return -1 

      def afactor_multiplier_downtrend(n ,period,  low,  start_value , max_value, trend ) :
          if trend > 0 : trend = -1

          pre_low = np.min( ( low[n-period:n-1]  ) ) 
          if low[n] < pre_low: 
              trend += -1 
          multiplier = abs(trend) - 1

          if multiplier >  max_value /  start_value :     
              multiplier = round(max_value /  start_value)

          return  multiplier


      def afactor_multiplier_uptrend(n ,period,  high,  start_value , max_value, trend ) :
          if trend < 0 : trend = 1

          pre_high = np.max( ( high[n-period:n-1]  ) ) 
          if high[n] > pre_high: 
              trend += 1 
          multiplier = trend - 1

          if multiplier >  max_value /  start_value :     
              multiplier = round(max_value /  start_value)

          return  multiplier


      # extreme_point = 
      # sar_array[period-1] = extreme_point
      trend = 0
      for n in range( period , len(sar_array)+1 ):

          trend , multiplier = trend(high ,  low, period, n)

          if trend(high ,  low, period, n) == 1  : # Upward trend validity 
              # high[n-1:n] --> current bar high        # high[n-period] --> n-4 bar high
              multiplier = afactor_multiplier_uptrend(n ,period,  high,  start_value , max_value, trend )
        
              extreme_point =  np.max( ( high[n-period:n] ))

              a_factor = start_value + multiplier * step_size 
              try:
                  old_sar = sar_array[n-1]

              except:
                  old_sar = np.min( ( low[n-period:n-1] ))

              sar_array[n] =  old_sar + a_factor * (extreme_point - old_sar)
                                                                                      
          elif trend(high ,  low, period, n) ==  -1  : # Downward trend validity  
              
              multiplier =  afactor_multiplier_downtrend(n ,period,  high,  start_value , max_value, trend )

              extreme_point = np.min(( low[n-period:n] ))                  
              a_factor = start_value + multiplier * step_size
              try:
                  old_sar = sar_array[n-1]  

              except:
                  old_sar = np.max( ( high[n-period:n-1] ))
                                                                                         
              sar_array[n]  =  old_sar - a_factor * (extreme_point - old_sar)                                
      
      return sar_array 
