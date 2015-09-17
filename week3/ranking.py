import os
def ranking():
    datalogFile=open(os.path.dirname(__file__)+"/data.log","r")
    ranking_dict={}
    for lines in datalogFile:
        if "CPU" in lines:
            l=lines.split()
            if l[1] in ranking_dict.keys():
                ranking_dict[l[1]].append(float(l[3]))
            else:
                ranking_dict[l[1]]=[float(l[3])]
    for key in ranking_dict.keys():
        min_nums=min(list(ranking_dict[key]))
        max_nums=max(list(ranking_dict[key]))
        avg=sum(list(ranking_dict[key]))/len(ranking_dict[key])
        print ("Test name: {0}\nCPU time: {1:.1f} s (min) \n          {2:.1f} s (avg) \n          {3:.1f} s (max)".format(key,min_nums,avg,max_nums))
ranking()

