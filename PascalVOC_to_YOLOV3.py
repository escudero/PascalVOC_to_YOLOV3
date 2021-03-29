import xml.etree.ElementTree as ET
import os
from glob import glob
import sys, getopt


names = []

def ParseXML(pascalvoc_path, filenames, file):
    global names
    for xml_file in glob(os.path.join(pascalvoc_path, 'Annotations', '*.xml')):
        if xml_file.split(os.path.sep)[-1] not in filenames:
            continue
        tree = ET.parse(open(xml_file))
        root = tree.getroot()
        image_name = root.find('filename').text
        img_path = os.path.join(pascalvoc_path, image_name)
        for i, obj in enumerate(root.iter('object')):
            klass_name = obj.find('name').text
            if klass_name not in names:
                names.append(klass_name)
            klass_id = names.index(klass_name)
            xmlbox = obj.find('bndbox')

            xmin = int(float(xmlbox.find('xmin').text))
            ymin = int(float(xmlbox.find('ymin').text))
            xmax = int(float(xmlbox.find('xmax').text))
            ymax = int(float(xmlbox.find('ymax').text))

            img_path = f"{img_path} {xmin},{ymin},{xmax},{ymax},{klass_id}"
        print(img_path)
        file.write(img_path+'\n')

def run_PascalVOC_to_YOLOV3(pascalvoc_path, sets_file, yolo_file, names_file):
    with open(sets_file) as f:
        filenames = [f'{filesname.strip()}.xml' for filesname in list(f)]

    with open(yolo_file, "w") as file:
        ParseXML(pascalvoc_path, filenames, file)

    print("Names:", names)
    with open(names_file, "w") as file:
        for name in names:
            file.write(f'{name}\n')

if __name__ == '__main__':
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, 'h', ['pascalvocpath=', 'setsfile=', 'yolofile=', 'namesfile=', 'prenames='])
    except getopt.GetoptError:
        print('PascalVOC_to_YOLOV3.py --pascalvocpath <pascalvocpath> --setsfile <setsfile> --yolofile <yolofile> --namesfile <namesfile> --prenames <prenames>')
        sys.exit(2)
    pascalvoc_path, sets_file, yolo_file, names_file, pre_names = [None, None, None, None, None]
    for opt, arg in opts:
        if opt == '-h':
            print('PascalVOC_to_YOLOV3.py --pascalvocpath <pascalvocpath> --setsfile <setsfile> --yolofile <yolofile> --namesfile <namesfile> --prenames <prenames>')
            sys.exit()
        elif opt in ("--pascalvocpath"):
            pascalvoc_path = arg
        elif opt in ("--setsfile"):
            sets_file = arg
        elif opt in ("--yolofile"):
            yolo_file = arg
        elif opt in ("--namesfile"):
            names_file = arg
        elif opt in ("--prenames"):
            pre_names = arg
    if None in [pascalvoc_path, sets_file, yolo_file, names_file]:
        print('PascalVOC_to_YOLOV3.py --pascalvocpath <pascalvocpath> --setsfile <setsfile> --yolofile <yolofile> --namesfile <namesfile> --prenames <prenames>')
        sys.exit()
    if pre_names is not None:
        names = pre_names.split(',')
    else:
        names = []

    run_PascalVOC_to_YOLOV3(pascalvoc_path, sets_file, yolo_file, names_file)
