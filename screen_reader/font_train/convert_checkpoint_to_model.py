import sys
import os
import pathlib

TESSERACT_LSTMF_WIN_EXE = r"C:\Program Files\Tesseract-OCR\lstmtraining.exe"
BASE_MODEL = os.path.join(pathlib.Path(__file__).parent.resolve(),"base_model/eng.traineddata")
CMD_TEMPLATE = '"{LSTMF_EXE}"  --stop_training  --continue_from {checkpoint} --model_output {out_path} ' \
               '--traineddata {base_model}'
def main(checkpoint_file_path):
    out_path = checkpoint_file_path.split(".")[0]
    cmd = CMD_TEMPLATE.format(LSTMF_EXE=TESSERACT_LSTMF_WIN_EXE,
                              checkpoint=checkpoint_file_path,
                              out_path=out_path,
                              base_model=BASE_MODEL)
    os.system(cmd)

if __name__ == "__main__":
    checkpoint_file = sys.argv[1]
    main(checkpoint_file)