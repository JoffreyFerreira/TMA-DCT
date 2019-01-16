import os        
import numpy as np
from skimage.color import rgb2gray
from skimage import data, measure,io
import skimage as sk
import matplotlib.pyplot as plt
from BluM import BlocM, BluM
import PIL as pil
import sys

n=16

#prend 2 bloc de taille 16*16 et retourne la distance euclidienne
def compareBloc(bloc, bloc1, size):
	sum = 0
	for i in range(size[0]):
		for j in range(size[1]):
			sum += np.sqrt((bloc[i,j]-bloc1[i,j])*(bloc[i,j]-bloc1[i,j]))
	return sum
			
# prend 2 images et renvoie les bloc + vecteur de deplacement de ces derniers
def prediction(img0, img1):
	tabDist = []
	img_size = img0.shape
	block = np.zeros(img_size)
	blocklist = np.zeros(img_size)
	for i in range(0,img_size[0],16):
		for j in range(0,img_size[1],16):
			block_size = img1[i:i+16,j:j+16].shape
			block[0:block_size[0],0:block_size[1]] = img1[i:i+16,j:j+16]
			blocklist[0:block_size[0],0:block_size[1]] = img0[i:i+16,j:j+16]
			dist = compareBloc(blocklist, block, block_size)
			 
			if dist>5 :
				vec = [0,0]
				for x in range(-15,15,1):
					for y in range(-15,15,1):
						block_size = img0[i+x:i+x+16,j+y:j+y+16].shape
						blocklist[0:block_size[0], 0:block_size[1]] = img0[i+x:i+x+16,j+y:j+y+16]
						tmpdist = compareBloc(blocklist, block,block_size)
						print(tmpdist)
						if tmpdist<dist :
							dist = tmpdist
							vec = [x, y] 
				tabDist.append([[i,j],vec])
	print(tabDist)
	return tabDist


# prend une image et une liste de couple bloc-vecteur et calcule la nouvelle image
def calculImage(img, tabDist, nameIm) :
	newimag = img
	for indice in range(tabDist):
		i = tabDist[indice][0][0]
		j = tabDist[indice][0][1]
		x = tabDist[indice][1][0]
		y = tabDist[indice][1][1]
		block = img[i:i+16, j:j+16]
		newimag[i+x:i+x+16, j+y:j+y+16] = block

	monIm=pil.Image.fromarray(np.ubyte(np.round(255.0*newimag,0)))
	monIm.save(nameIm)


# main
img0=io.imread('taxi_00.bmp')
img_gray0 = rgb2gray(img0)
img_gray0=sk.img_as_float(img_gray0)
img1=io.imread('taxi_01.bmp')
img_gray1 = rgb2gray(img1)
img_gray1 = sk.img_as_float(img_gray1)
tabDist = prediction(img_gray0,img_gray1)