import cv2
import numpy as np
import streamlit as st
from PIL import Image
from scipy.signal import argrelextrema


def image_difference(vec, image):
    # shift the image vec pixels to the right
    shift = np.float32([[1, 0, vec], [0, 1, 0]])
    shifted = cv2.warpAffine(image, shift, (image.shape[1], image.shape[0]))
    difference = cv2.subtract(image, shifted)
    return difference


def local_extremums(black_pix_array):
    minimums = argrelextrema(black_pix_array, np.less)
    maximums = argrelextrema(black_pix_array, np.greater)
    return minimums[0], maximums[0]


def biggest_extremums_diff(minimums, maximums, black_pix_list):
    value, vec = 0, 0
    for i in range(min(len(minimums), len(maximums))):
        minn, maxx = black_pix_list[minimums[i]], black_pix_list[maximums[i]]
        if (maxx - minn) > value:
            value, vec = maxx - minn, maximums[i]
    return vec


def count_black_pix(image, cropped_img, vec):
    grayImage = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    black_pix = (image.shape[0] * (image.shape[1] - vec)) - cv2.countNonZero(grayImage)
    return black_pix


def solve_stereogram(image):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    black_pix_list = []
    vec = int(image.shape[1] * 0.1)
    while vec < image.shape[1] * 0.4 :
        difference = image_difference(vec, image)
        crop_img = difference[0 : image.shape[0], vec : image.shape[1]]
        black_pix_list.append(count_black_pix(image, crop_img, vec))
        vec += 1
    minimums, maximums = local_extremums(np.array(black_pix_list))
    shift_value = biggest_extremums_diff(minimums, maximums, black_pix_list)
    answer_img = image_difference(int(image.shape[1] * 0.1) + shift_value, image)
    return answer_img


def load_img(file):
    img = Image.open(file)
    return img


st.title('Autostereogram solver')
st.write("""
    Upload a picture to see what is hidden inside :)

    PS

    it's not a perfect algorithm so not every autostereogram will be solved but I'm working on improving it!
""")


uploaded_file = st.file_uploader('Upload Files',type=['png','jpeg', 'jpg'])
if uploaded_file is not None:
    file_details = {'FileName':uploaded_file.name,
                    'FileType':uploaded_file.type,
                    'FileSize':uploaded_file.size}

    image = solve_stereogram(load_img(uploaded_file))
    st.image(image)
    st.image(load_img(uploaded_file))


cv2.waitKey(0)
cv2.destroyAllWindows()

