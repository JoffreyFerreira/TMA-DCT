# TMA-DCT

Localisation/répartition des données : Au milieu horizontal de l'image

Cas n=8,4,16
Observations :
* Cas n=4 donne un taux de compression de 16 ce qui donne une compression quasiment indetectible pour un homme et le temps de calcul est très rapide
* Cas n=8 compression de 64 et d'assez bonne qualité avec un temps de calcul assez court
* Cas n=16 Taux de cmopression de 256 ce qui est très élevée, donne une compression de pas très bonne qualité et le temps de calcul est plus long
Le choix de n=8 semble un bon compromis entre taux de compression élevée et qualité suffisante

PSNR :
A partir d'un facteur qualité de 75 le PSNR augmente brusquement et rapidement jusqu'à 60 dB, pour une image de qualité suffisante il faudrait un psnr supérieur à 30dB, cette valeur est dépassé vers qualité=20. Ce qui correspond à peu près à nos observations précédente sur la valeur de n

SSIM :
Le SSIM augmente rapidement jusqu'à qualité=60, ensuite il monte lentement jusqu'à un palier de 1 vers qualité=100
SSIM valide également le choix de n=8
 
