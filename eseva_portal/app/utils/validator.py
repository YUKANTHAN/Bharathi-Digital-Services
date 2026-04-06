import cv2
import numpy as np
import os

def check_blur(image_path):
    """
    Check if an image is blurry using the Variance of Laplacian method.
    Returns the variance score.
    Higher value -> sharper image (not blurry).
    Lower value -> blurrier image.
    """
    # Load image from path
    image = cv2.imread(image_path)
    
    if image is None:
        # File might not be an image or path is invalid. Return 0 for failure.
        return 0.0
        
    # Convert image to grayscale for Laplacian calculation
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate Variance of Laplacian
    #cv2.Laplacian computes the second-order derivatives (edges)
    # The variance is proportional to the number of edges.
    # Sharp images have many edges (high variance), blurry images have few (low variance).
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    return variance
