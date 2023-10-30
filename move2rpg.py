import glob
import os
import shutil


def copy_result(oldpath,oldname,newpath,newname):
    oldfile = os.path.join(oldpath, oldname)
    newfile = os.path.join(newpath, newname)

    recordpath = '/home/wuhan2020/yqc/monoi_results/record_null_file.txt'
    isExist = os.path.exists(oldfile)
    if not isExist:
        open(oldfile,'w') #新建txt

        record = open(recordpath,'a')
        record.write(oldfile + '\n')
        record.close()

        print('\n' + 'create null file: '+ oldname+ '.\n')
    shutil.copyfile(oldfile, newfile)



if __name__ == '__main__':
    out_data_path = "/home/wuhan2020/yqc/monoi_results"
    sortd_data_path ="/home/wuhan2020/yqc/rpg_trajectory_evaluation/results/euroc_monoi/laptop/monoi"
    scale_all = ["0.001", "0.01" , "0.1" , "1.0", "10.0", "100.0", "1000.0"]
    rpg_name = ["MH_01", "MH_02", "MH_03", "MH_04", "MH_05",
                 "V1_01", "V1_02", "V1_03",
                 "V2_01", "V2_02", "V2_03"]
    output_name = []
    for i in rpg_name:
        output_name.append(i.replace("_",""))

    for scale_num,scale in enumerate(scale_all):
        for round in range(0, 10):
            for file_num,file in enumerate(output_name):
                print("move: "+os.path.join(scale,str(round+1),file) + " to "+ 'monoi'+str(scale_num+1)+"/"+rpg_name[file_num] + "/traj"+str(round))
                copy_result(os.path.join(out_data_path,scale,str(round+1)) ,
                                      "f_dataset-"+file+"_monoi.txt",
                                      sortd_data_path +str(scale_num+1)+ '/laptop_monoi_' + rpg_name[file_num],
                                      "stamped_traj_estimate" + str(round) + ".txt")

                #注意算法monoi1路径已修改