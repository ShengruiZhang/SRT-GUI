import AFE

Arduino = AFE.Init(9600)

AFE.Activate(Arduino)

WindSpeedRaw = AFE.GetWindRaw(Arduino)
print(WindSpeedRaw, end='')

AFE.CloseSerial(Arduino)
