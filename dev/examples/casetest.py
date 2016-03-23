"""
Testscript for all cases
"""

noise = np.fromfile('../data/test_datasets/randnumbers/noisearr.txt')
noise = noise.reshape(20,300)

with open("../data/test_datasets/ricker/rickerlist.dat", 'r') as fh:
	rickerlist = np.array(fh.read().split()).astype('str')

noisefoldlist = ["no_noise","10pct_noise", "20pct_noise", "50pct_noise", "60pct_noise", "80pct_noise"]
noiselevellist = np.array([0., 0.1, 0.2, 0.5, 0.6, 0.8]) 

peaks = np.array([[-13.95      ,   6.06      ,  20.07      ],[  8.46648822,   8.42680793,   8.23354933]])
errors = []
for i, noisefolder in enumerate(noisefoldlist):
	print("##################### NOISELVL %i %% #####################\n" % int(noiselevellist[i] * 100.) )
	for filein in rickerlist:
		print("##################### CURRENT FILE %s  #####################\n" % filein )
		PICPATH = "../data/test_datasets/ricker/" + noisefolder + "/"
		PATH = "../data/test_datasets/ricker/" + filein
		srs = read_st(PATH)
		if i != 0:
			data = stream2array(srs) * noiselevellist[i] * noise
			srs = array2stream(data)

		name = 'boxcar_auto_noise_' + str(noiselevellist[i]) +  '.png'
		picpath = PICPATH + name
		st_rec = fk_reconstruct(srs, slopes=[-2,2], deltaslope=0.001, maskshape=['boxcar', None], solver='ilsmr',method='interpolate', mu=2.5e-2, tol=1e-12, peakinput=peaks)
		st_rec.normalize()
		fku.plot_data(stream2array(st_rec), savefig=picpath)


		name = 'boxcar_size1_noise_' + str(noiselevellist[i]) +  '.png'
		picpath = PICPATH + name
		st_rec = fk_reconstruct(srs, slopes=[-2,2], deltaslope=0.001, maskshape=['boxcar', None], solver='ilsmr',method='interpolate', mu=2.5e-2, tol=1e-12, peakinput=peaks)
		st_rec.normalize()
		fku.plot_data(stream2array(st_rec), savefig=picpath)


		taperrange = [0.5, 1, 1.5]
		for ts in taperrange:
			print("##################### %s, NOISE: %f, :CURRENTLY TAPERING WITH %f  #####################\n" % (filein, int(noiselevellist[i] * 100.), ts) )
			try:
				st_rec = fk_reconstruct(srs, slopes=[-2,2], deltaslope=0.001, maskshape=['taper', ts], solver='ilsmr',method='interpolate', mu=2.5e-2, tol=1e-12, peakinput=peaks)
				name = 'taper_' + str(ts) + "_" + str(noiselevellist[i]) +  '.png'
				picpath = PICPATH + name
				st_rec.normalize()
				fku.plot_data(stream2array(st_rec), savefig=picpath)
			except:
				error.append(picpath)
				continue

		bwrange = [1,2,4,8]
		for bw in bwrange:
			print("##################### %s, NOISE: %f, :CURRENTLY BUTTERWORTHING WITH %f  #####################\n" % (filein, int(noiselevellist[i] * 100.), bw) )
			try:
				st_rec = fk_reconstruct(srs, slopes=[-2,2], deltaslope=0.001, maskshape=['butterworth', bw], solver='ilsmr',method='interpolate', mu=2.5e-2, tol=1e-12, peakinput=peaks)
				name = 'butterworth_' + str(bw) + "_" + str(noiselevellist[i]) +  '.png'
				picpath = PICPATH + name
				st_rec.normalize()
				fku.plot_data(stream2array(st_rec), savefig=picpath)
			except:
				error.append(picpath)
				continue
