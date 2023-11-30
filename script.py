import cv2


def apply_mosaic(image, x, y, width, height, mosaic_size):
    """
    Apply a mosaic effect to a specific area of the image.
    """
    roi = image[y:y + height, x:x + width]  # Region of interest
    roi = cv2.resize(roi, (mosaic_size, mosaic_size), interpolation=cv2.INTER_LINEAR)
    roi = cv2.resize(roi, (width, height), interpolation=cv2.INTER_NEAREST)
    image[y:y + height, x:x + width] = roi
    return image

def apply_mosaic_to_face(src, dst):
    image_path = src

    face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    image = cv2.imread(image_path)
    face_cascade = cv2.CascadeClassifier(face_cascade_path)

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(1, 1))

    # Apply mosaic to each face
    mosaic_size = 15  # Size of the mosaic pixels
    for (x, y, w, h) in faces:
        image = apply_mosaic(image, x, y, w, h, mosaic_size)

    # Save or display the result
    cv2.imwrite(dst, image)

def apply_mosaic_to_pedestrain(src, dst):
    image_path = src

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    image = cv2.imread(image_path)

    # Detect faces in the image
    (regions, _) = hog.detectMultiScale(image,
                                        winStride=(4, 4),
                                        padding=(4, 4),
                                        scale=1.05)
    mosaic_size = 30
    for (x, y, w, h) in regions:
        image = apply_mosaic(image, x, y, w, h, mosaic_size)

    cv2.imwrite(dst, image)