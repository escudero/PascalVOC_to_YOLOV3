# PascalVOC_to_YOLOV3
Used to convert PASCAL VOC 1.1 (XML) labels to YOLOv3 training labels

## Example:
PascalVOC_to_YOLOV3.py --xmlpath &lt;xmlpath&gt; --yolofile &lt;yolofile&gt; --namesfile &lt;namesfile&gt;

PascalVOC_to_YOLOV3.py --xmlpath datasets/iris/xml/ --yolofile datasets/iris/data.txt --namesfile datasets/iris/data.names
