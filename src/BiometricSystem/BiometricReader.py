from brainflow.board_shim import BoardShim, BoardIds, BrainFlowInputParams, BrainFlowPresets
from scipy.signal import butter, filtfilt, find_peaks
from numpy import mean
from datetime import datetime
import time
from uuid import uuid4

class BiometricReader:
    def __init__(self):
        self.emotibit = None
        self.heartRate= None
        self.eda = None
        self.temperature= None
        self.startTime= None
        self.endTime= None
        self.setup()

    def setup(self):
        params= BrainFlowInputParams()
        #Can be run without specific address but it will take longer
        params.ip_address = '192.168.137.255'
        self.emotibit = BoardShim(BoardIds.EMOTIBIT_BOARD, params)
        BoardShim.disable_board_logger()
    
    def read(self):
        self.emotibit.prepare_session()
        start = datetime.now()
        self.startTime = start.strftime("%H:%M:%S")
        self.emotibit.start_stream()
        time.sleep(10)
        auxData= self.emotibit.get_board_data(preset=BrainFlowPresets.AUXILIARY_PRESET.value)
        ancData= self.emotibit.get_board_data(preset=BrainFlowPresets.ANCILLARY_PRESET.value)
        self.emotibit.stop_stream()
        end = datetime.now()
        self.startTime = end.strftime("%H:%M:%S")
        self.emotibit.release_session()
        self.processData(auxData, ancData)

    def processData(self, ppgData, edaData):

        filteredPpg= self.filterPPG(ppgData[1])
        heartRate= self.calculateHeartRate(filteredPpg)
        filteredEda= self.filterEDA(edaData[1])
        averageEda= mean(filteredEda)
        averageTemp = mean(edaData[2])

        self.heartRate = heartRate
        self.eda = averageEda
        self.temperature = averageTemp

    def filterPPG(self, data):
        order= 4
        sampleRate = 25
        nyquist_freq= 0.5 * sampleRate #multiplying the sample rate in half to find the nyquist freq
        low= 0.5 / nyquist_freq #getting low end of nyquist freq, 0.5 hertz equates to 30 beats per minute
        high= 3.0 / nyquist_freq #getting high end of nyquist freq, 3.0 hertz equates to 180 beats per minute
        b, a = butter(order, [low, high], btype= 'band')
        return filtfilt(b, a, data)

    def filterEDA(self, data):
        order= 4
        sampleRate= 15
        nyquist_freq = 0.5 * sampleRate #same as above
        limit =  1.0 / nyquist_freq
        b, a = butter(order, limit, btype= 'low')
        return filtfilt(b, a, data)

    def calculateHeartRate(self, data):
        sampleRate= 25
        maxBpm= 180
        distanceBetweenPeaks= sampleRate * 60 / maxBpm
        peaks, _ = find_peaks(data, distance= distanceBetweenPeaks)
        numPeaks= len(peaks) #getting the number of peaks
        signalDuration= len(data) / 25
        bpm = numPeaks * 60/ signalDuration
        return bpm

    def getHeartRate(self):
        return self.heartRate

    def getEDA(self):
        return self.eda
    
    def getTemperature(self):
        return self.temperature
    
    def getStartTime(self):
        return self.startTime
    
    def getEndTime(self):
        return self.endTime