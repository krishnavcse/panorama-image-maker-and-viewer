import os
import cv2
# use r to remove c to crop esc to quit

ref_point = []
cropping = False
f_path=""  # to keep track of the path of image

def path_image(path): # path_image() to pass the path of image which has to be cropped
    image = cv2.imread(path) # reading the image
    clone = image.copy()  # making a clone copy of the image
    cv2.namedWindow("image")  # Sub Window name
    def shape_selection(event, x, y, flags, param): # shape_selection() to keep track of co-ordinates
        global ref_point, cropping

        if event == cv2.EVENT_LBUTTONDOWN:
            ref_point = [(x, y)]
            cropping = True

        elif event == cv2.EVENT_LBUTTONUP:

            ref_point.append((x, y))
            cropping = False
            cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2) # rectangle made for cropping
            cv2.imshow("image", image) # display rectangle upon the clone image
    cv2.setMouseCallback("image", shape_selection)

    while True:
        cv2.imshow("image", image) # display the actual image
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"): # press 'r' to redo for making rectangle
            image = clone.copy()
                                   # After cropping pressing 'r' or 'c' to close the cropped and cloned image window

        elif key == ord("c"): # press 'c' to crop the image after making rectangle
            break

    if len(ref_point) == 2:
        crop_img = clone[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]
        cv2.imshow("crop_img", crop_img)
        cwd = os.getcwd()
        data = cwd.split("\\")
        data.pop()
        source_d = '\\'.join(data)
        source_d = source_d + '\cropped'
        source_f = source_d + '\crop.jpg'  # to store the cropped image temporary in cropped folder
        cv2.imwrite(source_f, crop_img)
        cv2.waitKey(0)

    cv2.destroyAllWindows() # to enable to destroy the windows after its use
