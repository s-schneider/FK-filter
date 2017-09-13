from bowpy.util.data_request import data_request
from obspy.clients.fdsn import Client

client = Client('IRIS')

cat = client.get_events(minmagnitude=8)

data_request('IRIS', cat=cat, net='*', channels='LH*', savefile=True,
             normal_mode_data=True, file_format='ah')
