import json
import os
import argparse
import sys

parser = argparse.ArgumentParser(description='Build OpenLambda working space.')
parser.add_argument('--workspace', type=str, default = "/root/ol_workspace", help='workspace of OpenLambda')
parser.add_argument('--worker_config', type=str, default = "./worker_config", help='worker config')
args = parser.parse_args()

def read_config(args):
    f = open(args.worker_config, "r")
    lines = f.readlines()
    f.close()
    configs = []
    for line in lines:
        line = line.strip().split(" ")
        configs.append({"worker":line[0], "port":line[1], "priority":line[2], "func_name":line[3]})
    return configs

if __name__ == "__main__":
    with open("example_config.json", "r") as f:
        template = json.load(f)
    configs = read_config(args)
    #example["worker_dir"] = os.path.join(args.workspace, configs["worker"], "worker")
    #print(example)
    print("Buidling workspace at {}".format(args.workspace))
    if not os.path.exists(args.workspace):
        os.makedirs(args.workspace)
        os.system("chmod +x init_functions.sh && cp init_functions.sh {}".format(args.workspace))
        os.system("chmod +x delete_function.sh && cp delete_function.sh {}".format(args.workspace))
        os.system("cp ./ol {}".format(args.workspace))
    
    for c in configs:
        if not os.path.exists(os.path.join(args.workspace, c["worker"])):
            os.system("./ol new --path={}".format(os.path.join(args.workspace, c["worker"])))
            template["worker_dir"] = os.path.join(args.workspace, c["worker"], "worker")
            template["registry"] = os.path.join(args.workspace, c["worker"], "registry")
            template["Pkgs_dir"] = os.path.join(args.workspace, c["worker"], "packages")
            template["SOCK_base_path"] = os.path.join(args.workspace, c["worker"], "lambda")
            template["worker_port"] = c["port"]
            template["seal_priority"] = c["priority"]
            template["function_name"] = c["func_name"]
            with open(os.path.join(args.workspace, c["worker"],"config.json"), 'w') as json_file:
                json.dump(template, json_file, indent=4)
            os.system("cp registry/* {}".format(os.path.join(args.workspace, c["worker"],"registry/")))