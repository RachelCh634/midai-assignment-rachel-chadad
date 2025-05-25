from ultralytics import YOLO
import cv2
import json

model = YOLO("yolov5su.pt")
image_path = "image.png"

image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError(f"Error, The image is not exist in {image_path}")

results = model(image)

boxes = results[0].boxes
class_ids = boxes.cls.tolist()
scores = boxes.conf.tolist()
coords = boxes.xyxy.tolist()

class_names = model.names

output = []
for cls_id, score, coord in zip(class_ids, scores, coords):
    x1, y1, x2, y2 = map(int, coord)
    label = f"{class_names[int(cls_id)]} ({score:.2f})"

    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    output.append({
        "class": class_names[int(cls_id)],
        "confidence": round(float(score), 3),
        "box": [round(float(x), 2) for x in coord]
    })

with open("results/detections.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

cv2.imwrite("results/output_with_boxes.jpg", image)

print("Output saved as: output_with_boxes.jpg")


