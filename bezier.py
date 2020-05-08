from PIL import Image
from PIL import ImageDraw
import numpy as np 
import cv2
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import sys

def parse_output(): 
    i = 0
    whole_line = ""
    with open("output") as f:
        lines = f.readlines()
        for line in lines:
            if "<>" in line:
                if (i % 2) == 0: 
                    whole_line = ""
                whole_line += line.strip()[2:]
                if (i % 2) == 0: 
                    whole_line += "|"
                if (i % 2) == 1:
                    print(whole_line) 
                    
                i += 1
            # print(line, end="")

def make_bezier(xys):
    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = pascal_row(n-1)
    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1-t)**i for i in range(n)])
            coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(
                tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result
    return bezier

def pascal_row(n, memo={}):
    # This returns the nth row of Pascal's Triangle
    if n in memo:
        return memo[n]
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n//2+1):
        # print(numerator,denominator,x)
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n&1 == 0:
        # n is even
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result))
    memo[n] = result
    return result

class Data(): 
    def __init__(self): 
        self.i = 0

    def right(self, maxVal):
        self.i = min(maxVal, self.i + 1)

    def left(self):
        self.i = max(0, self.i - 1)

    def get(self): 
        return self.i

def main(): 
    test = Data()
    fig, ax = plt.subplots()
    allCurves = []
    min_x = float('inf')
    min_y = float('inf')
    max_x = -float('inf') 
    max_y = -float('inf')
    
    def press(event):
        sys.stdout.flush()
        if event.key == 'right':
            test.right(len(allCurves) - 1)
        else: 
            test.left()
        
        # Plot
        ax.clear()
        for curve in allCurves[test.get()]: 
            codes = [Path.MOVETO] + [Path.LINETO for _ in range(len(curve) - 1)]
            path = Path(curve, codes)
            patch = patches.PathPatch(path, lw=2, fill=False)
            ax.add_patch(patch)

            ax.set_xlim(min_x * 0.9, max_x * 1.1)
            ax.set_ylim(min_y * 0.9, max_y * 1.1)
            ax.set_title(test.get())
        fig.canvas.draw()

    fig.canvas.mpl_connect('key_press_event', press)

    with open('data') as f: 
        lines = f.readlines()
        for line in lines: 
            line = line.strip()
            curves = line.split("|")
            
            # Create the control points
            for curve in curves: 
                l = eval(curve)
                controlPointsArray = [eval(curve) for curve in curves]

            # Setup
            ts = [t/100.0 for t in range(101)]

            # Create the bezier curves and 
            # figure out the bounds automatically:
            curves = []
            for controlPoints in controlPointsArray:
                bezier = make_bezier(controlPoints)
                curves.append(bezier(ts)) 
                for controlPoint in controlPoints:
                    min_x = min(controlPoint[0], min_x)
                    min_y = min(controlPoint[1], min_y)
                    max_x = max(controlPoint[0], max_x)
                    max_y = max(controlPoint[1], max_y)
            
            allCurves.append(curves)

    plt.show()

if __name__ == '__main__':
    if sys.argv[1] == "0":
        main()
    else: 
        parse_output()