import cv2
import numpy as np
import streamlit as st

def image_difference(vec, image):
    # shift the image 25 pixels to the right
    shift = np.float32([[1, 0, vec], [0, 1, 0]])
    shifted = cv2.warpAffine(image, shift, (image.shape[1], image.shape[0]))
    difference = cv2.subtract(image, shifted)
    return difference


def solve_stereogram(image):
    image = cv2.imread(image)
    black_pix = 1000000000000
    answer_img = None
    vec = 1
    while vec < image.shape[1]:
        difference = image_difference(vec, image)
        grayImage = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        count_black_pix = cv2.countNonZero(grayImage)
        if count_black_pix < black_pix:
            black_pix = count_black_pix
            answer_img = difference
        else: pass
        vec += 1
    return answer_img


st.title('Autostereogram solver')
st.write("""
    Upload a picture to see what is hidden inside :)
""")

uploaded_file = st.file_uploader('Upload Files',type=['png','jpeg'])
if uploaded_file is not None:
    file_details = {'FileName':uploaded_file.name,
                    'FileType':uploaded_file.type,
                    'FileSize':uploaded_file.size}

    image = solve_stereogram(uploaded_file.name)
    st.image(image, width=None)
    st.image(uploaded_file.name)


cv2.waitKey(0)
cv2.destroyAllWindows()
