import json
import csv
import os
import sys
from pprint import pprint
from tqdm import tqdm
import operator

def tf_analysis(src,num_cls):
    
    tf = {}
    with open(src,'r+') as file:
        for line in tqdm(file):
            dic = json.loads(line)
            for annos in dic["annotations"]:
                for anno in annos:
                    if anno["is_chinese"]:
                        try:
                            tf[anno["text"]] += 1
                        except:
                            tf[anno["text"]] = 1
    sorted_tf = sorted(tf.items(), key=operator.itemgetter(1))
    
    if num_cls == "all":
        with open(f"ctw_big.names","w+") as f:
            for i in sorted_tf:
                f.write(i[0]+"\n")

    else:
        with open(f"ctw{str(num_cls)}.names","w+") as f:
            for i in sorted_tf[-1*num_cls:]:
                f.write(i[0]+"\n")


    return f"ctw{str(num_cls)}.names"

    
     

if __name__ == "__main__":
    
    train_src = "train.jsonl"
    test_src = "test.jsonl" 
    val_src = "val.jsonl"

    train_path = "../data/train/"
    test_path = "../data/test/"
    val_path = "../data/val/"

    tf_analysis(train_src,"all")
    tf_analysis(train_src,1000)