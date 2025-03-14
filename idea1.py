"""
    Generate Dataset
    1. Converting video to frames
    2. Extracting features
    3. Getting change points
    4. User Summary ( for evaluation )
"""
import os
from config import config
from networks.CNN import ResNet
from utils.KTS.cpd_auto import cpd_auto
from tqdm import tqdm
import math
import cv2
import numpy as np
import h5py
import numpy as np




class Generate_Dataset:
    # def __init__(self, video_path, save_path):
    #     self.resnet = ResNet()
    #     self.dataset = {}
    #     self.video_list = []
    #     self.video_path = ''
    #     # print(save_path)
    #     self.h5_file = h5py.File(save_path, 'w')



        self._set_video_list(video_path)

    def _set_video_list(self, video_path):
        # import pdb;pdb.set_trace()
        if os.path.isdir(video_path):
            self.video_path = video_path
            fileExt = r".mp4",".avi"
            self.video_list = [_ for _ in os.listdir(video_path) if _.endswith(fileExt)]
            self.video_list.sort()
        else:
            self.video_path = ''
            
            self.video_list.append(video_path)

        for idx, file_name in enumerate(self.video_list):
            self.dataset['video_{}'.format(idx+1)] = {}
            self.h5_file.create_group('video_{}'.format(idx+1))


    def _extract_feature(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (224, 224))
        res_pool5 = self.resnet(frame)
        frame_feat = res_pool5.cpu().data.numpy().flatten()

        return frame_feat

    def _get_change_points(self, video_feat, n_frame, fps):
        n = n_frame / fps
        m = int(math.ceil(n/2.0))
        K = np.dot(video_feat, video_feat.T)
        change_points, _ = cpd_auto(K, m, 1)
        change_points = np.concatenate(([0], change_points, [n_frame-1]))

        temp_change_points = []
        for idx in range(len(change_points)-1):
            segment = [change_points[idx], change_points[idx+1]-1]
            if idx == len(change_points)-2:
                segment = [change_points[idx], change_points[idx+1]]

            temp_change_points.append(segment)
        change_points = np.array(list(temp_change_points))

        # temp_n_frame_per_seg = []
        # for change_points_idx in range(len(change_points)):
        #     n_frame = change_points[change_points_idx][1] - change_points[change_points_idx][0]
        #     temp_n_frame_per_seg.append(n_frame)
        # n_frame_per_seg = np.array(list(temp_n_frame_per_seg))
        # print(change_points)
        arr = change_points
        list1 = arr.tolist()
        list2 = list1[-1].pop(1) #pop [-1]value 
        print(list2)
        print(list1)
        
        print("****************") # [-1][-1] value find and divided by 15
       
        cps_m = math.floor(arr[-1][1]/15)
        list1[-1].append(cps_m)             #append to list 
        print(list1)
        
        print("****************") #list to nd array convertion
        
        arr = np.asarray(list1)
        print(arr)

        arrmul = arr * 15
        print(arrmul)

        print("****************")   
        # print(type(change_points))
        # print(n_frame_per_seg)
        # print(type(n_frame_per_seg))
        median_frame = []
        for x in arrmul:
            print(x)
            med = np.mean(x)
            print(med)
            int_array = med.astype(int)
            median_frame.append(int_array)
        print(median_frame)
        #   print(type(int_array))
        return arrmul

    # TODO : save dataset
    def _save_dataset(self):
        pass

    def _generator(self, video_idx, video_filename):
            video_idx = video_idx
            print(video_idx)
            import pdb;pdb.set_trace()
            video_path = video_filename
            for video_idx, video_filename in enumerate(video_idx ):
                video_path = video_filename
                if os.path.isdir(self.video_path):
                    video_path = os.path.join(self.video_path, video_filename)
                video_basename = os.path.basename(video_path).split('.')[0]
                video_capture = cv2.VideoCapture(video_path)
                fps = video_capture.get(cv2.CAP_PROP_FPS)
                n_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
                frame_list = []
                picks = []
                video_feat = None
                video_feat_for_train = None
                for frame_idx in tqdm(range(n_frames-1)):
                    success, frame = video_capture.read()
                    if frame_idx % 15 == 0:

                        if success:

                            frame_feat = self._extract_feature(frame)                    
                            picks.append(frame_idx)

                            if video_feat_for_train is None:
                                video_feat_for_train = frame_feat
                            else:
                                video_feat_for_train = np.vstack((video_feat_for_train, frame_feat))
                            if video_feat is None:
                                video_feat = frame_feat
                            else:
                                video_feat = np.vstack((video_feat, frame_feat))
                        else:
                            break
            video_capture.release()
            arrmul = self._get_change_points(video_feat, n_frames, fps)
            self.h5_file['video_{}'.format(video_idx+1)]['features'] = list(video_feat_for_train)
            self.h5_file['video_{}'.format(video_idx+1)]['picks'] = np.array(list(picks))
            self.h5_file['video_{}'.format(video_idx+1)]['n_frames'] = n_frames
            self.h5_file['video_{}'.format(video_idx+1)]['fps'] = fps
            self.h5_file['video_{}'.format(video_idx + 1)]['video_name'] = video_filename.split('.')[0]
            self.h5_file['video_{}'.format(video_idx+1)]['change_points'] = arrmul
            self.h5_file.close()

    def generate_dataset(self):
        print('[INFO] CNN processing')
        Parallel(n_jobs=-1)(delayed(self._generator)(video_idx, video_filename) for video_idx, video_filename in enumerate(self.video_list))


if __name__ == "__main__":
    cd  = Generate_Dataset(video_path, save_path)
    def __init__(self, video_path, save_path):
        self.resnet = ResNet()
        self.dataset = {}
        self.video_list = []
        self.video_path = ''
        # print(save_path)
        self.h5_file = h5py.File(save_path, 'w')