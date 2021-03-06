import matplotlib.pyplot as plt
import numpy as np
import math as meth
from scipy.ndimage.filters import gaussian_filter

data = np.load('LUCIFER_log_2019_9_15_9_30.npy')#10,8,42,#23,8,35
# data1 = np.load('LUCIFER_log_gps_2019_2_28_21_54.npy')
# plt.axis("equal")

coords = data[:,0:4]
filtered = coords[:,0:2]
raw = coords[:,2:]	

lon = filtered[:,0]
lat = filtered[:,1]
gps_lon = raw[:,0]
gps_lat = raw[:,1]

speed = data[:,4]
heading = data[:,5]
optical = data[:,8]
op_shutter_speed = data[:,9]
op_SQ = data[:,10]
op_max_pix = data[:,11]
Hdop = data[:,12]
exec_time = data[:,13]
# print(exec_time)
t = np.arange(0,len(speed)/10,0.1)
# speed = gaussian_filter(speed,sigma=2)
error = np.fabs(speed-optical)
# ratio = np.mean(speed[400:600]/optical[400:600])
# print(ratio)
# print(np.var(error[:250]))
# lat = data[int(len(data)/2):]
# lat = lat[:-40]
# lon = data[:int(len(data)/2)]
# lon = lon[:-40]
# speed = np.sqrt(np.gradient(lat)**2 + np.gradient(lon)**2)*111392*10

# gps_lat = data1[int(len(data)/2):]
# gps_lat -= (gps_lat[0]-lat[0])
# gps_lat = gps_lat[:-40]
# gps_lon = data1[:int(len(data)/2)]
# gps_lon -= (gps_lon[0]-lon[0])
# gps_lon = gps_lon[:-40]
# print(gps_lat[0],gps_lon[0]) 

# theta = meth.atan2((lat[10] - lat[0]),(lon[10] - lon[0])) - meth.atan2((gps_lat[10]-gps_lat[0]),(gps_lon[10] - gps_lon[0]))
# print(theta)
# angle = 57.3*meth.atan((gps_lat[30] - lat[30])/(gps_lon[30] - lon[30]))
# print(angle)

def LPF(c):
	x = np.zeros(2)
	x[0] = x[1] = c[0]
	y = np.zeros(2)
	GAIN = 1.370620474e+01
	coeff = 0.8540806855
	for i in range(len(c)):
		x[0] = x[1]
		# if c[i] < y[1]:
		# 	GAIN = 4.077683537
		# 	coeff = 0.5095254495
		# else:
		# GAIN = 5.165299770
		# coeff = 0.6128007881
		x[1] = c[i]/GAIN
		y[0] = y[1]
		y[1] = (x[0] + x[1]) + (coeff*y[0])
		c[i] = y[1]

	return c

plt.title('')
print(len(t))
def fit(x,c):
	return c[0]*x**3 + c[1]*x**2 + c[2]*x + c[3]

# # position plot : 
# plt.plot((lon[:] - lon[0]),(lat[:]-lat[0]), label='filtered')
# plt.xlabel('X (m)')
# plt.ylabel('Y (m)')
# plt.plot(111392*(gps_lon - gps_lon[0] ),111392*(gps_lat - gps_lat[0]), label='raw gps')
# plt.axis('equal')


dist_cord = 0
dist_vel = 0
dist_gps = 0
lon *= 111392.84
lat *= 111392.84
gps_lon *= 111392.84
gps_lat *= 111392.84
for i in range(1,len(lon)):
	dist_cord += meth.sqrt((lon[i]-lon[i-1])**2 + (lat[i]-lat[i-1])**2)
	dist_gps += meth.sqrt((gps_lon[i] - gps_lon[i-1])**2 + ( gps_lat[i] - gps_lat[i-1])**2 )
	dist_vel += 0.1*(speed[i]+speed[i-1])/2

# print(dist_vel,dist_cord,dist_gps)


#modelling speed : 
# exec_time = np.array([1550,1600,1640,1690,1750,1810])
# exec_time -= 1535
# exec_time = exec_time/(1810-1535)
# # # print(exec_time)
# speed = np.array([1,4,6.1,8.3,10.4,12])
# plt.scatter(exec_time,speed)
# c = np.polyfit(exec_time,speed,3)
# t_ = np.arange(0,1.0,0.01)
# model = fit(t_,c)
# print(c) #print coeffs
# plt.xlabel('input % (1=100%)')
# plt.ylabel('speed in m/s')
# inp = (1560-1535)/(1810-1535)
# print(inp)
# print(fit(inp,c))
# plt.plot(t_,model,label='fit')

# exec_time = np.array([1550,1600,1640,1690,1750,1810])
# exec_time -= 1535
# exec_time = exec_time/(1810-1535)
# # # print(exec_time)
# speed = np.array([1,4,6.1,8.3,10.4,12])
# plt.scatter(speed,exec_time)
# c = np.polyfit(speed,exec_time,3)
# speed_target = np.arange(0,12.0,0.01)
# model = fit(speed_target,c)
# print(c) #print coeffs
# plt.xlabel('target_speed')
# plt.ylabel('throttle')
# plt.plot(speed_target,model,label='fit')



def tune(speed, optical):
	feedback = 1
	process_noise = 0.1
	decay_rate = 0.1
	est_error = 0.05
	dt = 0.1
	for i in range(len(speed)-1):
		if(speed[i]<3):
			gain = process_noise/(process_noise+est_error)
			feedback += gain*(optical[i]-speed[i])
			process_noise *= (1-gain)
		optical[i+1] /= feedback
	return optical


# for testing which low pass filter works for us : LUCIFER_log_2019_3_22_12_8.npy
# speed = speed[:-40]
# optical = optical[:-40]
# t = t[:-40]
# print(len(t))
# speed = gaussian_filter(speed,sigma=2)
# optical = gaussian_filter(optical,sigma=1)
# # plt.title('without correction')
plt.plot(t,speed,label='filtered speed')
# plt.scatter(exec_time,speed)
# plt.plot(t[:-1],optical[1:],label='gps')
# gps = optical[1:]
# sped = speed[:-1]
# gain = op_SQ[1:]*10/(op_SQ[1:]*10+1)
# filt = gps*(1-gain) + gain*sped
# plt.plot(t[:-1],filt,label='fused')
# plt.plot(t[:-1],op_SQ[1:]*10,label='Sdop')
plt.plot(t,optical,label='raw')
# plt.ylim((0,10))
plt.plot(t,op_SQ,label='dS_x')
# plt.plot(t,Hdop,label='Hdop')
# plt.plot(t,gaussian_filter(op_SQ/20,sigma=1),label='SQ')

# plt.ylabel('speed in m/s')
# plt.xlabel('time in seconds')
# plt.plot(t,LPF(optical*(6/7)),label='LOW passed')

# for optical flow testing :
# op_SQ = gaussian_filter(op_SQ,sigma=10) 

# for finding variance : 
# variance = np.zeros(50)
# for i in range(50):
# 	target_value = i+60
# 	error_list = []
# 	for j in range(len(op_SQ)):
# 		if(op_SQ[j]==target_value):
# 			error_list.append(error[j])
# 	error_list = np.array(error_list)
# 	if(len(error_list)!=0):
# 		variance[i] = np.var(error_list)

# dummy_SQ = np.arange(60,110,1)

# plt.scatter(op_SQ,error,label='raw data')
# plt.scatter(dummy_SQ,variance,label='measured variance')
# c = np.polyfit(dummy_SQ[30:]/169,variance[30:],3)
# t_ = np.arange(60,110,1)
# anal_var = fit(t_/169,c)
# plt.scatter(t_,anal_var,label='analytical variance')
# print(c)
# # plt.plot(x,func,label='best fit variance')
# # # plt.ylim((50,100))
# plt.ylabel('error (m/s)')
# plt.xlabel('surface Quality')
# plt.plot(np.arange(0,len(lat)/10,0.1),speed,label='speed')


plt.legend()

plt.show()

# def sinu(x):
#     B = 4/meth.pi
#     C = -B/meth.pi

#     y = B*x + C*x*np.fabs(x);

#     P = 0.225;
#     y = P*(y*abs(y) - y) + y #   // Q * y + P * y * abs(y)
#     return y;

# def asinu(x):
# 	return (0.87266462599716477 + 0.69813170079773212*x*x )*x

# a = np.arange(0,1.0,0.001)

# last_MSE = 100
# for i in range(0,15):
# 	x = 0.1*i
# 	C1 = meth.pi/2 - x
# 	C2 = x
# 	y = a*(C1+ C2*a*a*a*a*a*a)
# 	MSE = np.linalg.norm(y-np.arcsin(a))
# 	if(MSE < last_MSE):
# 		save = np.array([C1,C2])
# 		last_MSE = MSE

# z = a*(1+0.57*a*a*a*a*a*a)
# MSE1 = np.linalg.norm(z-np.arcsin(a))

# # print(save,MSE/15)
# # print(y[0],y[-1])
# # y = x*x*x*x/(0.01+x*x*x*x)
# y = a*(save[0] +save[1]*a*a*a*a*a*a) 
# MSE2 = np.linalg.norm(y-np.arcsin(a))
# print(MSE1,MSE2)
# # plt.title('')
# # # plt.ylim((-1,1))
# plt.plot(a, y, label='internet')
# plt.plot(a, z,label='mine')
# plt.plot(a, np.arcsin(a), label ='true')
# plt.legend()
# plt.show()

