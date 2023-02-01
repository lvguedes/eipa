import sys
import math
import cv2 as cv
from matplotlib import pyplot as plt
import pdb

def calc_plot_pos(n_imgs: int):
    print(f'n_imgs is {n_imgs}')
    divisors_unique = {math.gcd(i, n_imgs) for i in range(1, n_imgs+1)}
    divisors = sorted(list(divisors_unique))
    avg_div = divisors[math.floor(len(divisors)/2)]

    return [avg_div, avg_div]
    

def show_imgs(*args):
    grid = calc_plot_pos(len(args))
    for i in range(0, len(args)):
        pos = grid[:2]
        pos.append(i + 1)
        print(f"Processing image {args[i]}")
        print(f"Image index in grid: {pos}")
        img = cv.imread(args[i])
        (b, g, r) = cv.split(img)
        img = cv.merge((r, g, b))
        #pdb.set_trace()
        plt.subplot(*pos)
        plt.imshow(img)
        plt.title(args[i])
    plt.show()

def main():
    show_imgs(*(sys.argv[1:]))
    
if __name__ == "__main__":
    main()
