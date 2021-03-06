import glob
import os
import  sys


def readfilename(path):
    ret = []
    files = glob.glob(path + '/*.yuv')
    for f in files:
        name = f.split('/')[-1]
        name = name.split(".")[0]
        ret.append(name)
    return ret


def crflist(crf):
    ret = []
    for q in crf.split(','):
        ret.append(q)
    return ret


def runvp9(self):
        preset = self.preset_vpx
        width  = self.width
        height = self.height
        rate   = self.fps
        codec  = self.codec
        frames = self.frames
        gop    = self.gop
       
        prefix = "" 
        bin_out_path        = prefix + self.bin_out + height + '/'
        input_sequence_path = prefix + self.test_sequence + height + '/'
        log_out_path        = prefix + self.log_out + height + '/'
        
        file_list = readfilename(input_sequence_path)
        crf_list =  crflist(self.crf)
        for filename in file_list:
            for crf in crf_list: 
                output = filename + '_' + crf + '_' + preset + '_.mp4'
                log_file = filename + '_' + crf + '_' + preset + '_.log'
    
                '''
                ffmpeg -i input.mp4 -c:v libvpx-vp9 -deadline realtime -crf 30 -b:v 0 output.webm
                '''

                command = 'sudo ffmpeg -f rawvideo -pix_fmt yuv420p -s:v '
                command += width + 'x' + height + ' -r ' + rate + ' -i '
                command += input_sequence_path + filename + '.yuv -c:v ' + codec + ' -deadline ' + preset
                command += ' -g ' + gop + ' -crf ' + str(crf)  + ' -b:v 0  -frames:v ' + frames + " "
                command += ' ' +  bin_out_path + output
                command += ' | tee -i ' + log_out_path + log_file
                print(command)
                os.system(command) 
