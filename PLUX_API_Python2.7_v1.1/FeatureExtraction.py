import statistics
import math

class FeatureExtract:
    
    def wavelength(data):
        total = 0
        for i, value in enumerate(data):
            if i == len(data) - 1:
                break
            if data[i+1] > value:
                total += data[i+1] - value
            else:
                total += value - data[i+1]
        wl = total / len(data)
        
        return wl
    
    def meanAbsoluteDeviation(data):
        avg = sum(data) / len(data)
        total = 0
        for value in data:
            total += abs(value - avg)
        mad = total / len(data)
        
        return mad
            
    
    def maxValue(data):
        return max(data)
    
    def minValue(data):
        return min(data)
    
    def medianValue(data):
        return statistics.median(data)
    
    def getAllData(self, data):
        return [self.wavelength(data), self.meanAbsoluteDeviation(data), self.maxValue(data), self.minValue(data)]
    
    def standartDeviation(data):
        avg = sum(data) / len(data)
        total = 0
        for value in data:
            total += (abs(value - avg)) ** 2
        sd = math.sqrt(total / len(data))
        
        return sd