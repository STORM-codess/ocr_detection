# ocr/extract.py
import easyocr
import cv2

# English-only OCR
reader = easyocr.Reader(['en'], gpu=False)

def extract_clean_lines(image_path):
    """
    Extract clean, grouped, line-by-line text from the image.
    Everything is returned in lowercase for consistent parsing.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not readable: " + image_path)

    results = reader.readtext(img, detail=1)

    line_map = {}

    for bbox, text, conf in results:
        # convert text to lowercase
        text = text.lower()

        y_top = int(bbox[0][1])
        line_key = (y_top // 10) * 10  # grouping lines

        if line_key not in line_map:
            line_map[line_key] = []

        line_map[line_key].append((bbox[0][0], text))

    # sort lines top-to-bottom
    sorted_lines = sorted(line_map.items(), key=lambda x: x[0])

    final_lines = []

    for y, words in sorted_lines:
        # sort words left → right
        words = sorted(words, key=lambda x: x[0])

        # join words as lowercase line
        line = " ".join([w[1] for w in words])

        final_lines.append(line)

    return final_lines
