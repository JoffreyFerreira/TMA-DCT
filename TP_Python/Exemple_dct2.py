import os        
import numpy as np
from skimage.color import rgb2gray
from skimage import data, measure,io
import skimage as sk
import matplotlib.pyplot as plt
from dct2 import dct2, idct2
import PIL as pil
import sys



img=io.imread('Im3Comp100.jpg')
img_gray = rgb2gray(img)
img_gray=sk.img_as_float(img_gray)
plt.figure(1)
plt.imshow(img_gray,cmap='gray')
N = int(sys.argv[1])
M = int(sys.argv[1])
window_size = (N,M)
img_size=img_gray.shape


dctblock=np.zeros(img_size)
block = np.zeros(window_size)
print(block.shape)
print(block.dtype)


# table de quantification
quant = np.zeros(window_size)
compr = N*M
for i in range(N):
	for j in range(M):
		quant[i,j] = 1+(1+j+i)*compr

#dct + quant
for i in range(0,img_size[0], N):
	for j in range(0,img_size[1], M):
		# print("i : "+str(i)+" j : "+str(j))
		block_size = img_gray[i:i+N,j:j+M].shape
		block[0:block_size[0],0:block_size[1]] = img_gray[i:i+N,j:j+M]
		block = dct2(block)
		dctblock[i:i+N,j:j+M] = block[0:block_size[0],0:block_size[1]]/quant[0:block_size[0],0:block_size[1]]

#image compr
plt.figure(3)
plt.imshow(np.log(1.0+dctblock),cmap='gray')

#idct + iquant
newim=np.zeros(img_size)
for i in range(0,img_size[0], N):
	for j in range(0,img_size[1], M):
		# print("i : "+str(i)+" j : "+str(j))
		block_size = dctblock[i:i+N,j:j+M].shape
		block[0:block_size[0],0:block_size[1]] = dctblock[i:i+N,j:j+M]*quant[0:block_size[0],0:block_size[1]]
		block = idct2(block)
		newim[i:i+N,j:j+M] = block[0:block_size[0],0:block_size[1]]


#psnr et ssim
psnr=measure.compare_psnr(img_gray,newim,1.0)
ssim=measure.compare_ssim(img_gray,newim)
print("psnr : "+str(psnr)+" ssim : "+str(ssim))

plt.figure(4)
newim=np.ubyte(np.round(255.0*newim,0))
plt.imshow(newim,cmap='gray')

fich=open('madct.dat','wb')
fich.write(np.reshape(newim,-1)) 
fich.close()

psnr_tab = np.zeros(30)
ssim_tab = np.zeros(30)
abs_tab = np.zeros(30)
compt=0

for qual in range(10,160,5):

	monIm=pil.Image.fromarray(np.ubyte(np.round(255.0*img_gray,0)))
	monIm.save('essai.jpeg',quality=qual)

	img_compr = io.imread("essai.jpeg")
	img_compr = rgb2gray(img_compr)
	img_compr=sk.img_as_float(img_compr)
	psnr_tab[compt]=measure.compare_psnr(img_gray,img_compr,1.0)
	ssim_tab[compt]=measure.compare_ssim(img_gray,img_compr)
	abs_tab[compt] = qual
	compt+=1

plt.figure(5)
plt.plot(abs_tab, psnr_tab)
plt.figure(6)
plt.plot(abs_tab, ssim_tab)
print( "taille= ",os.path.getsize("essai.jpeg"), "en octet")
print("compression =", 1.0*img_size[0]*img_size[1]/os.path.getsize("essai.jpeg"))
plt.show()