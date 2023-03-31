## EXAMPLE ##
# bars["sar_value"] = parabolic_sar(bars)


## PARABOLIC SAR ## 
def fall_sar(sar , a_factor , ep ):

  return sar - a_factor (ep - sar) 

def rise_sar(sar , a_factor , ep ):

  return sar + a_factor (ep - sar) 

def parabolic_sar(bars):

  trend_count = 0
  sar_list = []
  for i in range(1, len(bars)+1):
    # bar_low = bars.Low 
    # bar_high = bars.High
    
    if n == 1 :
      added = bar_low[n] + bar_high[n]
      sar =  added/2
      sar_list.append(sar)

    if n < 3 :

      if bar_high[n] > bar_high[n-1]:
        trend_count += 1  
        sar = min(bar_low[n] , bar_low[n-1])
        ep = max(bar_high[n] , bar_high[n-1])
        a_factor = 0.02 + abs(trend_count) * 0.02 

      elif  bar_high[n] < bar_high[n-1]:
        trend_count += -1  
        sar = max(bar_high[n] , bar_high[n-1])
        a_factor = 0.02 + abs(trend_count-1) * 0.02 

      else:
        added= (bar_low[n-1] + bar_low[n] + bar_high[n-1] + bar_high[n]  )
        sar = added / 4

      sar_list.append(sar)
      
    else:

        if current_SAR > bar_low[n] and trend_count > 0 :  # reversal towards downtrend
          trend_count = 0
          trend_count += -1 
          sar = max( bar_max[n] , bar_max[n-1] )
          ep = max(bar_high[n] , bar_high[n-1])
          a_factor = 0.02 + abs(trend_count-1) * 0.02 

          reversed_sar = fall_sar(sar , a_factor , ep )
          sar_list.append(reversed_sar) # append
          continue

        elif  current_SAR < bar_high[n] and trend_count < 0 :  # reversal towards uptrend
          trend_count = 0 
          trend_count += 1 
          sar = min( bar_low[n] , bar_low[n-1] ) 
          ep = min(bar_high[n] , bar_high[n-1]) 
          a_factor = 0.02 + abs(trend_count-1) * 0.02 

          reversed_sar = rise_sar(sar , a_factor , ep )
          sar_list.append(reversed_sar) # append
          continue

        if trend_count > 0 :

          # new_SAR = sar + a_factor (ep - sar)
          sar_ = rise_sar(sar , a_factor , ep )
          sar = min(sar_ , bar_low[n-1] , bar_low[n-2] )
          trend_count += 1
          ep = max(bar_high[n] , bar_high[n-1])
    
        else:
          # new_SAR = sar - a_factor (ep - sar)
          sar_ = fall_sar(sar , a_factor , ep )
          sar = max(sar_ , bar_max[n-1] , bar_max[n-2] )
          trend_count += -1
          ep = max(bar_high[n] , bar_high[n-1])
          
        a_factor = 0.02 + abs(trend_count-1) * 0.02 
        current_SAR = SAR_value
        sar_list.append(current_SAR) # append
        if a_factor > 0.2 :
          a_factor = 0.2
  return sar_list      
