import subprocess
import os
import glob
import shutil
import math
import numpy as np


#yaml文件处理
def changeYamlConfig(path, key, value):
    with open(path, 'r', encoding='utf-8') as f:
        lines = []  # 创建了一个空列表，里面没有元素
        for line in f.readlines():
            if line != '\n':
                lines.append(line)
        f.close()
    with open(path, 'w', encoding='utf-8') as f:
        flag = 0
        for line in lines:
            if key in line:
                leftstr = line.split(":")[0]
                newline = "{0}: {1}".format(leftstr, value)
                line = newline
                f.write('%s\n' % line)
                flag = 1
            else:
                f.write('%s' % line)
        f.close()
        return flag

#同时改变4个参数
def all_para_settings(scale, yaml_path):
    acc_cov= 0.1
    gyr_cov = 0.1
    b_acc_cov = 0.0001
    b_gyr_cov = 0.0001
    changeYamlConfig(yaml_path, 'acc_cov', acc_cov * scale )
    changeYamlConfig(yaml_path, 'gyr_cov', gyr_cov * scale)
    changeYamlConfig(yaml_path, 'b_acc_cov', b_acc_cov * scale)
    changeYamlConfig(yaml_path, 'b_gyr_cov', b_gyr_cov * scale)

def para_resume(yaml_path):
    all_para_settings(1, yaml_path)


def copy_result(oldpath, oldname, newpath, newname):
    oldfile = os.path.join(oldpath, oldname)
    newfile = os.path.join(newpath, newname)

    isExist_newdir = os.path.exists(newpath)
    if not isExist_newdir:
        os.makedirs(newpath)

    shutil.copyfile(oldfile, newfile)

def copy_gt_to_result(src,dst):

    isExist = os.path.exists(dst)
    if not isExist:
        os.makedirs(dst)
    shutil.copyfile(src+'/stamped_groundtruth.txt', dst + '/stamped_groundtruth.txt')
    shutil.copyfile(src + '/eval_cfg.yaml', dst + '/eval_cfg.yaml')


if __name__ == '__main__':
    #目标：IMU噪声参数四个参数同时调，scale : 10^-3 to 10^3 每种跑10次

    fastlio_dir = '/home/kevin/work/lidar_imu_noise/ros_ws/src/FAST_LIO/'
    yaml_path = fastlio_dir + 'config/imu_noise.yaml'
    pos_log_dir = fastlio_dir + 'Log'
    date = '130405'
    scale_type = "big"      # scale_type = ["big", "small", "single"]
    repeat_time = 5

    rpg_dir = '/home/kevin/work/rpg_trajectory_evaluation'
    rpg_eval_dir = rpg_dir + '/results/fastlio_' + scale_type + '/laptop'
    gt_dir = '/home/kevin/work/rpg_trajectory_evaluation/gt/fastlio/nclt/'+date           # need to modify if add other nclt data

    scale_all = []
    if scale_type == "big":
        for i, num in enumerate(range(-3, 4)):
            scale_all.append(math.pow(10, num))
    elif scale_type == "small":
        for i, num in enumerate(np.linspace(-1, 1, 11)):
            scale_all.append(math.pow(10, num))
    elif scale_type == "single":
        for i, num in enumerate(np.linspace(-1.8, 1.8, 10)):
            scale_all.append(math.pow(10, num))

    #修改噪声参数
    for scale_num, scale in enumerate(scale_all):
        scale = math.pow(scale, 2)     # cov为平方
        if scale_type == 'big' or "small":
            all_para_settings(scale, yaml_path)
        elif scale_type == 'single':
            pass

        # copy gt and config to each data files   eg: stamped_groundtruth.txt  eval_cfg.yaml
        out_dir = rpg_eval_dir + '/scale' + str(scale_num) + '/laptop_scale' + str(scale_num) + '_nclt'+date
        copy_gt_to_result(gt_dir, out_dir)
        for round in range(0, repeat_time):  # 跑10次重复
            os.system('cd /home/kevin/work/lidar_imu_noise/ros_ws')
            os.system('roslaunch fast_lio imu_noise.launch')
            out_name = 'stamped_traj_estimate' + str(round) + '.txt'
            copy_result(pos_log_dir, 'pos_log.txt', out_dir, out_name)
            # 更新pos_log为blank
            file = open(pos_log_dir + '/pos_log.txt', 'w')
            file.close()
    para_resume(yaml_path)