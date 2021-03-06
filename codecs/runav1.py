import glob
import os, sys
import multiprocessing


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


def runav1(self):
        preset = self.preset_26x
        width  = self.width
        height = self.height
        rate   = self.fps
        codec  = self.codec
        frames = self.frames
        gop    = self.gop
        cpus = str(multiprocessing.cpu_count())
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
                ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 1920x1080 -r 25 -i input.yuv -c:v libaom-av1 -preset fast -g 300 -crf 22 -b:v 0 -cpu-used 4 output.mp4
                '''
                command = 'sudo ffmpeg -f rawvideo -pix_fmt yuv420p -s:v '
                command += width + 'x' + height + ' -r ' + rate + ' -i '
                command += input_sequence_path + filename + '.yuv -c:v ' + codec #' -preset ' + preset
                command += ' -g ' + gop + ' -crf ' + crf  + ' -b:v 0 ' + ' -frames:v ' + frames + ' '
                command += '-cpu-used ' + cpus + ' ' +  bin_out_path + output
                command += ' | tee -i ' + log_out_path + log_file
                print(command)
                os.system(command)
