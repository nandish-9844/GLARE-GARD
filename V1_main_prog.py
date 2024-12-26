import cv2
import numpy as np
import matplotlib.pyplot as plt


#__________________________________________________________________________________________________________________
def main():
     # Load the image
    image_path = input("Enter the path of the image: ")
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("Failed to load image. Check the path.")
        return

    # Display the intensity (grayscale) image
    plt.imshow(image, cmap='gray')
    plt.title("Grayscale Image")
    plt.axis("off")
    plt.show()

    # Get the dimensions of the image
    height, width = image.shape

    # Define slice dimensions
    slice_height = height // 8  # 8 slices vertically
    slice_width = width // 32  # 32 slices horizontally

    # Initialize the 8x32 array for storing mode intensities
    intensity_modes = np.zeros((8, 32), dtype=int)

    # Divide the image into 8x32 slices and calculate mode intensity for each slice
    for i in range(8):
        for j in range(32):
            # Extract the slice
            slice_image = image[i * slice_height:(i + 1) * slice_height, j * slice_width:(j + 1) * slice_width]

            # Calculate the mode of the slice
            unique, counts = np.unique(slice_image, return_counts=True)
            mode_intensity = unique[np.argmax(counts)]

            # Store the mode intensity in the array
            intensity_modes[i, j] = mode_intensity

    # Print the 8x32 array of mode intensities
    print("8x32 Array of Mode Intensities:")
    print(intensity_modes)
    return(intensity_modes)
#_____________________________________________________________________________________________________________________
    
def generate_heatmap(intensity_modes):

    plt.figure(figsize=(8, 4))  # Adjust figure size as needed

    # Create a heatmap with appropriate colormap (e.g., 'hot')
    plt.imshow(intensity_modes, cmap='hot', interpolation='nearest')
    plt.title("Intensity Map")
    plt.colorbar(label="Intensity Mode")
    plt.tight_layout()
    plt.show()
#___________________________________________________________________________________________________________________


import numpy as np
def focus_intensities(intensity_modes):
  focused_intensity_modes = np.where(intensity_modes >= 100, intensity_modes, 0)
  print("focused intensity modes array:\n")
  print(focused_intensity_modes)
  return focused_intensity_modes


#__________________________________________________________________________________________________________________

def otpt(focused_intensity_modes):
    height, width = focused_intensity_modes.shape
    r = str(0) #runbit toggles everytime a frame is read
    rb = str(0)  #resereve bit can be used to cheak for errors


    # 16 bit format:  runbit(1) +position(8) +voltage_value(5) +resreve_bit(1) + sum(1)
    for i in range(height):
        for j in range(width):
            if focused_intensity_modes[i, j] != 0:
                position = (i * width) + j 
                binary_position = r + rb + format(position, '08b')  # 8-bit BCD of position
                inte_val = focused_intensity_modes[i, j] #intensity val
                op_voltage = round(inte_val*0.61176*0.19755) #int val of voltage level bw 0 to 32
                """225->156+1 combo(multi by 0.61176) & 156->32bit(multi by 0.19755)"""
                binary_position += format(op_voltage, '05b') 
                sum_16b  = 0
                for bit in binary_position:
                    sum_16b ^= int(bit)  # XOR with the current bit (converted to integer)
                binary_position += str(sum_16b)
                print(binary_position + " : \t"+ "Run bit:"+binary_position[0]+ "\t reserve bit:" +binary_position[1] +"\t position[BCD]:" +binary_position[2:9] + "\t Voltage level[BCD]:" +binary_position[10:14] + "\t Sum bit[for bit fliping errors]:" +binary_position[15] )
                    

    r = str(not int(r))#update run bit
#__________________________________________________________________________________________________________________
if __name__ == "__main__":
    intensity_modes = main()
    generate_heatmap(intensity_modes)
    focused_intensity_modes = focus_intensities(intensity_modes)
    generate_heatmap(focused_intensity_modes)
    otpt(focused_intensity_modes)